from django.conf.urls.defaults import *
from apps.lottery.views import *

urlpatterns = patterns('',
    (r'^$', IndexView, {}, 'index'),
    (r'^(\d+)/$', DetailsView, {}, 'details'),
)
