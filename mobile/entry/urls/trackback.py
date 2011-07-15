"""Urls for the entry trackback"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

urlpatterns = patterns('entry.views.trackback',
                       url(r'^(?P<slug>[-\w]+)/$', 'entry_trackback',
                           name='entry_entry_trackback'),
                       )
