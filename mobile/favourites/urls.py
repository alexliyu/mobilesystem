from django.conf.urls.defaults import *

from favourites.views import IndexView

urlpatterns = patterns('',
    (r'^$',
        IndexView, {},
        'index'),
    )
