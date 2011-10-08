#-*- coding:utf-8 -*-
"""
这是用户后台管理模型定义文件.

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import random

from userena.models import UserenaSignup, Note, Category, Area
from userena.utils import get_profile_model
from mobile.utils.sms import sms
from actstream.views import user



class UserenaSignupInline(admin.StackedInline):
    model = UserenaSignup
    max_num = 1
class UserprofileInline(admin.StackedInline):
    model = get_profile_model()
    max_num = 1
class UserenaAdmin(UserAdmin):
    inlines = [UserenaSignupInline, UserprofileInline ]
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff', 'date_joined')
    actions = ['send_sms']
    list_filter = ('groups', 'is_staff')
    actions_on_top = True
    actions_on_bottom = True
    
    def send_sms(self, request, queryset, *arg1, **arg2):
        sms_object = sms()
        for user_object in queryset:
            send_users = ''
            try:
                password = int(random.random() * 100000)
            except:
                password = 123456
            send_users = user_object.get_profile().mobile
            user_object.set_password(password)
            user_object.save()
            send_result = sms_object.post_sms(send_users, u'您的新密码是%s' % password)
            self.message_user(request, send_result)
    send_sms.short_description = u'发送用户密码'
    
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'message_short', 'addtime_format_admin', 'category_name')
    list_display_links = ('id', 'message_short')
    search_fields = ['message']
    list_per_page = 10
    
class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    list_display_links = ('id', 'name', 'code')
    list_per_page = 10

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_per_page = 10
    
admin.site.unregister(User)
admin.site.register(User, UserenaAdmin)
admin.site.register(get_profile_model())
admin.site.register(Note, NoteAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Area, AreaAdmin)
