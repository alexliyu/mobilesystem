from django.conf.urls.defaults import *

from apps.weather.views import IndexView

urlpatterns = patterns('',
    (r'^$', IndexView, {}, 'index'),
)

