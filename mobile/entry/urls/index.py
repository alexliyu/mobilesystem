#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
使用通用视图，用于显示index首页
'''
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

from ..models import Category


def get_books():
    pass


info_conf = {
             'queryset': Category.tree.all(),
             'template_name': 'entry/index.html',
             'template_object_name': 'publisher',
             'extra_context': {
                               'book_list': get_books,
                               
                               
                               
                               }
             }

urlpatterns = patterns('django.views.generic.list_detail',
                       url(r'^$', 'object_list',
                           info_conf, 'index'),
                       )

urlpatterns += patterns('entry.views.categories',
                        url(r'^(?P<path>[-\/\w]+)/page/(?P<page>\d+)/$',
                            'category_detail',
                            name='entry_category_detail_paginated'),
                        url(r'^(?P<path>[-\/\w]+)/$', 'category_detail',
                            name='entry_category_detail'),
                        )
