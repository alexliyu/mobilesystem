#-*- coding:utf-8 -*-
"""
这是地图应用程序，用于管理及显示地图

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from datetime import timedelta

from django.http import Http404

from baseutils.views import BaseView
from baseutils.breadcrumbs import *

class IndexView(BaseView):
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name,
            None,
            u'地图',
            lazy_reverse('maps:osm-about'),
        )

    def handle_GET(self, request, context):
        raise Http404

class TouchMapLiteView(BaseView):
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name,
            None,
            u'地图',
            lazy_reverse('maps:touchmaplite'),
        )

    def handle_GET(self, request, context):
        context.update({
            'zoom_controls': True,
        })
        return self.render(request, context, 'maps/touchmaplite/map',
                           expires=timedelta(days=365))
