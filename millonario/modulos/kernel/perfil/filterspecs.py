#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib

from django.db import models
from django.utils.translation import ugettext as _

from django.contrib.admin.filterspecs import DateFieldFilterSpec
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import Form, DateField, CharField, HiddenInput
from django.template import loader, Context
from django.contrib.admin.filterspecs import FilterSpec,DateFieldFilterSpec
import datetime
class DateRangeFilterSpec(DateFieldFilterSpec):
    def __init__(self, f, request, params, model, model_admin,
                 field_path=None):
        super(DateFieldFilterSpec, self).__init__(f, request, params, model,
                                                  model_admin,
                                                  field_path=field_path)

        self.field_generic = '%s__' % self.field_path

        self.date_params = dict([(k, v) for k, v in params.items()
                                 if k.startswith(self.field_generic)])

        today = datetime.date.today()
        hora_actual=datetime.datetime.now().strftime('%Y-%m-%d %H:0:0')
        one_week_ago = today - datetime.timedelta(days=7)
        today_str = isinstance(self.field, models.DateTimeField) \
                    and today.strftime('%Y-%m-%d 23:59:59') \
                    or today.strftime('%Y-%m-%d')

        self.links = (
            (_('Any date'), {}),
            (_('Today'), {'%s__year' % self.field_path: str(today.year),
                       '%s__month' % self.field_path: str(today.month),
                       '%s__day' % self.field_path: str(today.day)}),
            (_('Past 7 days'), {'%s__gte' % self.field_path:
                                    one_week_ago.strftime('%Y-%m-%d'),
                             '%s__lte' % self.field_path: today_str}),
            (_('This month'), {'%s__year' % self.field_path: str(today.year),
                             '%s__month' % self.field_path: str(today.month)}),
            (_('This year'), {'%s__year' % self.field_path: str(today.year)}),
            (_('En La ultima hora'), {'%s__gte' % self.field_path: hora_actual}),
            (_('semana'), {'%s__gte' % self.field_path:
                                    one_week_ago.strftime('%Y-%m-%d'),
                             '%s__lte' % self.field_path: today_str}),

        )

    def title(self):
        return self.field.verbose_name

    def choices(self, cl):
        for title, param_dict in self.links:
            yield {'selected': self.date_params == param_dict,
                   'query_string': cl.get_query_string(
                                   param_dict,
                                   [self.field_generic]),
                   'display': title}

FilterSpec.filter_specs.insert(0, (lambda f: hasattr(f, 'date_range_filter'), DateRangeFilterSpec))