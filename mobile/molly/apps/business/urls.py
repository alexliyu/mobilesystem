from django.conf.urls.defaults import patterns
from mobile.molly.apps.business.views import PromotionsView,IndexView,\
    PromotionsDetail

#info = {
#    'queryset': PromotionsInfo.objects.get(id),
#    'template_name': 'promotionsDetail.html',
#    'template_object_name': 'promotions',
#}
urlpatterns = patterns('',
       (r'^(?P<slug>[\d+]+)/$', PromotionsDetail,{},'promotionsDetail'),
       (r'^pro/(?P<slug>[\d+]+)/$', PromotionsView, {},'promotionsView'),
       (r'^$', IndexView, {},'index'),
       )