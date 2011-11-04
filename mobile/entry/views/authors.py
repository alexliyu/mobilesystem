#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list

from ..models import Author
from settings import PAGINATION
from .decorators import update_queryset
from .decorators import template_name_for_entry_queryset_filtered
from django.views.decorators.cache import cache_page
from baseutils.views import BaseView
from baseutils.breadcrumbs import *


class author_list(BaseView):
    """显示一个分类中的文章"""
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
        object_list = Author.published.all()
        template_name = 'entry/authors_list'
        context['object_list'] = object_list
        return self.render(request, context, template_name)

class author_detail(BaseView):
    """Display the entries of an author"""
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, username, page=None):
        return Breadcrumb(
            self.conf.local_name, None, u'娱讯互动社区', lazy_reverse('index')
        )
    
    def handle_GET(self, request, context, username, page=None):
        author = get_object_or_404(Author, username=username)
        template_name = template_name_for_entry_queryset_filtered('author', author.username)
        context['author'] = author
        context['queryset'] = author.entries_published()
        context['paginate_by'] = PAGINATION
        context['page'] = page
        return self.render(request, context, template_name)
    
#@cache_page(60 * 300)
#def author_detail(request, username, page=None, **kwargs):
#    """Display the entries of an author"""
#    extra_context = kwargs.pop('extra_context', {})
#
#    author = get_object_or_404(Author, username=username)
#    if not kwargs.get('template_name'):
#        kwargs['template_name'] = template_name_for_entry_queryset_filtered(
#            'author', author.username)
#
#    extra_context.update({'author': author})
#    kwargs['extra_context'] = extra_context
#
#    return object_list(request, queryset=author.entries_published(),
#                       paginate_by=PAGINATION, page=page,
#                       **kwargs)
