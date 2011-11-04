#-*- coding:utf-8 -*-
from datetime import timedelta
from xml.sax.saxutils import escape

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from baseutils.views import BaseView
from baseutils.breadcrumbs import *



class IndexView(BaseView):
    def get_metadata(self, request):
        return {
            'title': 'Events',
            'additional': 'View events from across the University.',
        }

    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, None, '消防知识', lazy_reverse('xiaofang:index')
        )

    def handle_GET(self, request, context, page=None):
        context['zine_list'] = self.conf.provider.category_list(request, 'xiaofang', page)
        return self.render(request, context, 'xiaofang/index',
                           expires=timedelta(days=7))
        
class TypeView(BaseView):
    def get_metadata(self, request):
        return {
            'title': 'Events',
            'additional': 'View events from across the University.',
        }

    @BreadcrumbFactory
    def breadcrumb(self, request, context, path, slug=None, page=None):
        return Breadcrumb(
            self.conf.local_name, None, '消防知识', lazy_reverse('xiaofang:index')
        )

    def handle_GET(self, request, context, path, slug=None, page=None):
        context['path'] = path
        context['zine_list'] = self.conf.provider.category_list(request, path, page)
        return self.render(request, context, 'xiaofang/index',
                           expires=timedelta(days=7))

class ItemListView(BaseView):
    def get_metadata(self, request, path, slug):
        return {
            'title': 'Events',
            'additional': 'View events from across the University.',
        }

    @BreadcrumbFactory
    def breadcrumb(self, request, context, path, slug, page=None):
        context = self.conf.provider.category_detail(request, context, slug, page)
        return Breadcrumb(
            self.conf.local_name,
            lazy_parent('xiaofang:type-list', path),
            context['category'].title,
            lazy_reverse('item-list', args=[path, slug])
        )

    def handle_GET(self, request, context, path, slug, page=None):
        context['path'] = path
        context['slug'] = slug
        return self.render(request, context, 'xiaofang/item_list')

class ItemDetailView(BaseView):
    def get_metadata(self, request, path, slug, id):
        return {
            'title': 'Events',
            'additional': 'View events from across the University.',
        }

    @BreadcrumbFactory
    def breadcrumb(self, request, context, path, slug, id):
        return Breadcrumb(
            self.conf.local_name,
            lazy_parent('xiaofang:item-list', args=[path, slug]),
            '栏目内容',
            lazy_reverse('item-detail', args=[path, slug, id])
        )

    def handle_GET(self, request, context, path, slug, id):
        item = self.conf.provider.detail(id)
        context.update({
            'item': item
        })
        return self.render(request, context, 'xiaofang/item_detail')
