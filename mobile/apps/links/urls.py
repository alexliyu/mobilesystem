from django.conf.urls.defaults import *

from apps.links.views import IndexView


urlpatterns = patterns('',
    (r'^$',
        IndexView, {},
        'index'),
    )
