#-*- coding:utf-8 -*-
from baseutils.views import BaseView
from baseutils.breadcrumbs import BreadcrumbFactory, Breadcrumb, lazy_reverse, lazy_parent
from apps.business.models import BusinessInfo, PromotionsInfo
from django.core.paginator import  Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import settings
from apps.interactive.models import Interactive_Info, Interactive_User, \
    Interactive_Categries
from apps.interactive.form import PostForm
class IndexView(BaseView):
    
    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index'), '互动',
            lazy_reverse('index'))
        
    def handle_GET(self, request, context):
        templates = 'interactive/index'
        interactive_list = Interactive_Info.objects.all()[:5]
        interactive_user = Interactive_User.objects.all()[:5]
        interactive_categries = Interactive_Categries.objects.all()
        
        context['interactive_list'] = interactive_list
        context['interactive_user'] = interactive_user
        context['interactive_categries'] = interactive_categries
        
        return self.render(request, context, templates)
    
class InteractiveList(BaseView):
    
    @BreadcrumbFactory
    def breadcrumb(self, request, context, slug, page=None):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index'), '活动列表',
            lazy_reverse('index'))
        
    
    def handle_GET(self, request, context, slug, page=None):
        templates = 'interactive/categries_list'
        category = Interactive_Categries.objects.get(slug=slug)
        matches = Interactive_Info.objects.all().filter(category=category)
        try:
            if page < 1:
                page = 1
        except ValueError:
            page = 1    
            
       
        paginator = Paginator(matches, settings.PAGINATION) 
        
        try:
            list = paginator.page(page)
        except(EmptyPage, InvalidPage, PageNotAnInteger):
            list = paginator.page(1)
       
                    
        
        context['page_object'] = list
        context['paginate_by'] = settings.PAGINATION
        context['page'] = page
        context['category'] = category
        
        
        
        
        return self.render(request, context, templates)
    
    
class InteractiveDetail(BaseView):
    
    @BreadcrumbFactory
    def breadcrumb(self, request, context, slug):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index'), '互动详情',
            lazy_reverse('index'))
        
    def handle_GET(self, request, context, slug):
        templates = 'interactive/detail'
        interactive_info = Interactive_Info.objects.get(pk=slug)
        users_list = Interactive_User.objects.filter(interactive_info=interactive_info)
        context['object'] = interactive_info
        context['users_list'] = users_list
        
        return self.render(request, context, templates)
        
class InteractivePost(BaseView):
    
    @BreadcrumbFactory
    def breadcrumb(self, request, context, slug):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index'), '参与互动',
            lazy_reverse('index'))
        
    def handle_GET(self, request, context, slug):
        templates = 'interactive/detail'
        interactive_info = Interactive_Info.objects.get(pk=slug)
        users_list = Interactive_User.objects.filter(interactive_info=interactive_info)
        context['object'] = interactive_info
        context['users_list'] = users_list
        
        return self.render(request, context, templates)
    
    def handle_POST(self, request, context, slug):
        templates = 'interactive/detail'
        
        form = PostForm(request.POST, user=request.user, slug=slug, file=request.FILES.get('attachments', None))
        if form.is_valid() and request.POST.get('submit', ''):
            post = form.save()
            
        interactive_info = Interactive_Info.objects.get(pk=slug)
        users_list = Interactive_User.objects.filter(interactive_info=interactive_info)
        context['object'] = interactive_info
        context['users_list'] = users_list
        
        return self.render(request, context, templates)
    
class PromotionsView(BaseView):
    
    @BreadcrumbFactory
    def breadcrumb(self, request, context, slug):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index'), '优惠活动',
            lazy_reverse('index'))
        
    def handle_GET(self, request, context, slug):
        
        after_range_num = 0
        bevor_range_num = 0
        try:
            page = int(request.GET.get("page", 1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1    
        
        promotionsList = PromotionsInfo.objects.select_related().filter(business=int(slug))
        paginator = Paginator(promotionsList, 10) 
        
        try:
            list = paginator.page(page)
        except(EmptyPage, InvalidPage, PageNotAnInteger):
            list = paginator.page(1)
        if page >= after_range_num:
            page_range = paginator.page_range[page - after_range_num:page + bevor_range_num]
        else:
            page_range = paginator.page_range[0:int(page) + bevor_range_num]
            
        context['page_range'] = page_range
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
            self.conf.local_name, lazy_parent('index'), '活动详情',
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
            self.conf.local_name, lazy_parent('index'), '优惠活动',
            lazy_reverse('index'))
        
    def handle_GET(self, request, context):
        
        after_range_num = 0
        bevor_range_num = 0
        try:
            page = int(request.GET.get("page", 1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1    
        
        promotionsList = PromotionsInfo.objects.filter(picSrc__gt='')
        paginator = Paginator(promotionsList, 10) 
        
        try:
            list = paginator.page(page)
        except(EmptyPage, InvalidPage, PageNotAnInteger):
            list = paginator.page(1)
        if page >= after_range_num:
            page_range = paginator.page_range[page - after_range_num:page + bevor_range_num]
        else:
            page_range = paginator.page_range[0:int(page) + bevor_range_num]
         
        context['page_range'] = page_range   
        context['list'] = list
        context.update({
           'sent': request.GET.get('sent') == 'true',
           'referer': request.GET.get('referer', ''),
        })
        return self.render(request, context, 'promotions/index')  
    
class PicDownload(BaseView):
    
    def handle_GET(self, request, context):
        
        imgUrl = request.path[9:]
        
        file_object = open(settings.UPLOADS_ROOT + imgUrl[21:], 'rb')
        try:
            all_the_images = file_object.read()
        finally:
            file_object.close()
        
#        all_the_images=
                
        response = HttpResponse(mimetype='application/ms-excel') 
        response['Content-Disposition'] = 'attachment; filename=' + imgUrl[22:]
        response.write(all_the_images)  
        return response
    
    
