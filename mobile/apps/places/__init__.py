#-*- coding:utf-8 -*-
"""
这是地理信息系统的初始化类，用于生成公共方法
创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050

@param DEBUG 是否开启调试模式

@param TEMPLATE_DEBUG 是否开启模板调试模式

@event event 无事件

@exception exception 无返回

@keyparam  param 无参数

@return 无返回
       
"""
from math import atan2, degrees
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import Point

from apps.places.models import EntityType, Entity, Identifier

def get_entity(scheme, value):
    """
    2011-07-09修复，用scheme:value这样的值来匹配entity，或者地图实例
    """
    return get_object_or_404(Entity, identifier_scheme=scheme, identifier_value=value)
class EntityCache(dict):
    
    def __missing__(self, key):
        scheme, value = key.split(':')
        self[key] = get_entity(scheme, value)
        return self[key]

def get_point(request, entity):
    if entity and entity.location:
        point = entity.location
    elif entity and not entity.location:
        point = None
    elif request.session.get('geolocation:location'):
        point = Point(request.session.get('geolocation:location'), srid=4326)
    else:
        point = None
    return point
