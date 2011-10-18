#-*- coding:utf-8 -*-
"""
这是短信后台管理模型定义文件.

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.contrib import admin

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from sms.models import sms_history, sms_list, sms_entry, sms_time_list

from mobile.utils.smsutils import sms




class SmsAdmin(admin.ModelAdmin):
   
    list_display = ('title', 'sms_id', 'stat', 'creat_date')
    actions = ['send_sms']
    actions_on_top = True
    actions_on_bottom = True
    
    def send_sms(self, request, queryset, *arg1, **arg2):
        send_users = ''
        sms_object = sms()
        errors = ''
        stat = 0
        for sms_item in queryset:
            for user_object in sms_item.sms_users.all():
                try:
                    send_users += user_object.get_profile().mobile + ','
                except Exception, e:
                    stat = 4
                    errors += e.message
                    
            for group_object in sms_item.sms_groups.all():
                for user_object in group_object.user_set.all():
                    try:
                        send_users += user_object.get_profile().mobile + ','
                    except Exception, e:
                        stat = 4
                        errors += e.message
            send_result = str(sms_object.post_sms(u'批量群发短信', send_users, sms_item.content))
            if len(send_result) > 3:
                sms_item.sms_id = send_result
                stat = 1
            else:
                stat = 3
                errors += send_result
            sms_item.stat = stat
            sms_item.errors = errors
            sms_item.save(force_update=True)
            self.message_user(request, send_result)
    send_sms.short_description = u'发送短信'
    
class sms_historyAdmin(admin.ModelAdmin):
    list_display = ('title', 'sms_id', 'send_type', 'stat', 'creat_date')
    search_fields = ['content']
    list_per_page = 10
    
class sms_entryAdmin(admin.ModelAdmin):
    list_display = ('title', 'stat', 'creat_date')
    search_fields = ['content']
    list_per_page = 10
    
class sms_time_listAdmin(admin.ModelAdmin):
    list_display = ('title', 'sms_id', 'stat', 'creat_date')
    search_fields = ['content']
    list_per_page = 10
    
admin.site.register(sms_time_list, sms_time_listAdmin)
admin.site.register(sms_entry, sms_entryAdmin)
admin.site.register(sms_list, SmsAdmin)
admin.site.register(sms_history, sms_historyAdmin)
