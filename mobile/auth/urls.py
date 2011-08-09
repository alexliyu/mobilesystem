from django.conf.urls.defaults import *

from auth.views import IndexView, ClearSessionView

urlpatterns = patterns('',
    (r'^$',
        IndexView, {},
        'index'),
        
    (r'^clear-session/$',
        ClearSessionView, {},
        'clear-session'),
)
