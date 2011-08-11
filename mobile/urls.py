from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from conf import applications, all_apps
from apps.business.views import PicDownload
from feeds import LatestEntries, EntryDiscussions, EntryComments, EntryTrackbacks, EntryPingbacks, SearchEntries, TagEntries, CategoryEntries, AuthorEntries
# Admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)), # Admin site
    (r'^comments/', include('django.contrib.comments.urls')), # Django comments
    (r'^accounts/', include('userena.urls')),
    (r'^messages/', include('userena.contrib.umessages.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^sentry/', include('sentry.web.urls')),
    (r'^tracking/', include('tracking.urls')),
    
#    (r'^entry/', include('entry.urls')),
    
    (r'^download/', PicDownload),
     url(r'^latest/$',
                           LatestEntries(),
                           name='entry_entry_latest_feed'),
                       url(r'^search/$',
                           SearchEntries(),
                           name='entry_entry_search_feed'),
                       url(r'^tags/(?P<slug>[- \w]+)/$',
                           TagEntries(),
                           name='entry_tag_feed'),
                       url(r'^authors/(?P<username>[.+-@\w]+)/$',
                           AuthorEntries(),
                           name='entry_author_feed'),
                       url(r'^categories/(?P<path>[-\/\w]+)/$',
                           CategoryEntries(),
                           name='entry_category_feed'),
                       url(r'^discussions/(?P<slug>[-\w]+)/$',
                           EntryDiscussions(),
                           name='entry_entry_discussion_feed'),
                       url(r'^comments/(?P<slug>[-\w]+)/$',
                           EntryComments(),
                           name='entry_entry_comment_feed'),
                       url(r'^pingbacks/(?P<slug>[-\w]+)/$',
                           EntryPingbacks(),
                           name='entry_entry_pingback_feed'),
                       url(r'^trackbacks/(?P<slug>[-\w]+)/$',
                           EntryTrackbacks(),
                           name='entry_entry_trackback_feed'),
    (r'', applications.home.urls)) # Home default

# Dynamically add apps
for app in (app for app in all_apps() if app.has_urlconf and app.local_name != 'home'):
    urlpatterns += patterns('',
        (r'^' + app.local_name + '/', include(app.urls)))

# Redirecting old URLs
urlpatterns += patterns('django.views.generic.simple',
    (r'^maps/busstop:(?P<atco>[A-Z\d]+)/(?P<remain>.*)$', 'redirect_to', {'url': '/places/atco:%(atco)s/%(remain)s'}),
    (r'^maps/[a-z]\-+:(?P<id>\d{8})/(?P<remain>.*)$', 'redirect_to', {'url': '/places/oxpoints:%(id)s/%(remain)s'}),
    (r'^maps/[a-z]\-+:(?P<id>[NW]\d{8})/(?P<remain>.*)$', 'redirect_to', {'url': '/places/osm:%(id)s/%(remain)s'}),
    (r'^maps/(?P<remain>.*)$', 'redirect_to', {'url': '/places/%(remain)s'}),
    (r'^osm/(?P<remain>.*)$', 'redirect_to', {'url': '/maps/osm/%(remain)s'}),
)


handler500 = 'utils.views.handler500'

urlpatterns += patterns('simpleavatar.views',
        url('^account/avatar/change/$', 'change', {'template_name': 'forum/account/avatar/change.html'}, \
                name='forum_avatar_change'),

    (r'^accounts/avatar/', include('simpleavatar.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT})
    )
