from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required

from forum import views, accountviews 

urlpatterns = patterns('',
    url(r'^$', views.index, name='forum_index'),
    url(r'^recent/$', views.recent, name='forum_recent'),
    url(r'^forum/(?P<forum_slug>\w+)/$', views.forum, name='forum_forum'),
    url(r'^forum/(?P<forum_slug>\w+)/(?P<topic_type>\w+)/$', views.forum, name='forum_forum_ext'),
    url(r'^forum/(?P<forum_slug>\w+)/(?P<topic_type>\w+)/(?P<topic_type2>\w+)/$',
        views.forum, name='forum_forum_ext2'),
    url('^topic/(?P<topic_id>\d+)/$', views.topic, name='forum_topic'),
    url('^topic/new/(?P<forum_id>\d+)/$', views.new_post, name='forum_new_topic'),
    url('^reply/new/(?P<topic_id>\d+)/$', views.new_post, name='forum_new_replay'),
    url('^post/(?P<post_id>\d+)/$', views.post, name='forum_post'),
    url('^post/(?P<post_id>\d+)/edit/$', views.edit_post, name='forum_post_edit'),
    url('^user/(?P<user_id>\d+)/topics/$', views.user_topics, name='forum_user_topics'),
    url('^user/(?P<user_id>\d+)/posts/$', views.user_posts, name='forum_user_posts'),

    url(r'^lang.js$', direct_to_template, {'template': 'forum/lang.js'}, name='forum_lang_js'),

    url('^markitup_preview/$', views.markitup_preview, name='markitup_preview'),
)

urlpatterns += patterns('',
    url(r'^account/$', login_required(accountviews.profile), name='forum_account_index'),
    url(r'^account/signature/$', accountviews.signature, name='forum_signature'),

    url(r'^user/(?P<user_id>\d+)/$', login_required(accountviews.profile), name='forum_user_profile'),
)

urlpatterns += patterns('simpleavatar.views',
        url('^account/avatar/change/$', 'change', {'template_name': 'forum/account/avatar/change.html'}, \
                name='forum_avatar_change'),

    (r'^accounts/avatar/', include('simpleavatar.urls')),
)
