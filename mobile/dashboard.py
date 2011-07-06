#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    自定义后台面板
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        # append a group for "Administration" & "Applications"
        self.children.append(modules.Group(
            u'管理员工具',
            column=1,
            collapsible=True,
            children=[
                modules.AppList(
                    u'系统管理',
                    column=1,
                    collapsible=False,
                    models=('django.contrib.*',),
                )
            ]
        ))
        
        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            u'应用程序管理',
            collapsible=True,
            column=1,
            
            exclude=('django.contrib.*',),
        ))
        
        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            u'模型管理',
            column=1,
            collapsible=False,
            models=('django.contrib.*',),
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            u'媒体资源管理',
            column=2,
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            u'其他',
            column=2,
            children=[
                {
                    'title': _('Django Documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': u'查看日志',
                    'url': '/sentry',
                    'external': True,
                },
                {
                    'title': u'Lincdm官网',
                    'url': 'http://www.33445120.tk',
                    'external': True,
                },
            ]
        ))
        
        # append a feed module
        self.children.append(modules.Feed(
            _('Latest Django News'),
            column=2,
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))
        
        # append a recent actions module
        self.children.append(modules.RecentActions(
            u'最近动作',
            limit=5,
            collapsible=False,
            column=3,
            ))


