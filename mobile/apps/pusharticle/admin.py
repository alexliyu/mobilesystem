#-*- coding:utf-8 -*-
'''
Created on 2011-10-19

@author: alex
'''
from django.contrib import admin
from apps.pusharticle.models import PushList, PushResult


class PushListAdmin(admin.ModelAdmin):
    '''
    用于管理推送列表
    '''
    actions = ['testPush']
    actions_on_top = True
    actions_on_bottom = True
    
    list_filter = ('category', 'pushurl', 'is_active')
    list_display = ('name', 'pushurl', 'category', 'latest', 'last_retrieved', 'pushtime', 'is_active')
    
    def testPush(self, request, queryset, *arg1, **arg2):
                #for image in queryset:
                pass
            

class PushResultAdmin(admin.ModelAdmin):
    '''
    用于管理推送结果列表
    '''
    actions_on_top = True
    actions_on_bottom = True
    
    list_filter = ('push_stat', 'push_name')
    list_display = ('title', 'push_name', 'push_stat', 'push_date')
    
                        

admin.site.register(PushResult, PushResultAdmin)
admin.site.register(PushList, PushListAdmin)
