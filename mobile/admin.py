#-*- coding:utf-8 -*-
"""
这是项目的基本管理类，主要用于通过后台管理APPS.

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050

"""
from models import Apps
from django.contrib import admin

#def active_apps(modeladmin, request, queryset):
#    def run(batches):
#        for batch in batches:
#            batch.run()
#            
#    for batch in queryset:
#        if not batch.currently_running:
#            batch.pending = True
#            batch.save()
#        thread = threading.Thread(target=run, args=[(batch,)])
#        thread.daemon = True
#        thread.start()
#active_apps.short__description = "激活插件"

class AppsAdmin(admin.ModelAdmin):
    """
    插件模型的管理类，用来管理插件
    """
    list_display = ['name', 'namespace', 'slug', 'create_date', 'active']
    ordering = ['name']
    #actions = [active_apps]

admin.site.register(Apps, AppsAdmin)
