from django.conf.urls.defaults import *

from url_shortener.views import IndexView

urlpatterns = patterns('',
    (r'^$',
        IndexView, {},
        'index'),
)
