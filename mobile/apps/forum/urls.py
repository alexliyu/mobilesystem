from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


from apps.forum.accountviews import profile, signature 

from .views import IndexView, forum, recent, topic, post, new_post, edit_post, user_posts, user_topics, markitup_preview


urlpatterns = patterns('',
   url(r'^user/(?P<user_id>\d+)/topics/$', user_topics, {}, 'forum_user_topics'),
   url(r'^user/(?P<user_id>\d+)/posts/$', user_posts, {}, 'forum_user_posts'),
   (r'^$', IndexView, {}, 'index'),
   (r'^recent/$', recent, {}, 'forum_recent'),
   ('^topic/(?P<topic_id>\d+)/$', topic, {}, 'forum_topic'),
   ('^topic/new/(?P<forum_id>\d+)/$', new_post, {}, 'forum_new_topic'),
   ('^reply/new/(?P<topic_id>\d+)/$', new_post, {}, 'forum_new_replay'),
   
   url(r'^account/$', profile, {}, 'forum_account_index'),
   url(r'^account/signature/$', signature, {}, 'forum_signature'),
   
  
   (r'^(?P<forum_slug>\w+)/(?P<topic_type>\w+)/$', forum, {}, 'forum_forum_ext'),
   (r'^(?P<forum_slug>\w+)/(?P<topic_type>\w+)/(?P<topic_type2>\w+)/$', forum, {}, 'forum_forum_ext2'),
   (r'^(?P<forum_slug>\w+)/$', forum, {}, 'forum_forum'),
   
 
  
   ('^post/(?P<post_id>\d+)/edit/$', edit_post, {}, 'forum_post_edit'),
   ('^post/(?P<post_id>\d+)/$', post, {}, 'forum_post'),
)

urlpatterns += patterns('',
     #url(r'^user/(?P<user_id>\d+)/$', profile, {}, 'forum_user_profile'),
    
)
