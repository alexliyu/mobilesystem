#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
import re, urllib, random, email
import urllib2
from datetime import datetime, tzinfo, timedelta
from xml.etree import ElementTree as ET

from django.contrib.gis.geos import Point

from conf.settings import batch

from apps.weather.models import (
    Weather, OUTLOOK_CHOICES, VISIBILITY_CHOICES, PRESSURE_STATE_CHOICES,
    SCALE_CHOICES
)

class BBCWeatherProvider(object):
    def __init__(self):
        self.location_id = '厦门'

    @staticmethod
    def _find_choice_match(choices, verbose):
        matches = [a for a, b in choices if (verbose or '').lower() == b]
        if len(matches) == 1:
            return matches[0]
        else:
            return None

    _OBSERVATIONS_URL = 'http://www.webxml.com.cn/webservices/weatherwebservice.asmx/getWeatherbyCityName?theCityName=%s'
    

    @batch('* */4 * * *')
    def import_data(self, metadata, output):
        """存储天气信息"""

        observations = self.get_observations_data()
        
        weathers = [(
            Weather.objects.create(location_id=self.location_id, name=self.location_id), observations
        )]


        VERBATIM = (
            'temperature', 'wind_speed', 'humidity', 'pressure',
            'wind_direction', 'sunset', 'sunrise', 'observed_date',
            'published_date', 'name', 'min_temperature', 'max_temperature',
        )
        LOOKUP = (
            ('outlook', OUTLOOK_CHOICES),
            ('outlook_1', OUTLOOK_CHOICES),
            ('outlook_2', OUTLOOK_CHOICES),
        )

        for weather, data in weathers:
            for k, l in LOOKUP:
                if k in data:
                    setattr(weather, k, self._find_choice_match(l, data[k]))
                    
            weather.published_date = data['published_date']
            weather.observed_date = data['observed_date']
            weather.temperature = data['temperature']
            weather.temperature_content = data['temperature_content']
            weather.description = data['description']
            weather.temperature_1 = data['temperature_1']
            weather.temperature_2 = data['temperature_2']

            weather.save()
        return metadata

    def get_observations_data(self):
        """获取天气xml"""
        request = urllib2.Request(self._OBSERVATIONS_URL % self.location_id)
        response = urllib2.urlopen(request)
        
        xml = ET.parse(response)
        tmpdata = xml.findall('.//')
        
        """处理xml数据格式"""
        
        data = {
              'outlook':tmpdata[6].text.split(' ')[1],
              'published_date':tmpdata[4].text,
              'observed_date':tmpdata[6].text.split(' ')[0],
              'temperature':tmpdata[5].text,
              'temperature_content':tmpdata[10].text,
              'description':tmpdata[11].text,
              'outlook_1':tmpdata[13].text.split(' ')[1],
              'temperature_1':tmpdata[12].text,
              'outlook_2':tmpdata[18].text.split(' ')[1],
              'temperature_2':tmpdata[17].text,
              
              
              }
        
        
        return data

    
