#-*- coding:utf-8 -*-
"""
这是用于GIS的应用程序，作为系统最核心的应用之一，将会与其他各个应用相关联
创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.utils.translation import ugettext_lazy as _

class Mete:
    """
    定义此应用程序的附加信息，诸如应用程序名
    """
    title = _('Place')

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
