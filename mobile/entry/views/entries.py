#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
from django.views.generic.date_based import archive_year
from django.views.generic.date_based import archive_month
from django.views.generic.date_based import archive_day
from django.views.generic.date_based import object_detail
from django.contrib.auth.views import login

from entry.models import Entry
from entry.views.decorators import protect_entry, password
from entry.views.decorators import update_queryset
from settings import PAGINATION
from settings import ALLOW_EMPTY
from settings import ALLOW_FUTURE
from utils.views import BaseView
from utils.breadcrumbs import *

from actstream import action

#entry_index = update_queryset(object_list, Entry.published.all)
#
#entry_year = update_queryset(archive_year, Entry.published.all)
#
#entry_month = update_queryset(archive_month, Entry.published.all)
#
#entry_day = update_queryset(archive_day, Entry.published.all)
#
#entry_detail = protect_entry(object_detail)

class entry_index(BaseView):
    """显示一个分类中的文章"""
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
        object_list = Entry.published.all()
        template_name = 'entry/entry_archive'
        context['object_list'] = object_list
        context['paginate_by'] = PAGINATION

        return self.render(request, context, template_name)

class entry_year(BaseView):
    """显示一个分类中的文章"""
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, year):
        return Breadcrumb(
            self.conf.local_name, None, u'娱讯厦门', lazy_reverse('index')
        )
        
    def handle_GET(self, request, context, year):
        archive_year = Entry.published.all()
        template_name = 'entry/date_entry'
        context['archive_year'] = archive_year
        context['paginate_by'] = PAGINATION
        context['date_field'] = 'creation_date'
        context['allow_empty'] = ALLOW_EMPTY
        context['allow_future'] = ALLOW_FUTURE
        #context['month_format'] = '%m'
        context['make_object_list'] = True

        return self.render(request, context, template_name)
    
class entry_month(BaseView):
    """显示一个分类中的文章"""
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, year, month):
        return Breadcrumb(
            self.conf.local_name, None, u'娱讯厦门', lazy_reverse('index')
        )
        
    def handle_GET(self, request, context, year, month):
        archive_month = Entry.published.all()
        template_name = 'entry/date_entry'
        context['archive_month'] = archive_month
        context['paginate_by'] = PAGINATION
        context['date_field'] = 'creation_date'
        context['allow_empty'] = ALLOW_EMPTY
        context['allow_future'] = ALLOW_FUTURE
        context['month_format'] = '%m'
        context['make_object_list'] = True
        
        
        return self.render(request, context, template_name)
    
class entry_day(BaseView):
    """显示一个分类中的文章"""
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, year, month, day):
        return Breadcrumb(
            self.conf.local_name, None, u'娱讯厦门', lazy_reverse('index')
        )
        
    def handle_GET(self, request, context, year, month, day):
        entry_day = Entry.published.all()
        template_name = 'entry/date_entry'
        context['entry_day'] = entry_day
        context['paginate_by'] = PAGINATION
        context['date_field'] = 'creation_date'
        context['allow_empty'] = ALLOW_EMPTY
        context['allow_future'] = ALLOW_FUTURE
        context['month_format'] = '%m'
        context['make_object_list'] = True

        return self.render(request, context, template_name)

class entry_detail(BaseView):
    """显示一个分类中的文章"""
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, year, month, day, slug):
        self.entry = get_object_or_404(Entry, slug=slug, creation_date__year=year, creation_date__month=month, creation_date__day=day)
        return Breadcrumb(
            self.conf.local_name, lazy_parent('entry_category_detail', self.entry.categories.get().slug) , self.entry.title, lazy_reverse('entry_entry_detail', year=year, month=month, day=day, slug=slug)
        )
        
    def handle_GET(self, request, context, year, month, day, slug):
        template_name = 'entry/entry_detail'
        entry = self.entry

        if entry.login_required and not request.user.is_authenticated():
            return login(request, 'login.html')
        if entry.password and entry.password != \
               request.session.get('entry_entry_%s_password' % entry.pk):
            return password(request, entry)
        template_name = entry.template
        context['object'] = entry
        context['paginate_by'] = PAGINATION
        context['date_field'] = 'creation_date'
        context['allow_future'] = ALLOW_FUTURE
        context['month_format'] = '%m'
        context['make_object_list'] = True
        context['queryset'] = Entry.published.on_site()
        
        action.send(request.user, verb=u'正在浏览', target=entry)
        return self.render(request, context, template_name)
        
class entry_shortlink(BaseView):
    """显示一个分类中的文章"""
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, object_id):
        return Breadcrumb(
            self.conf.local_name, None, u'娱讯厦门', lazy_reverse('index')
        )
        
    def handle_GET(self, request, context, object_id):

        entry = get_object_or_404(Entry, pk=object_id)
        return self.redirect(entry.get_absolute_url(), request)


