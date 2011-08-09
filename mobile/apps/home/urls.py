#-*- coding:utf-8 -*-
"""
这是项目的home应用模块中的URL路由文件.

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
"""
from django.conf.urls.defaults import *

from apps.home.views import (
    IndexView, UserMessageView,
    StaticDetailView,
)

urlpatterns = patterns('',

    (r'^$',
        IndexView, {},
        'index'),
    
    (r'^about/$',
        StaticDetailView,
        {'title':'关于我们', 'template':'about'},
        'static_about'),

    (r'^messages/$',
        UserMessageView, {},
        'messages'),
        
)
