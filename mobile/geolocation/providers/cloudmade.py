#-*- coding:utf-8 -*-
"""
这是项目的基本配置文件.

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050

@param DEBUG 是否开启调试模式

@param TEMPLATE_DEBUG 是否开启模板调试模式

@event event 无事件

@exception exception 无返回

@keyparam  param 无参数

@return 无返回
       
"""
import urllib, urllib2, logging

import simplejson

from django.conf import settings
from django.contrib.gis.gdal.datasource import OGRException
from django.contrib.gis.geos import Point

from geolocation.providers import BaseGeolocationProvider
from utils.geopy import geocoders
logger = logging.getLogger(__name__)

class CloudmadeGeolocationProvider(BaseGeolocationProvider):
    REVERSE_GEOCODE_URL = 'http://geocoding.cloudmade.com/%(api_key)s/geocoding/closest/%(type)s/%(lat)f,%(lon)f.js'
    GEOCODE_URL = 'http://maps.google.com/maps/api/geocode/json?address=%(query)s&sensor=false'

    def __init__(self, search_locality=None):
        self.search_locality = search_locality

    def reverse_geocode(self, lon, lat):

        params = {
            'api_key': settings.API_KEYS['cloudmade'],
            'lon': lon,
            'lat': lat,
            'type': 'road',
        }

        try:
            request_url = self.REVERSE_GEOCODE_URL % params
            response = urllib2.urlopen(request_url)
            if response.code != 200:
                logger.error("Request to %s returned response code %d" % (request_url, response.code))
                return []
            json = simplejson.loads(response.read().replace('&apos;', "'"), 'utf8')
        except urllib2.HTTPError, e:
            logger.error("Cloudmade returned a non-OK response code %d", e.code)
            return []
        except urllib2.URLError, e:
            logger.error("Encountered an error reaching Cloudmade: %s", str(e))
            return []
        
        if not json:
            return []
        
        else:
            name = json['features'][0]['properties'].get('name')
            try:
                params['type'] = 'area'
                data = simplejson.load(urllib2.urlopen(self.REVERSE_GEOCODE_URL % params))
                name = '%s, %s' % (name, data['features'][0]['properties']['name'])
            except Exception:
                pass
            return [{
                'name': json['features'][0]['properties'].get('name'),
                'location': (lon, lat),
                'accuracy': 100,
            }]

    def geocode(self, query):
        
        if not query:
            return []
        
        if self.search_locality and not (', ' in query or ' near ' in query):
            query += ', %s' % self.search_locality

        params = {
            'query': query,
        }
        """
        调用google map 定位
        """
        g = geocoders.Google(output_format='json')
        json = g.geocode(params.get('query'), exactly_one=False)
        if not json:
            return []

        results = []
        
        for feature in json:
            try:
                # Cloudmade returns a lat-long (and we use long-lats internally)
                bounds_a, bounds_b = Point(feature[1][1], feature[1][0], srid=4326).transform(settings.SRID, clone=True)
            except OGRException:
                # The point wasn't transformable into the co-ordinate
                # scheme desired - it's probably a long way away.
                continue

            centroid = feature[1][1], feature[1][0]
#            accuracy = bounds_a.distance(bounds_b) / 1.414
            accuracy = 100
            
            try:
                name = feature[0]
                if name == self.search_locality and name.lower() != query.split(',')[0].lower():
                    continue

#                try:
#                    params.update({
#                        'type': 'area',
#                        'lat': centroid[1],
#                        'lon': centroid[0],
#                    })
#                    data = simplejson.load(urllib2.urlopen(self.REVERSE_GEOCODE_URL % params))
#                    if name != data['features'][0]['properties']['name']:
#                        name = '%s, %s' % (name, data['features'][0]['properties']['name'])
#                except Exception:
#                    pass
                    
                results.append({
                    'name': name,
                    'location': centroid,
                    'accuracy': accuracy,
                })
                    
                
            except KeyError:
                results += self.reverse_geocode(*centroid)

        return results
