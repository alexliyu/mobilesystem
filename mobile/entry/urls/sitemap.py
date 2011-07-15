"""Urls for the entry sitemap"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

urlpatterns = patterns('entry.views.sitemap',
                       url(r'^$', 'sitemap',
                           {'template': 'entry/sitemap.html'},
                           name='entry_sitemap'),
                       )
