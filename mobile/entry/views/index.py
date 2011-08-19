#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2011-8-3

@author: 李昱 Email:alexliyu2012@gmail.com QQ:939567050
__________________________________________________________
'''

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.csrf.middleware import csrf_exempt
from django.db.models.query import QuerySet
from django.core.paginator import  Paginator, InvalidPage, EmptyPage, PageNotAnInteger

from entry.models import Category, Entry
from utils.views import BaseView
from utils.breadcrumbs import *
from settings import PAGINATION
from .decorators import template_name_for_entry_queryset_filtered




class IndexView(BaseView):
    """
    资讯、生活的首页定义类
    """
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, None, u'娱讯厦门', lazy_reverse('index')
        )
        
    def handle_GET(self, request, context):
        template_name = 'entry/index'
        context['category'] = Category.tree.all()
        context['object_list'] = Entry.published.all()[:10]
        return self.render(request, context, template_name)
    
class category_detail(BaseView):
    """显示一个分类中的文章"""
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, path, page=None):
        self.category = get_category_or_404(path)
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index'), self.category, lazy_reverse('entry_category_detail', args=[self.category.slug])
        )
        
    def handle_GET(self, request, context, path, page=None):
        category = self.category
        template_name = 'entry/entry_list'
        context['category'] = category
        

        matches = QuerySet
        '''
        这里用于获取category的下级分类的查询记录集，并进行合并，生成一个查询记录集
        '''
        if category.children.all():
                for child in category.children.all():
                    try:
                            matches = matches() | child.entries_published()
                    except:
                            matches = child.entries_published()
                matches = matches | category.entries_published()
        else:
                matches = category.entries_published()
        
     
        try:
            if page < 1:
                page = 1
        except ValueError:
            page = 1    
            
       
        paginator = Paginator(matches, PAGINATION) 
        
        try:
            list = paginator.page(page)
        except(EmptyPage, InvalidPage, PageNotAnInteger):
            list = paginator.page(1)
       
                    
        
        context['page_object'] = list
        context['paginate_by'] = PAGINATION
        context['page'] = page
       

        return self.render(request, context, template_name)

def get_category_or_404(path):
    """Retrieve a Category by a path"""
    path_bits = [p for p in path.split('/') if p]
    return get_object_or_404(Category, slug=path_bits[-1])



