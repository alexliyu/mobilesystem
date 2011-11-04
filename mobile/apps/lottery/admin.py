#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from django.contrib import admin
from apps.lottery.models import *
from apps.lottery.forms import Lottery_listAdminForm
from baseutils.smsutils  import sms

class lotteryAdmin(admin.ModelAdmin):
   
    list_display = ('lottery_title', 'addTime')
    actions = ['send_sms']
    actions_on_top = True
    actions_on_bottom = True
    form = Lottery_listAdminForm
    
    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site
        super(lotteryAdmin, self).__init__(model, admin_site)
    
    def send_sms(self, request, queryset, *arg1, **arg2):
        send_users = ''
        sms_object = sms()
        for sms_item in queryset:
            for user_object in sms_item.UserProfile.all():
                try:
                    send_users += user_object.mobile + ','
                except:
                    send_users += user_object.user.username + ','
            send_result = sms_object.post_sms(u'抽奖中奖通知短信', send_users, sms_item.sms_content)
            
            self.message_user(request, send_result)
    send_sms.short_description = u'发送短信'

admin.site.register(lottery, lotteryAdmin)
