from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^$',IndexView, {},'index'),
    (r'^(\d+)/$',DetailsView,{},'details'),
)
