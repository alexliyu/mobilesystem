#-*- coding:utf-8 -*-
"""
这是地图应用程序，用于管理及显示地图

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from email.utils import formatdate
from datetime import datetime, timedelta
from time import mktime
import simplejson, urllib2, base64
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404

from baseutils.views import BaseView
from baseutils.breadcrumbs import *
from baseutils.misc import AnyMethodRequest

from apps.places.models import Entity

from .models import GeneratedMap

class GeneratedMapView(BaseView):
    breadcrumb = NullBreadcrumb

    def handle_GET(self, request, context, hash):
        gm = get_object_or_404(GeneratedMap, hash=hash)
        response = HttpResponse(open(gm.get_filename(), 'r').read(), mimetype='image/png')

        response['Expires'] = formatdate(mktime((datetime.now() + timedelta(days=7)).timetuple()))
        response['Last-Modified'] = formatdate(mktime(gm.generated.timetuple()))
        response['ETag'] = hash
        return response

class AboutView(BaseView):

    @BreadcrumbFactory
    def breadcrumb(self, request, context):
        return Breadcrumb(
            self.conf.local_name,
            None,
            u'关于娱讯地图',
            lazy_reverse('maps:osm-about'),
        )

    def handle_GET(self, request, context):
        return self.render(request, context, 'maps/osm/about')

class GPXView(BaseView):
    breadcrumb = NullBreadcrumb

    def handle_GET(self, request, context, ptype):
        out = []
        out.append('<?xml version="1.0"?>\n')
        out.append('<gpx version="1.0"')
        out.append(' creator="E2-Mobile &lt;http://2go3.com/&gt;"')
        out.append(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        out.append(' xmlns="http://www.topografix.com/GPX/1/0"')
        out.append(' xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">\n')

        for entity in Entity.objects.filter(primary_type__slug=ptype, source__module_name='providers.apps.maps.osm'):
            out.append('  <wpt lat="%(lat)f" lon="%(lon)f">\n' % {'lat':entity.location[1], 'lon':entity.location[0]})
            out.append('    <name>%s</name>\n' % entity.title)
            out.append('  </wpt>\n')

        out.append('</gpx>')

        return HttpResponse(out, mimetype="application/gpx+xml")

