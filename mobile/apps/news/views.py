#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from datetime import timedelta
from entry.models import Entry
from django.contrib.auth.models import User
from utils.views import BaseView
from utils.breadcrumbs import BreadcrumbFactory, Breadcrumb, lazy_reverse
from apps.users.models import UserProfile


class IndexView(BaseView):
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, None, u'新闻',
            lazy_reverse('index'))
    
    def handle_GET(self, request, context):
        lotterylist = entry_index
        context['lotterylist'] = lotterylist
        context.update({
           'sent': request.GET.get('sent') == 'true',
           'referer': request.GET.get('referer', ''),
        })
        return self.render(request, context, 'lottery/index',
                           expires=timedelta(days=7))
    
class DetailsView(BaseView):
    @BreadcrumbFactory
    def breadcrumb(self, request, context, slug):
        return Breadcrumb(
            self.conf.local_name, None, u'中奖查询',
            lazy_reverse('Details'))

    def handle_GET(self, request, context, slug):
        #blacklist=User.objects.select_related().filter(lottery=int(slug))
        a = lottery.objects.get(id=int(slug))
        blacklist = a.UserProfile.all()

        context['blacklist'] = blacklist
        context.update({
           'sent': request.GET.get('sent') == 'true',
           'referer': request.GET.get('referer', ''),
        })
        return self.render(request, context, 'lottery/Details',
                           expires=timedelta(days=7))
    
