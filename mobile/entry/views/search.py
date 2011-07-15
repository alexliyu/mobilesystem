#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list

from entry.models import Entry
from settings import PAGINATION


def entry_search(request):
    """Search entries matching with a pattern"""
    error = None
    pattern = None
    entries = Entry.published.none()

    if request.GET:
        pattern = request.GET.get('pattern', '')
        if len(pattern) < 2:
            error = u'关键词太短了，至少要2个字以上！'
        else:
            entries = Entry.published.search(pattern)
    else:
        error = u'很抱歉，没有搜索到您要找的内容！'

    return object_list(request, queryset=entries,
                       paginate_by=PAGINATION,
                       template_name='entry_search.html',
                       extra_context={'error': error,
                                      'pattern': pattern})
