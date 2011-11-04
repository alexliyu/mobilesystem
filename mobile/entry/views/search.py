#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list

from entry.models import Entry
from settings import PAGINATION
from baseutils.views import BaseView
from baseutils.breadcrumbs import *

class entry_search(BaseView):
    """Search entries matching with a pattern"""
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, None, u'娱讯互动社区', lazy_reverse('index')
        )
        
    def handle_GET(self, request, context):
        error = None
        pattern = None
        entries = Entry.published.none()
        template_name = 'entry/entry_search'
        pattern = request.GET.get('pattern', '')
        if len(pattern) < 2:
            error = u'关键词太短了，至少要2个字以上！'
        else:
            entries = Entry.published.search(pattern)
                
        context['queryset'] = entries
        context['paginate_by'] = PAGINATION
        context['error'] = error
        context['pattern'] = pattern

        return self.render(request, context, template_name)

