from django.conf.urls.defaults import patterns
from apps.interactive.views import IndexView, InteractiveList, InteractiveDetail, InteractivePost
#info = {
#    'queryset': PromotionsInfo.objects.get(id),
#    'template_name': 'promotionsDetail.html',
#    'template_object_name': 'promotions',
#}
urlpatterns = patterns('',
       (r'^categries/(?P<slug>[\w+]+)/$', InteractiveList, {}, 'interactivelist'),
       (r'^categries/(?P<slug>[\w+]+)/page/(?P<page>\d+)/$', InteractiveList, {}, 'interactivelist_paginated'),
       (r'^detail/(?P<slug>[\w+]+)/$', InteractiveDetail, {}, 'interactivedetail'),
       (r'^post/(?P<slug>[\w+]+)/$', InteractivePost, {}, 'interactivepost'),
#       (r'^pro/(?P<slug>[\d+]+)/$', PromotionsView, {}, 'promotionsView'),
#       (r'^proall/', PromotionsList, {}, 'promotionsView'),
#       (r'^(?P<slug>[\d+]+)/$', BusinessDetail, {}, 'businessDetail'),
       (r'^$', IndexView, {}, 'index'),
       )
