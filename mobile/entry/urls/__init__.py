#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^tags/', include('entry.urls.tags',)),
    url(r'^feeds/', include('entry.urls.feeds')),
    url(r'^authors/', include('entry.urls.authors')),
    url(r'^categories/', include('entry.urls.categories')),
    url(r'^search/', include('entry.urls.search')),
    url(r'^', include('entry.urls.quick_entry')),
    url(r'^', include('entry.urls.capabilities')),
    url(r'^', include('entry.urls.entries')),
    url(r'^', include('entry.urls.index')),
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

