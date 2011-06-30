# Create your views here.
from mobile.molly.utils.views import BaseView
from mobile.molly.utils.breadcrumbs import BreadcrumbFactory, Breadcrumb, lazy_reverse
from mobile.molly.apps.business.models import BusinessInfo, PromotionsInfo
from django.utils.datetime_safe import datetime

class IndexView(BaseView):
    
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, None, 'business',
            lazy_reverse('index'))
        
    def handle_GET(self, request, context):
        businessList=BusinessInfo.objects.all()
        context['businessList']=businessList
        context.update({
           'sent': request.GET.get('sent') == 'true',
           'referer': request.GET.get('referer', ''),
        })
        return self.render(request, context, 'business/index')
        
class PromotionsView(BaseView):
    
    @BreadcrumbFactory
    def breadcrumb(self, request, context,slug):
        return Breadcrumb(
            self.conf.local_name, None, 'promotions',
            lazy_reverse('index'))
        
    def handle_GET(self, request, context,slug):
        promotionsList=PromotionsInfo.objects.select_related().filter(business=int(slug))
        context['promotionsList']=promotionsList
        context.update({
           'sent': request.GET.get('sent') == 'true',
           'referer': request.GET.get('referer', ''),
        })
        return self.render(request, context, 'promotions/index')
    
class PromotionsDetail(BaseView):
    
    @BreadcrumbFactory
    def breadcrumb(self, request, context,slug):
        return Breadcrumb(
            self.conf.local_name, None, 'promotions',
            lazy_reverse('index'))
        
    def handle_GET(self, request, context,slug):
        promotions=PromotionsInfo.objects.get(id=int(slug))
        context['promotions']=promotions
        context.update({
           'sent': request.GET.get('sent') == 'true',
           'referer': request.GET.get('referer', ''),
        })
        return self.render(request, context, 'promotions/promotionsDetail')
    
    
    