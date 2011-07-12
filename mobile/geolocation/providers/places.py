#-*- coding:utf-8 -*-
"""
这是用于查询GIS地理位置的provider之一，用于检索数据库中所保存的地理位置.

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050

       
"""

import logging
from itertools import chain

import simplejson

from geolocation.providers import BaseGeolocationProvider
from apps.places.models import Entity, EntityName

logger = logging.getLogger(__name__)

class PlacesGeolocationProvider(BaseGeolocationProvider):
    def __init__(self, search_identifiers=None):
        self.search_identifiers = search_identifiers

    def geocode(self, query):
        entities = Entity.objects.all()
        if self.search_identifiers:
            entities = entities.filter(
                _identifiers__scheme__in=self.search_identifiers,
                _identifiers__value__iexact=query,
            )
        else:
            """
            2011-07-13 修正查找GIS地点时全部匹配查询为部分匹配查询
            """
            entities = entities.filter(
                _identifiers__value__icontains=query,
            )

        entities = chain(
            Entity.objects.filter(names__title__icontains=query,
                                  location__isnull=False),
            entities,
        )

        for entity in entities:
            yield {
                'name': entity.title,
                'location': tuple(entity.location),
                'accuracy': 100,
            }
