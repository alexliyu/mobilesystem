from django.conf.urls.defaults import *

from .views import IndexView, ItemListView, ItemDetailView, TypeView

urlpatterns = patterns('',
   (r'^$', IndexView, {}, 'index'),
   (r'^(?P<path>[-\w]+)/$', TypeView, {}, 'type-list'),
  
   (r'^(?P<path>[-\w]+)/(?P<slug>[-\w]+)/$', ItemListView, {}, 'item-list'),
   (r'^(?P<path>[-\w]+)/(?P<slug>[-\w]+)/(?P<id>\d+)/$', ItemDetailView, {}, 'item-detail'),
)
