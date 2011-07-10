from django.conf.urls.defaults import *

import maps.osm.urls

from maps.views import IndexView, TouchMapLiteView

urlpatterns = patterns('',
        (r'^$', IndexView, {}, 'index'),
        (r'^touchmaplite/$', TouchMapLiteView, {}, 'touchmaplite'),
        (r'^osm/', include(maps.osm.urls.urlpatterns)),
    )
