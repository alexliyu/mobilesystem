#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''

from utils.views import BaseView
from utils.breadcrumbs import BreadcrumbFactory, Breadcrumb, lazy_reverse



class IndexView(BaseView):
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, None, u'新闻',
            lazy_reverse('index'))
    
    def handle_GET(self, request, context, page=None):
        return self.conf.provider.category_detail(request, 'news', page)
    

    
