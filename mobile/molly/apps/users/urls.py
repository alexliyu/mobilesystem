from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from mobile.molly.apps.users.views import IndexView


urlpatterns = patterns('',
   (r'^convert/$',
       IndexView, {},
       'index'),
   )
