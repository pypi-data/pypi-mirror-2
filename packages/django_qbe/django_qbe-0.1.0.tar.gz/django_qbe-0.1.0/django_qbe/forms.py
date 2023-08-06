# -*- coding: utf-8 -*-
from django import forms
from django.db import connection
from django.db.models.fields import Field
from django.core.urlresolvers import reverse
from django.conf import settings
from django.forms.formsets import BaseFormSet, formset_factory
from django.utils.importlib import import_module
from django.utils.translation import ugettext as _

from django_qbe.widgets import CriteriaInput

try:
    module = "django.db.backends.%s" % settings.DATABASE_ENGINE
    base_mod = import_module("%s.base" % module)
    OPERATORS = base_mod.DatabaseWrapper.operators
    intros_mod = import_module("%s.introspection" % module)
    TABLE_NAMES = intros_mod.DatabaseIntrospection(connection).table_names()
except ImportError:
    OPERATORS = {}
    TABLE_NAMES = []

SORT_CHOICES = (
    ("", ""),
    ("asc", _("Ascending")),
    ("des", _("Descending")),
)


class QueryByExampleForm(forms.Form):
    show = forms.BooleanField(label=_("Show"), required=False)
    model = forms.CharField(label=_("Model"))
    field = forms.CharField(label=_("Field"))
    criteria = forms.CharField(label=_("Criteria"), required=False)
    sort = forms.ChoiceField(label=_("Sort"), choices=SORT_CHOICES,
                             required=False)

    def __init__(self, *args, **kwargs):
        super(QueryByExampleForm, self).__init__(*args, **kwargs)
        model_widget = forms.Select(attrs={'class': "qbeFillModels to:field"})
        self.fields['model'].widget = model_widget
        sort_widget = forms.Select(attrs={'disabled': "disabled",
                                          'class': 'submitIfChecked'},
                                   choices=SORT_CHOICES)
        self.fields['sort'].widget = sort_widget
        criteria_widget = CriteriaInput(attrs={'disabled': "disabled"})
        self.fields['criteria'].widget = criteria_widget
        criteria_widgets = getattr(criteria_widget, "widgets", [])
        if criteria_widgets:
            criteria_len = len(criteria_widgets)
            criteria_names = ",".join([("criteria_%s" % s)
                                       for s in range(0, criteria_len)])
            field_attr_class = "qbeFillFields enable:sort,%s" % criteria_names
        else:
            field_attr_class = "qbeFillFields enable:sort,criteria"
        field_widget = forms.Select(attrs={'class': field_attr_class})
        self.fields['field'].widget = field_widget

    def clean_model(self):
        model = self.cleaned_data['model']
        return model.lower().replace(".", "_")

    def clean_criteria(self):
        criteria = self.cleaned_data['criteria']
        try:
            operator, over = eval(criteria, {}, {})
            return (operator, over)
        except:
            return (None, None)


