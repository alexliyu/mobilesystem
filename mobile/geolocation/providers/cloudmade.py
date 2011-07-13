import urllib, urllib2, logging

import simplejson

from django.conf import settings
from django.contrib.gis.gdal.datasource import OGRException
from django.contrib.gis.geos import Point

from geolocation.providers import BaseGeolocationProvider

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

        query = query.strip()
        if query.split(' ')[0][0].isdigit():
            query = ' '.join(query.split(' ')[1:])

        params = {
            'query': urllib.quote_plus(str(query)),
        }

        try:
            request_url = self.GEOCODE_URL % params
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

        results = []
        
        features = [{
                  'address_components':json['results'][0]['address_components'],
                  'bounds':json['results'][0]['geometry']['bounds']['northeast'],
                  'location':json['results'][0]['geometry']['location']
                  
                  }]       
        
        for i, feature in enumerate(features):
            try:
                # Cloudmade returns a lat-long (and we use long-lats internally)
                bounds_a, bounds_b = Point(feature['bounds']['lng'], feature['bounds']['lat'], srid=4326).transform(settings.SRID, clone=True)
            except OGRException:
                # The point wasn't transformable into the co-ordinate
                # scheme desired - it's probably a long way away.
                continue

            centroid = tuple(feature['location']['lng'], feature['location']['lat'])
            centroid = centroid[1], centroid[0]
            accuracy = bounds_a.distance(bounds_b) / 1.414
            
            try:
                name = feature['address_components']['formatted_address']
                if name == self.search_locality and name.lower() != query.split(',')[0].lower():
                    continue

                try:
                    if i > 0:
                        raise ValueError
                    params.update({
                        'type': 'area',
                        'lat': centroid[1],
                        'lon': centroid[0],
                    })
                    data = simplejson.load(urllib2.urlopen(self.REVERSE_GEOCODE_URL % params))
                    if name != data['features'][0]['properties']['name']:
                        name = '%s, %s' % (name, data['features'][0]['properties']['name'])
                except Exception:
                    pass
                    
                results.append({
                    'name': name,
                    'location': centroid,
                    'accuracy': accuracy,
                })
                    
                
            except KeyError:
                results += self.reverse_geocode(*centroid)

        return results
