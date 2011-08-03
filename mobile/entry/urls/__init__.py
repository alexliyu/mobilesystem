#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from entry.views.index import IndexView, category_detail
from entry.views.search import entry_search
from entry.views.entries import entry_index, entry_day, entry_detail, entry_month, entry_shortlink, entry_year
from entry.views.authors import author_list, author_detail
urlpatterns = patterns('',
#    url(r'^tags/', include('entry.urls.tags',)),
#    url(r'^feeds/', include('entry.urls.feeds')),
#    url(r'^authors/', include('entry.urls.authors')),
#    url(r'^categories/', include('entry.urls.categories')),
#    url(r'^search/', include('entry.urls.search')),
#    url(r'^', include('entry.urls.quick_entry')),
#    url(r'^', include('entry.urls.capabilities')),
#    url(r'^', include('entry.urls.entries')),
#    url(r'^', include('entry.urls.index')),
     url(r'^$', IndexView, {}, 'index'),
     url(r'^search/$', entry_search, {}, 'entry_entry_search'),
     url(r'^author/$', author_list, {}, 'entry_author_list'),
     url(r'^author/(?P<username>[.+-@\w]+)/$', author_detail, {}, 'entry_author_detail'),
     url(r'^author/(?P<username>[.+-@\w]+)/page/(?P<page>\d+)/$', author_detail, {}, 'entry_author_detail_paginated'),
     url(r'^page/(?P<page>\d+)/$', entry_index, {}, 'index_paginated'),
     url(r'^(?P<year>\d{4})/$', entry_year, {}, 'entry_entry_archive_year'),
     url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', entry_month, {}, 'entry_entry_archive_month'),
     url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', entry_day, {}, 'entry_entry_archive_day'),
     url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', entry_detail, {}, 'entry_entry_detail'),
     url(r'^(?P<object_id>\d+)/$', entry_shortlink, {}, 'entry_entry_shortlink'),
     url(r'^(?P<path>[-\/\w]+)/page/(?P<page>\d+)/$', category_detail, {}, 'entry_category_detail_paginated'),
     url(r'^(?P<path>[-\/\w]+)/$', category_detail, {}, 'entry_category_detail'),
)
#urlpatterns += patterns('',
#      (r'^static/(?P<path>.*)$', 'django.views.static.serve',
#      {'document_root':  settings.MEDIA_ROOT}),
#      (r'^media/(?P<path>.*)$', 'django.views.static.serve',
#      {'document_root':  settings.MEDIA_ROOT}),
#    )
#
#if settings.DEBUG:
#    urlpatterns = patterns('',
#        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls')),
#    ) + urlpatterns

