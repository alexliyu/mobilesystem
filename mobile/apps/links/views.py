#-*- coding:utf-8 -*-
"""
网址导航应用程序的视图类.

创建于 2011-7-10.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050

       
"""
import urllib
from datetime import timedelta

from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from models import links_class
from utils.views import BaseView
from utils.breadcrumbs import BreadcrumbFactory, Breadcrumb, lazy_reverse


class IndexView(BaseView):
    """
    默认显示视图.
    用于显示网址分类及列表
    """
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, None, u'网址导航',
            lazy_reverse('index'))
    
    def handle_GET(self, request, context):
        linkscategroy = links_class.objects.all()
        context['linkscategroy'] = linkscategroy
        context.update({
           'sent': request.GET.get('sent') == 'true',
           'referer': request.GET.get('referer', ''),
        })
        return self.render(request, context, 'links/index',
                           expires=timedelta(days=7))
    
