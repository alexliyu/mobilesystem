from django.conf.urls.defaults import *

from geolocation.views import IndexView, ClearHistoryView, FavouritesView

urlpatterns = patterns('',
    (r'^$',
        IndexView, {},
        'index'),

    (r'^clear/$',
        ClearHistoryView, {},
        'clear'),

    (r'^favourites/$',
        FavouritesView, {},
        'favourites'),

)
    
