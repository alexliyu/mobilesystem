#-*- coding:utf-8 -*-
"""
这是地理信息系统的后台注册文件，注册模型到django后台管理界面
创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.contrib.gis import admin
from apps.places.models import (Entity, EntityName, EntityType, EntityTypeName, EntityGroup,
                    EntityGroupName, Route, StopOnRoute, Journey)

class EntityTypeNameInline(admin.TabularInline):
    model = EntityTypeName
    fk_name = "entity_type"


class EntityGroupNameInline(admin.TabularInline):
    model = EntityGroupName
    fk_name = "entity_group"


class EntityNameInline(admin.TabularInline):
    model = EntityName
    fk_name = "entity"


class EntityTypeAdmin(admin.ModelAdmin):
    inlines = [
        EntityTypeNameInline,
    ]


class EntityGroupAdmin(admin.ModelAdmin):
    inlines = [
        EntityGroupNameInline,
    ]


class EntityAdmin(admin.OSMGeoAdmin):
    """
    注册GEO管理模型
    """
    list_display = ('title', 'absolute_url', 'primary_type')
    list_filter = ('source', 'primary_type',)
    map_template = 'gis/admin/google.html'
    openlayers_url = 'http://openlayers.org/dev/OpenLayers.js'
    extra_js = ['http://maps.google.com/maps/api/js?v=3.5&amp;sensor=false']
    inlines = [
        EntityNameInline,
    ]

class StopOnRouteInline(admin.StackedInline):
    model = StopOnRoute
    fk_name = 'route'

class RouteAdmin(admin.ModelAdmin):
    inlines = [
        StopOnRouteInline
    ]
"""
注册后台管理模块
"""
admin.site.register(Entity, EntityAdmin)
admin.site.register(EntityType, EntityTypeAdmin)
admin.site.register(EntityGroup, EntityGroupAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Journey)

