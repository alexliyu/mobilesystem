#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from datetime import timedelta
from models import Lottery
from django.contrib.auth.models import User
from mobile.molly.utils.views import BaseView
from mobile.molly.utils.breadcrumbs import BreadcrumbFactory, Breadcrumb, lazy_reverse


class IndexView(BaseView):
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, None, u'中奖查询',
            lazy_reverse('index'))
    
    def handle_GET(self, request, context):
        lotterylist = Lottery.objects.all()
        context['lotterylist'] = lotterylist
        context.update({
           'sent': request.GET.get('sent') == 'true',
           'referer': request.GET.get('referer', ''),
        })
        return self.render(request, context, 'Lottery/index',
                           expires=timedelta(days=7))
    
class DetailsView(BaseView):
    @BreadcrumbFactory
    def breadcrumb(self, request, context, slug):
        return Breadcrumb(
            self.conf.local_name, None, u'中奖查询',
            lazy_reverse('Details'))

    def handle_GET(self, request, context, slug):
        #blacklist=User.objects.select_related().filter(Lottery=int(slug))
        a = Lottery.objects.get(id=int(slug))
        blacklist = a.User.all()
        context['blacklist'] = blacklist
        context.update({
           'sent': request.GET.get('sent') == 'true',
           'referer': request.GET.get('referer', ''),
        })
        return self.render(request, context, 'Lottery/Details',
                           expires=timedelta(days=7))
    
