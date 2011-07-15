"""Urls for the entry entries"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

from ..models import Entry
from settings import PAGINATION
from settings import ALLOW_EMPTY
from settings import ALLOW_FUTURE

entry_conf_index = {'paginate_by': PAGINATION,
                    'template_name': 'entry/entry_archive.html'}

entry_conf = {'date_field': 'creation_date',
              'allow_empty': ALLOW_EMPTY,
              'allow_future': ALLOW_FUTURE,
              'month_format': '%m',
              'template_name':'entry/entry_list.html',
              }

entry_conf_year = entry_conf.copy()
entry_conf_year['template_name'] = 'entry/date_entry.html'
entry_conf_month = entry_conf_year.copy()
entry_conf_day = entry_conf_year.copy()
entry_conf_year['make_object_list'] = True
del entry_conf_year['month_format']

entry_conf_detail = entry_conf.copy()
del entry_conf_detail['allow_empty']
entry_conf_detail['queryset'] = Entry.published.on_site()
entry_conf_detail['template_name'] = 'entry/entry_detail.html'

urlpatterns = patterns(
    'entry.views.entries',
   
    url(r'^page/(?P<page>\d+)/$',
        'entry_index', entry_conf_index,
        name='index_paginated'),
    url(r'^(?P<year>\d{4})/$',
        'entry_year', entry_conf_year,
        name='entry_entry_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        'entry_month', entry_conf_month,
        name='entry_entry_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        'entry_day', entry_conf_day,
        name='entry_entry_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        'entry_detail', entry_conf_detail,
        name='entry_entry_detail'),
    url(r'^(?P<object_id>\d+)/$',
        'entry_shortlink',
        name='entry_entry_shortlink'),
    )
