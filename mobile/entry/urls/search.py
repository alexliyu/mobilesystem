"""Urls for the entry search"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

urlpatterns = patterns('entry.views.search',
                       url(r'^$', 'entry_search', name='entry_entry_search'),
                       )
