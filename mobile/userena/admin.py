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

from userena.models import UserenaSignup, Note, Category, Area
from userena.utils import get_profile_model
from mobile.utils.sms import sms



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
    actions_on_top = True
    actions_on_bottom = True
    
    def send_sms(self, request, queryset, *arg1, **arg2):
        send_users = ''
        sms_object = sms()
        for user in queryset:
            send_users += user.get_profile().mobile + ','
        send_result = sms_object.post_sms(send_users, u'这是一条测试短信，请收到短信的同事，反馈给李昱，同时报上各位的手机运营商，以便于我统计哪些手机运营商接收不到短信')
        self.message_user(request, send_result)
    send_sms.short_description = u'发送测试短信'
    
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
