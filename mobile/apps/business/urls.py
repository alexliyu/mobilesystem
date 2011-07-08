from django.conf.urls.defaults import patterns
from mobile.apps.business.views import PromotionsView, \
    PromotionsDetail, PromotionsList, BusinessList, BusinessDetail

#info = {
#    'queryset': PromotionsInfo.objects.get(id),
#    'template_name': 'promotionsDetail.html',
#    'template_object_name': 'promotions',
#}
urlpatterns = patterns('',
       (r'^detail/(?P<slug>[\d+]+)/$', PromotionsDetail, {}, 'promotionsDetail'),
       (r'^pro/(?P<slug>[\d+]+)/$', PromotionsView, {}, 'promotionsView'),
       (r'^proall/', PromotionsList, {}, 'promotionsView'),
       (r'^(?P<slug>[\d+]+)/$', BusinessDetail, {}, 'businessDetail'),
       (r'^$', BusinessList, {}, 'index'),
       )
