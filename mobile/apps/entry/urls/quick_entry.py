"""Url for the entry quick entry view"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

urlpatterns = patterns('entry.views.quick_entry',
                       url(r'^quick_entry/$', 'view_quick_entry',
                           name='entry_entry_quick_post')
                       )
