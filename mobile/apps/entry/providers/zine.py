#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
from django.core.paginator import  Paginator, InvalidPage, EmptyPage, PageNotAnInteger

from apps.entry.models import Category, Entry
from settings import PAGINATION
from apps.entry.views.decorators import template_name_for_entry_queryset_filtered
from django.db.models.query import QuerySet
from apps.entry.providers import BaseEntryProvider


class ZineEntryProvider(BaseEntryProvider):
    def __init__(self):
        pass
        
    def get_category_or_404(self, path):
        """Retrieve a Category by a path"""
        path_bits = [p for p in path.split('/') if p]
        return get_object_or_404(Category, slug=path_bits[-1])
    
    def category_list(self, request, path, page=None, **kwargs):
        """显示分类"""
        category = self.get_category_or_404(path)
        return category.children.all()
    
    def detail(self, id):
        """返回内容对象"""
        return Entry.published.get(pk=int(id))
    
    def category_detail(self, request, context, path, page=None, **kwargs):
        """显示一个分类中的文章"""
        category = self.get_category_or_404(path)
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
        context['template_name'] = template_name
        context['page'] = page
        
        return context
