from django.conf.urls.defaults import *

from mobile.molly.apps.home.views import (
    IndexView, UserMessageView,
    StaticDetailView,
)

urlpatterns = patterns('',

    (r'^$',
        IndexView, {},
        'index'),
    
    (r'^about/$',
        StaticDetailView,
        {'title':'About', 'template':'about'},
        'static_about'),

    (r'^messages/$',
        UserMessageView, {},
        'messages'),
        
)
