from django.conf.urls.defaults import *

from apps.home.views import StaticDetailView

from apps.places.views import (
    IndexView,
    NearbyListView, NearbyDetailView,
    EntityDetailView,
    EntityUpdateView,

    NearbyEntityListView, NearbyEntityDetailView,
    CategoryListView, CategoryDetailView,
    
    ServiceDetailView,

    APIView,
)

urlpatterns = patterns('',
    (r'^$',
        IndexView, {},
        'index'),

    (r'^nearby/$',
        NearbyListView, {},
        'nearby-list'),
    (r'^nearby/(?P<ptypes>[^/;]+(\;[^/;]+)*)/$',
        NearbyDetailView, {},
        'nearby-detail'),

    (r'^category/$',
        CategoryListView, {},
        'category-list'),
    (r'^category/(?P<ptypes>[^/;]+(\;[^/;]+)*)/$',
        CategoryDetailView, {},
        'category-detail'),

    (r'^(?P<scheme>[^/]+):(?P<value>[^/]+)/$',
        EntityDetailView, {},
        'entity'),
    
    (r'^(?P<scheme>[a-z_\-]+):(?P<value>[^/]+)/service$',
        ServiceDetailView, {},
        'service-detail'),
    
    (r'^(?P<scheme>[^/]+):(?P<value>[^/]+)/nearby/$',
        NearbyEntityListView, {},
        'entity-nearby-list'),
    (r'^(?P<scheme>[^/]+):(?P<value>[^/]+)/nearby/(?P<ptype>[^/]+)/$',
        NearbyEntityDetailView, {},
        'entity-nearby-detail'),

    (r'^(?P<scheme>[a-z_\-]+):(?P<value>[^/]+)/update/$',
        EntityUpdateView, {},
        'entity-update'),

    (r'^openstreetmap/$',
        StaticDetailView,
        {'title':'About OpenStreetMap', 'template':'openstreetmap'},
        'static-openstreetmap'),

    (r'^api/$',
        APIView, {},
        'api'),
)
