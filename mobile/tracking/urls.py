from django.conf.urls.defaults import *
from django.conf import settings
from mobile.tracking import views

urlpatterns = patterns('',
    url(r'^refresh/$', views.update_active_users, name='tracking-refresh-active-users'),
    url(r'^refresh/json/$', views.get_active_users, name='tracking-get-active-users'),
    url(r'^map/$', views.display_map, name='tracking-visitor-map'),
)


