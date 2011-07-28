#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from forms import SignatureForm
from utils.views import BaseView
from utils.breadcrumbs import *


class profile(BaseView):
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, user_id=None):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index') , u'用户资料', lazy_reverse('forum_topic', args=[user_id])
        )
        
    def handle_GET(self, request, context, user_id=None):
        template_name = "forum/account/profile"  
        view_user = request.user
        if user_id:
            view_user = get_object_or_404(User, pk=user_id)
        view_only = view_user != request.user
        context['view_user'] = view_user
        context['view_only'] = view_only
        
        
        return self.render(request, context, template_name) 
      
class signature(BaseView):
    def get_metadata(self, request):
        return {
            'title': u'团购',
            'additional': 'View news feeds and events from across the University.',
        }
        
    @BreadcrumbFactory
    def breadcrumb(self, request, context, form_class=SignatureForm):
        return Breadcrumb(
            self.conf.local_name, lazy_parent('index') , u'注册', lazy_reverse('forum_topic', args=[form_class])
        )
    
    @login_required    
    def handle_GET(self, request, context, form_class=SignatureForm):
        template_name = "forum/account/signature"  
        profile = request.user.get_profile()
        form = form_class(instance=profile)
        context['form'] = form
        return self.render(request, context, template_name) 
   
    @login_required
    def handle_POST(self, request, context, form_class=SignatureForm):
        template_name = "forum/account/signature"  
        profile = request.user.get_profile()
        form = form_class(instance=profile, data=request.POST)
        form.save()
        context['form'] = form
        return self.render(request, context, template_name) 

