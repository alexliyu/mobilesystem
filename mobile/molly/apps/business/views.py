#-*- coding:utf-8 -*-
from mobile.molly.utils.views import BaseView
from mobile.molly.utils.breadcrumbs import BreadcrumbFactory, Breadcrumb, lazy_reverse
from mobile.molly.apps.business.models import BusinessInfo, PromotionsInfo
 
class BusinessList(BaseView):
    
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, None, '商家列表',
            lazy_reverse('index'))
        
    def handle_GET(self, request, context):
        businessList = BusinessInfo.objects.all()
        context['businessList'] = businessList
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
        promotionsList = PromotionsInfo.objects.select_related().filter(business=int(slug))
        context['promotionsList'] = promotionsList
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
            self.conf.local_name, None, '联盟商家',
            lazy_reverse('index'))
        
    def handle_GET(self, request, context):
        promotionsList = PromotionsInfo.objects.filter(picSrc__gt='')
        context['promotionsList'] = promotionsList
        context.update({
           'sent': request.GET.get('sent') == 'true',
           'referer': request.GET.get('referer', ''),
        })
        return self.render(request, context, 'promotions/index')  
    
    
