from django.conf.urls.defaults import *

from wurfl.views import IndexView

urlpatterns = patterns('',
    (r'^$', IndexView, {}, 'index'),
)

