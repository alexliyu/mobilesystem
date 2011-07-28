from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required

from forum.accountviews import profile, signature 

from .views import IndexView, forum, recent, topic, post, new_post, edit_post, user_posts, user_topics, markitup_preview
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
   (r'^$', IndexView, {}, 'index'),
   (r'^recent/$', recent, {}, 'forum_recent'),
   (r'^(?P<forum_slug>\w+)/$', forum, {}, 'forum_forum'),
   (r'^(?P<forum_slug>\w+)/(?P<topic_type>\w+)/$', forum, {}, 'forum_forum_ext'),
   (r'^(?P<forum_slug>\w+)/(?P<topic_type>\w+)/(?P<topic_type2>\w+)/$', forum, {}, 'forum_forum_ext2'),
   ('^forum/topic/(?P<topic_id>\d+)/$', topic, {}, 'forum_topic'),
   ('^forum/topic/new/(?P<forum_id>\d+)/$', new_post, {}, 'forum_new_topic'),
   ('^reply/new/(?P<topic_id>\d+)/$', new_post, {}, 'forum_new_replay'),
   ('^post/(?P<post_id>\d+)/$', post, {}, 'forum_post'),
   ('^post/(?P<post_id>\d+)/edit/$', edit_post, {}, 'forum_post_edit'),
   ('^user/(?P<user_id>\d+)/topics/$', user_topics, {}, 'forum_user_topics'),
   ('^user/(?P<user_id>\d+)/posts/$', user_posts, {}, 'forum_user_posts'),
)

urlpatterns += patterns('',
    url(r'^account/$', profile, {}, 'forum_account_index'),
    url(r'^account/signature/$', signature, {}, 'forum_signature'),

    url(r'^user/(?P<user_id>\d+)/$', profile, {}, 'forum_user_profile'),
)
