"""Urls for the entry feeds"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

from ..feeds import LatestEntries
from ..feeds import EntryDiscussions
from ..feeds import EntryComments
from ..feeds import EntryTrackbacks
from ..feeds import EntryPingbacks
from ..feeds import SearchEntries
from ..feeds import TagEntries
from ..feeds import CategoryEntries
from ..feeds import AuthorEntries


urlpatterns = patterns('',
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
                       )
