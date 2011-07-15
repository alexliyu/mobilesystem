"""Urls for the entry tags"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

tag_conf = {'template_name': 'entry/tag_list.html'}

urlpatterns = patterns('entry.views.tags',
                       url(r'^$', 'tag_list',
                           tag_conf, name='entry_tag_list'),
                       url(r'^(?P<tag>[- \w]+)/$', 'tag_detail',
                           name='entry_tag_detail'),
                       url(r'^(?P<tag>[- \w]+)/page/(?P<page>\d+)/$',
                           'tag_detail', name='entry_tag_detail_paginated'),
                       )
