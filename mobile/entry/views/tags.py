#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.views.generic.list_detail import object_list

from tagging.views import tagged_object_list

from entry.models import Entry
from settings import PAGINATION
from entry.managers import tags_published
from entry.views.decorators import update_queryset
from entry.views.decorators import template_name_for_entry_queryset_filtered
from baseutils.views import BaseView
from baseutils.breadcrumbs import *
from django.shortcuts import get_object_or_404



class tag_list(BaseView):
    def get_metadata(self, request):
        return {
            'title': u'标签',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, tag, page=None, **kwargs):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index') , u'标签列表', lazy_reverse('tag_list')
        )
        
    def handle_GET(self, request, context, tag, page=None, **kwargs):
        template_name = "entry/tag_list"
        context['object_list'] = tags_published()
        context['tag'] = tag
        context['queryset_or_model'] = tags_published()
        context['page'] = page
        return self.render(request, context, template_name)
       
        
class tag_detail(BaseView):
    def get_metadata(self, request):
        return {
            'title': u'标签',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, tag, page=None, **kwargs):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index') , tag, lazy_reverse('entry_tag_detail', args=[tag, page], ** kwargs)
        )
        
    def handle_GET(self, request, context, tag, page=None, **kwargs):
        entry = Entry.published.all().filter(tags__contains=tag).filter(status=2)
        template_name = "entry/entry_list"
        context['object_list'] = entry
        context['tag'] = tag
        context['queryset_or_model'] = entry
        context['page'] = page
        context['paginate_by'] = PAGINATION
        return self.render(request, context, template_name)



    
