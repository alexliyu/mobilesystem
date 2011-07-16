from django.conf.urls.defaults import *
from apps.news.views import *

urlpatterns = patterns('',
    (r'^$', IndexView, {}, 'index'),
)
