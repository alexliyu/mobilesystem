#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.views.generic.list_detail import object_list

from tagging.views import tagged_object_list

from entry.models import Entry
from settings import PAGINATION
from entry.managers import tags_published
from entry.views.decorators import update_queryset
from entry.views.decorators import template_name_for_entry_queryset_filtered
from utils.views import BaseView
from utils.breadcrumbs import *

tag_list = update_queryset(object_list, tags_published)

class tag_detail(BaseView):
    def get_metadata(self, request):
        return {
            'title': u'标签',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, tag, page=None, **kwargs):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index') , u'标签列表', lazy_reverse('entry_tag_detail', args=[tag, page], ** kwargs)
        )
        
    def handle_GET(self, request, context, tag, page=None, **kwargs):
        template_name = "forum/forum"
    
        if not kwargs.get('template_name'):
            kwargs['template_name'] = template_name_for_entry_queryset_filtered('tag', tag)


        return tagged_object_list(request, tag=tag,
                              queryset_or_model=Entry.published.all(),
                              paginate_by=PAGINATION, page=page,
                              **kwargs)



    
