#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list

from ..models import Category
from settings import PAGINATION
from .decorators import template_name_for_entry_queryset_filtered
from django.db.models.query import QuerySet


def get_category_or_404(path):
    """Retrieve a Category by a path"""
    path_bits = [p for p in path.split('/') if p]
    return get_object_or_404(Category, slug=path_bits[-1])


def category_detail(request, path, page=None, **kwargs):
    """显示一个分类中的文章"""
    extra_context = kwargs.pop('extra_context', {})

    category = get_category_or_404(path)
    if not kwargs.get('template_name'):
        kwargs['template_name'] = template_name_for_entry_queryset_filtered(
            'category', category.slug)

    extra_context.update({'category': category})
    kwargs['extra_context'] = extra_context
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
    return object_list(request, queryset=matches,
                       paginate_by=PAGINATION, page=page,
                       ** kwargs)