class BaseQueryByExampleFormSet(BaseFormSet):
    _selects = []
    _froms = []
    _wheres = []
    _sorts = []
    _params = []
    _raw_query = None

    def clean(self):
        """
        Checks that there is almost one field to select
        """
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on
            # its own
            return
        selects, froms, wheres, sorts, params = self.get_query_parts()
        if not selects:
            validation_message = _(u"At least you must check a row to get.")
            raise forms.ValidationError, validation_message
        self._selects = selects
        self._froms = froms
        self._wheres = wheres
        self._sorts = sorts
        self._params = params

    def get_query_parts(self):
        """
        Return SQL query for cleaned data
        """
        selects = []
        froms = []
        wheres = []
        sorts = []
        params = []
        for data in self.cleaned_data:
            if not ("model" in data and "field" in data):
                break
            model = data["model"]
            field = data["field"]
            show = data["show"]
            criteria = data["criteria"]
            sort = data["sort"]
            db_field = u"%s.%s" % (model, field)
            operator, over = criteria
            is_join = operator.lower() == 'join'
            if show and not is_join:
                selects.append(db_field)
            if sort:
                sorts.append(db_field)
            if all(criteria):
                if is_join:
                    over_split = over.lower().rsplit(".", 1)
                    join_model = over_split[0].replace(".", "_")
                    join_field = over_split[1]
                    join = u"%s.%s = %s_id" \
                           % (join_model, join_field, db_field)
                    if join not in wheres and join_model in TABLE_NAMES:
                        wheres.append(join)
                        if join_model not in froms:
                            froms.append(join_model)
                    # join_select = u"%s.%s" % (join_model, join_field)
                    # if join_select not in selects:
                    #     selects.append(join_select)
                elif operator in OPERATORS:
                    # db_operator = OPERATORS[operator] % over
                    db_operator = OPERATORS[operator]
                    lookup = self._get_lookup(operator, over)
                    params.append(lookup)
                    wheres.append(u"%s %s" % (db_field, db_operator))
            if model not in froms and model in TABLE_NAMES:
                froms.append(model)
        return selects, froms, wheres, sorts, params

    def get_raw_query(self, limit=None, offset=None, count=False,
                      add_extra_ids=False, add_params=False):
        if self._raw_query:
            return self._raw_query
        if self._sorts:
            order_by = u"ORDER BY %s" % (", ".join(self._sorts))
        else:
            order_by = u""
        if self._wheres:
            wheres = u"WHERE %s" % (" AND ".join(self._wheres))
        else:
            wheres = u""
        if count:
            selects = (u"COUNT(*) as count", )
            order_by = u""
        elif add_extra_ids:
            selects = self._get_selects_with_extra_ids()
        else:
            selects = self._selects
        limits = u""
        if limit:
            try:
                limits = u"LIMIT %s" % int(limit)
            except ValueError:
                pass
        offsets = u""
        if offset:
            try:
                offsets = u"OFFSET %s" % int(offset)
            except ValueError:
                pass
        sql = u"""SELECT %s FROM %s %s %s %s %s;""" \
              % (", ".join(selects),
                 ", ".join(self._froms),
                 wheres,
                 order_by,
                 limits,
                 offsets)
        if add_params:
            return u"%s /* %s */" % (sql, ", ".join(self._params))
        else:
            return sql

    def get_results(self, limit=None, offset=None, query=None, admin_name=None,
                    row_number=False):
        """
        Fetch all results after perform SQL query and
        """
        add_extra_ids = (admin_name != None)
        if not query:
            sql = self.get_raw_query(limit=limit, offset=offset,
                                     add_extra_ids=add_extra_ids)
        else:
            sql = query
        if settings.DEBUG:
            print sql
        cursor = connection.cursor()
        cursor.execute(sql, tuple(self._params))
        query_results = cursor.fetchall()
        if admin_name:
            selects = self._get_selects_with_extra_ids()
            results = []
            try:
                offset = int(offset)
            except ValueError:
                offset = 0
            for r, row in enumerate(query_results):
                i = 0
                l = len(row)
                if row_number:
                    result = [(r + offset + 1, u"#row%s" % (r + offset + 1))]
                else:
                    result = []
                while i < l:
                    appmodel, field = selects[i].split(".")
                    admin_url = reverse("%s:%s_change" % (admin_name,
                                                           appmodel),
                                         args=[row[i + 1]])
                    result.append((row[i], admin_url))
                    i += 2
                results.append(result)
            return results
        else:
            if row_number:
                results = []
                for r, row in enumerate(query_results):
                    result = [r + 1]
                    for cell in row:
                        result.append(cell)
                    results.append(result)
                return results
            else:
                return query_results

    def get_count(self):
        query = self.get_raw_query(count=True)
        results = self.get_results(query=query)
        if results:
            return float(results[0][0])
        else:
            return len(self.get_results())

    def get_labels(self, add_extra_ids=False, row_number=False):
        if row_number:
            labels = [_(u"#")]
        else:
            labels = []
        if add_extra_ids:
            selects = self._get_selects_with_extra_ids()
        else:
            selects = self._selects
        if selects and isinstance(selects, (tuple, list)):
            for select in selects:
                label_splits = select.replace("_", ".").split(".")
                label = u"%s.%s: %s" % (label_splits[0].capitalize(),
                                        label_splits[1].capitalize(),
                                        label_splits[2].capitalize())
                labels.append(label)
        return labels

    def _get_lookup(self, operator, over):
        lookup = Field().get_db_prep_lookup(operator, over,
                                            connection=connection,
                                            prepared=True)
        string_related_operators = ('exact', 'contains', 'regex', 'startswith', 
                                    'endswith', 'iexact', 'endswith', 'iregex',
                                    'istartswith','icontains')
        if isinstance(lookup, (tuple, list)):
            return lookup[0]
        return lookup

    def _get_selects_with_extra_ids(self):
        selects = []
        for select in self._selects:
            appmodel, field = select.split(".")
            selects.append(select)
            selects.append("%s.id" % appmodel)
        return selects

QueryByExampleFormSet = formset_factory(QueryByExampleForm,
                                        formset=BaseQueryByExampleFormSet,
                                        extra=1,
                                        can_delete=True)
