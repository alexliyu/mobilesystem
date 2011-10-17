#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from datetime import datetime, timedelta

from utils.views import BaseView
from utils.breadcrumbs import *

from models import Weather

class IndexView(BaseView):
    def initial_context(self, request):
        try:
            observation = Weather.objects.latest('published_date')
        except Weather.DoesNotExist:
            observation = None
        return {
            'observation': observation,
           
        }

    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            'weather',
            None,
            u'天气预报',
            lazy_reverse('index'),
        )

    def handle_GET(self, request, context):
        return self.render(request, context, 'weather/index',
                           expires=timedelta(minutes=10))
