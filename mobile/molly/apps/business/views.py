#-*- coding:utf-8 -*-
from mobile.molly.utils.views import BaseView
from mobile.molly.utils.breadcrumbs import BreadcrumbFactory, Breadcrumb, lazy_reverse
from mobile.molly.apps.business.models import BusinessInfo, PromotionsInfo
from django.core.paginator import  Paginator,InvalidPage,EmptyPage,PageNotAnInteger
 
class BusinessList(BaseView):
    
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, None, '商家列表',
            lazy_reverse('index'))
        
    def handle_GET(self, request, context):
        
        after_range_num = 4
        bevor_range_num = 5
        try:
            page = int(request.GET.get("page",1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1    
            
        businessList = BusinessInfo.objects.order_by('id').all()
        paginator = Paginator(businessList,10) 
        
        try:
            list = paginator.page(page)
        except(EmptyPage,InvalidPage,PageNotAnInteger):
            list = paginator.page(1)
        if page >= after_range_num:
            page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
        else:
            page_range = paginator.page_range[0:int(page)+bevor_range_num]

        context['list'] = list
        context['page_range']=page_range
        context.update({
           'sent': request.GET.get('sent') == 'true',
           'referer': request.GET.get('referer', ''),
        })
        return self.render(request, context, 'business/index')
    
class BusinessDetail(BaseView):
    
    @BreadcrumbFactory
    def breadcrumb(self, request, context, slug):
        return Breadcrumb(
            self.conf.local_name, None, '商家详情',
            lazy_reverse('index'))
        
    def handle_GET(self, request, context, slug):
        business = BusinessInfo.objects.get(id=int(slug))
        context['business'] = business
        context.update({
           'sent': request.GET.get('sent') == 'true',
           'referer': request.GET.get('referer', ''),
        })
        
        return self.render(request, context, 'business/businessDetail')
        
class PromotionsView(BaseView):
    
    @BreadcrumbFactory
    def breadcrumb(self, request, context, slug):
        return Breadcrumb(
            self.conf.local_name, None, '优惠活动',
            lazy_reverse('index'))
        
    def handle_GET(self, request, context, slug):
        
        after_range_num = 4
        bevor_range_num = 5
        try:
            page = int(request.GET.get("page",1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1    
        
        promotionsList = PromotionsInfo.objects.select_related().filter(business=int(slug))
        paginator = Paginator(promotionsList,10) 
        
        try:
            list = paginator.page(page)
        except(EmptyPage,InvalidPage,PageNotAnInteger):
            list = paginator.page(1)
        if page >= after_range_num:
            page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
        else:
            page_range = paginator.page_range[0:int(page)+bevor_range_num]
            
        context['page_range']=page_range
        context['list'] = list
        context.update({
           'sent': request.GET.get('sent') == 'true',
           'referer': request.GET.get('referer', ''),
        })
        return self.render(request, context, 'promotions/index')
    
class PromotionsDetail(BaseView):
    
    @BreadcrumbFactory
    def breadcrumb(self, request, context, slug):
        return Breadcrumb(
            self.conf.local_name, None, '活动详情',
            lazy_reverse('index'))
        
    def handle_GET(self, request, context, slug):
        promotions = PromotionsInfo.objects.get(id=int(slug))
        context['promotions'] = promotions
        context.update({
           'sent': request.GET.get('sent') == 'true',
           'referer': request.GET.get('referer', ''),
        })
        
        return self.render(request, context, 'promotions/promotionsDetail')
  
class PromotionsList(BaseView):
    
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, None, '优惠活动',
            lazy_reverse('index'))
        
    def handle_GET(self, request, context):
        
        after_range_num = 4
        bevor_range_num = 5
        try:
            page = int(request.GET.get("page",1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1    
        
        promotionsList = PromotionsInfo.objects.filter(picSrc__gt='')
        paginator = Paginator(promotionsList,10) 
        
        try:
            list = paginator.page(page)
        except(EmptyPage,InvalidPage,PageNotAnInteger):
            list = paginator.page(1)
        if page >= after_range_num:
            page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
        else:
            page_range = paginator.page_range[0:int(page)+bevor_range_num]
         
        context['page_range']=page_range   
        context['list'] = list
        context.update({
           'sent': request.GET.get('sent') == 'true',
           'referer': request.GET.get('referer', ''),
        })
        return self.render(request, context, 'promotions/index')  
    
    
