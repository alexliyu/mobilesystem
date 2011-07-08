from django.conf.urls.defaults import *

import mobile.maps.osm.urls

from views import IndexView, TouchMapLiteView

urlpatterns = patterns('',
        (r'^$', IndexView, {}, 'index'),
        (r'^touchmaplite/$', TouchMapLiteView, {}, 'touchmaplite'),
        (r'^osm/', include(mobile.maps.osm.urls.urlpatterns)),
    )