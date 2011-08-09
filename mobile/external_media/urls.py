from django.conf.urls.defaults import *

from external_media.views import IndexView, ExternalImageView

urlpatterns = patterns('',
    (r'^$',
        IndexView, {},
        'index'),

    (r'^external_images/(?P<slug>[0-9a-f]{8})/$',
        ExternalImageView, {},
        'image'),

)
