#-*- coding:utf-8 -*-
"""
这是短信后台管理模型定义文件.

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.contrib import admin

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from sms.models import sms_history, sms_list

from utils.sms import sms




class SmsAdmin(admin.ModelAdmin):
   
    list_display = ('title', 'sms_id', 'stat', 'creat_date')
    actions = ['send_sms']
    actions_on_top = True
    actions_on_bottom = True
    
    def send_sms(self, request, queryset, *arg1, **arg2):
        send_users = ''
        sms_object = sms()
        for sms_item in queryset:
            for user_object in sms_item.sms_users.all():
                try:
                    send_users += user_object.get_profile().mobile + ','
                except:
                    pass
            for group_object in sms_item.sms_groups.all():
                for user_object in group_object.user_set.all():
                    try:
                        send_users += user_object.get_profile().mobile + ','
                    except:
                        pass
            send_result = sms_object.post_sms(send_users, sms_item.content)
            if len(send_result) > 3:
                sms_item.sms_id = send_result
                sms_item.stat = 1
            else:
                sms_item.stat = 3
                sms_item.errors = send_result
            sms_item.save()
            self.message_user(request, send_result)
    send_sms.short_description = u'发送短信'
    
class sms_historyAdmin(admin.ModelAdmin):
    list_display = ('title', 'sms_id', 'stat', 'creat_date')
    search_fields = ['content']
    list_per_page = 10
    

    

admin.site.register(sms_list, SmsAdmin)
admin.site.register(sms_history, sms_historyAdmin)
