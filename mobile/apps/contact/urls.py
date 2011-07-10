from django.conf.urls.defaults import *

from apps.contact.views import IndexView, ResultListView, ResultDetailView

urlpatterns = patterns('',
    (r'^$', IndexView, {}, 'index'),
    (r'^results/$', ResultListView, {}, 'result_list'),
    (r'^results/(?P<id>[^\/]+)/$', ResultDetailView, {}, 'result_detail'),
)
