#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from datetime import datetime, timedelta
from django.utils.log import logging
from django.forms import Media
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.utils.text import truncate_words
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, NoReverseMatch

from tagging.models import Tag

from lincdm import settings
from lincdm.managers import HIDDEN
from lincdm.managers import PUBLISHED
from lincdm.entry.admin.forms import EntryAdminForm
from lincdm.app.fetchblog.feedstest import getpage
from lincdm.app.fetchblog.models import FeedList, FeedsResult, TempImages
import feedparser, os
from lincdm.lib import htmllib
from lincdm.lib.htmllib import HTMLStripper, gbtools
from lincdm.entry.models import Entry, EntryAbstractClass



'''
用于管理采集文章
'''
class TempImagesAdmin(admin.ModelAdmin):
    actions = ['getImages']
    actions_on_top = True
    actions_on_bottom = True
    
    def getImages(self, request, queryset, *arg1, **arg2):
                for image in queryset:
                        logging.info('start to fetch images,The url is %s', image.oldurl)
                        try:
                                name = htmllib.sid() + '.jpg'
                                result = getpage(htmllib.encoding(image.oldurl), 30)
                                if result.code == 200:
                                        result = self.__store_images(result.read(), name, image)
                                else:
                                        result = False
                                if result:
                                        logging.info('Success!')
                                else:
                                        logging.info('this one was Fail!')

                        except Exception, data:
                                logging.info(data)
    getImages.short_description = u'采集图片'
    
    def __saveImages(self, name, image):
        try:
            path = os.path.join(settings.MEDIA_ROOT, 'cache/%s' % name)
            f = file(path, "wb")
            f.write(image)
            f.close()
            return "%scache/%s" % (settings.MEDIA_URL, name)
        except Exception, e:
            logging.error(e)
            return False
        
    def __store_images(self, content, name, model):
                try:
                        #media = model.get_or_create(pk=model.pk)
                        #media.mtype, media.width, media.height = htmllib.getImageInfo(content)
                        model.newurl = self.__saveImages(name, content)
                        model.stat = 1
                        model.save()
                        return True


                except Exception, data:
                        model.stat = 2
                        logging.error('the db saved error is: %s', data)
        
'''
用于管理采集文章
'''
class FeedsRresultAdmin(admin.ModelAdmin):
    actions = ['getArticle', 'getFeed', 'saveArticle' ]
    actions_on_top = True
    actions_on_bottom = True
    
    def getArticle(self, request, queryset, *arg1, **arg2):
                for feed in queryset:
                        logging.info('start to fetch article,The title is %s', feed.title)
                        try:
                                if feed.feed.start_target != 'nohtml':

                                        logging.info('fetch new article %s,at %s' % (feed.link, datetime.now()))
                                        contenthtml = ''
                                        try:
                                                result = getpage(feed.link, 30)
                                                if result.code == 200:
                                                        if len(feed.feed.start_target) != 0 and feed.feed.start_target != 'nohtml':
                                                                contenthtml = htmllib.parsehtml(result.read(), feed.feed, feed.link, feed.feed.feedurl)
                                                        else:
                                                                contenthtml = feed.excerpt
                        
                                                        self.__store_article(contenthtml, feed)
                        
                                                        return True
                                                return False
                                        except Exception, data:
                                                logging.info('DownloadError in get %s.the error is %s', feed.link, data)
                                                return False
                                else:
                                    self.__store_article(feed.excerpt, feed)
                        except Exception, data:
                                logging.error('the rpc error is %s ', data)

    getArticle.short_description = u'采集正文内容'

    def __store_article(self, contenthtml, feed):
        entry = FeedsResult.objects.get(pk=feed.pk)
        try:

            entry.content = htmllib.decoding(contenthtml)
            entry.fetch_stat = 1
            images = htmllib.Parse_images_url(contenthtml)
            for image in images:
                    obj, result = TempImages.objects.get_or_create(oldurl=image, entry=entry)
        except Exception, data:
                        entry.fetch_stat = 2
                        logging.info('the db saved error is: %s', data)
        entry.save()
        logging.info('adding the article,the name is %s', feed.title)

    def saveArticle(self, request, queryset, *arg1, **arg2):
        for entry in queryset:
            result = self.__store_entry(entry)
            
    saveArticle.short_description = u'发布采集'
    def __store_entry(self, feed):
                try:
                    entry, result = Entry.published.get_or_create(title=feed.title)
                    entry.excerpt = feed.excerpt
                    entry.status = 2
                    entry.author_name = feed.author_name
                    entry.date = feed.date
                    entry.slug = htmllib.sid() 
                    entry.content = self.__Parse_image(feed.content)
                    entry.categories.add(feed.feed.category)                   
                    entry.save()
                    feed.fetch_stat = 4
                    feed.save()
                except Exception, data:
                        logging.error('the db saved error is: %s', data)
                        feed.fetch_stat = 3
                        feed.save()

                logging.info('adding the article,the name is %s', feed.title)

    def __Parse_image(self, content):
                images = htmllib.Parse_images_url(content)

                if images:
                    try:
                        for image in images:
                                tmpimage = TempImages.objects.get(oldurl=image)
                                if tmpimage != None:
                                        content = gbtools.stringQ2B(content)
                                        content = htmllib.decoding(content).replace(image, tmpimage.newurl)

                    except Exception, data:
                        logging.info(data)
                return content

'''
用于管理采集列表
'''
class FeedAdmin(admin.ModelAdmin):
    actions = ['test_feed', 'getFeed' ]
    actions_on_top = True
    actions_on_bottom = True
    
    
    # Custom Actions
    def test_feed(self, request, queryset):
        """Set the entries to the user"""
        for feed in queryset:
            result = getpage(feed.feedurl, 30)
            if result.code == 200:
                self.message_user(request, "测试成功！")
            else:
                self.message_user(request, "测试失败！")
    test_feed.short_description = u'测试采集订阅'
    
    '''
    获取Feed订阅内容
    '''
    def getFeed(self, request, queryset, *arg1, **arg2):
                logging.info(u'开始采集Feed')
                feed_retrieval_deadline = datetime.now() - timedelta(minutes=1200)
                
                for feed in queryset:

                    if feed.last_retrieved > feed_retrieval_deadline:
                            logging.info('Skipping feed %s.', feed.feedurl)
                            continue

                    logging.info('Getting feed %s.', feed.feedurl)
                    try:

                            result = getpage(feed.feedurl, 30)
                    except Exception:
                            logging.warning('Could not get feed %s ,and the fetch is restart now' % feed.feedurl)
                            feed.last_retrieved = datetime.now()
                            #feed.save()
                            break
                    if result.code == 200:
                            self.__parse_feed(result.read(), feed.feedurl, feed.stop_target, feed.category, feed.latest, feed.start_target, feed.mid_target, feed.end_target, feed.allow_target)

                            feed.last_retrieved = datetime.now()
                            feed.save()

                    elif result.code == 500:
                            logging.error('Feed %s returned with status code 500.' % feed.feedurl)
                    elif result.code == 404:
                            logging.error('Error 404: Nothing found at %s.' % feed.feedurl)
    
    getFeed.short_description = u'采集订阅'
    '''
    解析获取的feed内容
    '''
    def __parse_feed(self, feed_content, feed_url, stop_target, category, feed_latest, start_target, mid_target, end_target, allow_target):
                feed = feedparser.parse(feed_content)
                i = 0
                dead_i = 0
                for entry in feed.entries:
                        logging.info('start parse feed,the dead_i is %s', dead_i)
                        title = htmllib.decoding(entry.title)
                        categorie_keys = []
                        content = ''
                        date_published = datetime.now()
                        author_name = ''
                        Mystat = True
                        if self.__feedslist_check(title) == False:
                            try:
                                    i += 1
                                    url = ''
                                    logging.info('beging to add new article No. %s', i)
                                    if(entry.has_key('feedburner_origlink')):
                                            url = entry.feedburner_origlink
                                    else:
                                            url = entry.link
                                    if entry.has_key('content'):
                                            content = entry.content[0].value
                                    else:
                                            content = entry.description
                                    if entry.has_key('author'):
                                            author_name = entry.author
                                    else:
                                            author_name = "转载"
                                    stripper = HTMLStripper()
                                    stripper.feed(title)
                                    title = stripper.get_data()
                                    content = htmllib.decoding(content)
                                    content = htmllib.GetFeedclean(url, content, stop_target)
                                    if(entry.has_key('updated_parsed')):
                                            date_published = datetime(*entry.updated_parsed[:6])
                                    else:
                                            date_published = datetime.now()
                            except Exception, data:
                                    logging.warn('this like something happened,the error is %s', data)

                            try:
                                    feedresult = self.__store_article(title, url, category, content, date_published, author_name, feed_url, feed)
                                    if feedresult == True:
                                            logging.info('The No.%s  is fetched to the db', i)
                                    else:
                                            logging.error('The No.%s is fetched Fail', i)
                                            Mystat = False
                            except Exception, data:
                                    logging.warning('the error is %s', data)
                                    Mystat = False

                        else:
                            logging.info('skip this article,it is aready have')





    def __store_article(self, title, url, category, content, date_published, author_name, feed_link, feed):
                try:
                        entry = FeedsResult.objects.get(title=title)
                        return False
                except:
                        entry = FeedsResult(
                                          title=htmllib.decoding(title),
                                          link=url,
                                          excerpt=content,
                                          author_name=htmllib.decoding(author_name),
                                          category=category,
                                          feed=self.model.objects.get(),
                                          date=datetime.now()
                                          )
                       
#                        try:
#                                entry.date = datetime.strptime(date_published[:-6], '%a, %d %b %Y %H:%M:%S')
#                        except:
#                                try:
#                                        entry.date = datetime.strptime(date_published[0:19], '%Y-%m-%d %H:%M:%S')
#                                except:
#                                        entry.date = datetime.now()
#    
                        entry.save()
                        return True


    def __feedslist_check(self, title):
            try:
                entry = FeedsResult.objects.get(title=title)
                return True
            except:
                return False

    
class EntryAdmin(admin.ModelAdmin):
    """Admin for Entry model"""
    form = EntryAdminForm
    date_hierarchy = 'creation_date'
    fieldsets = ((_('Content'), {'fields': ('title', 'content',
                                            'image', 'status')}),
                 (_('Options'), {'fields': ('featured', 'excerpt', 'template',
                                            'related', 'authors',
                                            'creation_date',
                                            'start_publication',
                                            'end_publication'),
                                 'classes': ('collapse', 'collapse-closed')}),
                 (_('Privacy'), {'fields': ('password', 'login_required',),
                                 'classes': ('collapse', 'collapse-closed')}),
                 (_('Discussion'), {'fields': ('comment_enabled',
                                               'pingback_enabled')}),
                 (_('Publication'), {'fields': ('categories', 'tags',
                                                'sites', 'slug')}))
    list_filter = ('categories', 'authors', 'status', 'featured',
                   'login_required', 'comment_enabled', 'pingback_enabled',
                   'creation_date', 'start_publication',
                   'end_publication', 'sites')
    list_display = ('get_title', 'get_authors', 'get_categories',
                    'get_tags', 'get_sites',
                    'get_comments_are_open', 'pingback_enabled',
                    'get_is_actual', 'get_is_visible', 'get_link',
                    'get_short_url', 'creation_date')
    radio_fields = {'template': admin.VERTICAL}
    filter_horizontal = ('categories', 'authors', 'related')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'excerpt', 'content', 'tags')
    actions = ['make_mine', 'make_published', 'make_hidden',
               'close_comments', 'close_pingbacks',
               'ping_directories', 'make_tweet', 'put_on_top']
    actions_on_top = True
    actions_on_bottom = True

    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site
        super(EntryAdmin, self).__init__(model, admin_site)

    # Custom Display
    def get_title(self, entry):
        """Return the title with word count and number of comments"""
        title = _('%(title)s (%(word_count)i words)') % \
                {'title': entry.title, 'word_count': entry.word_count}
        comments = entry.comments.count()
        if comments:
            return _('%(title)s (%(comments)i comments)') % \
                   {'title': title, 'comments': comments}
        return title
    get_title.short_description = _('title')

    def get_authors(self, entry):
        """Return the authors in HTML"""
        try:
            authors = ['<a href="%s" target="blank">%s</a>' % 
                       (reverse('entry_author_detail',
                                args=[author.username]),
                        author.username) for author in entry.authors.all()]
        except NoReverseMatch:
            authors = [author.username for author in entry.authors.all()]
        return ', '.join(authors)
    get_authors.allow_tags = True
    get_authors.short_description = _('author(s)')

    def get_categories(self, entry):
        """Return the categories linked in HTML"""
        try:
            categories = ['<a href="%s" target="blank">%s</a>' % 
                          (category.get_absolute_url(), category.title)
                          for category in entry.categories.all()]
        except NoReverseMatch:
            categories = [category.title for category in
                          entry.categories.all()]
        return ', '.join(categories)
    get_categories.allow_tags = True
    get_categories.short_description = _('category(s)')

    def get_tags(self, entry):
        """Return the tags linked in HTML"""
        try:
            return ', '.join(['<a href="%s" target="blank">%s</a>' % 
                              (reverse('entry_tag_detail',
                                       args=[tag.name]), tag.name)
                              for tag in Tag.objects.get_for_object(entry)])
        except NoReverseMatch:
            return entry.tags
    get_tags.allow_tags = True
    get_tags.short_description = _('tag(s)')

    def get_sites(self, entry):
        """Return the sites linked in HTML"""
        return ', '.join(
            ['<a href="http://%(domain)s" target="blank">%(name)s</a>' % 
             site.__dict__ for site in entry.sites.all()])
    get_sites.allow_tags = True
    get_sites.short_description = _('site(s)')

    def get_comments_are_open(self, entry):
        """Admin wrapper for entry.comments_are_open"""
        return entry.comments_are_open
    get_comments_are_open.boolean = True
    get_comments_are_open.short_description = _('comment enabled')

    def get_is_actual(self, entry):
        """Admin wrapper for entry.is_actual"""
        return entry.is_actual
    get_is_actual.boolean = True
    get_is_actual.short_description = _('is actual')

    def get_is_visible(self, entry):
        """Admin wrapper for entry.is_visible"""
        return entry.is_visible
    get_is_visible.boolean = True
    get_is_visible.short_description = _('is visible')

    def get_link(self, entry):
        """Return a formated link to the entry"""
        return u'<a href="%s" target="blank">%s</a>' % (
            entry.get_absolute_url(), _('View'))
    get_link.allow_tags = True
    get_link.short_description = _('View on site')

    def get_short_url(self, entry):
        """Return the short url in HTML"""
        short_url = entry.short_url
        if not short_url:
            return _('Unavailable')
        return '<a href="%(url)s" target="blank">%(url)s</a>' % \
               {'url': short_url}
    get_short_url.allow_tags = True
    get_short_url.short_description = _('short url')

    # Custom Methods
    def save_model(self, request, entry, form, change):
        """Save the authors, update time, make an excerpt"""
        if not form.cleaned_data.get('excerpt') and entry.status == PUBLISHED:
            entry.excerpt = truncate_words(strip_tags(entry.content), 50)

        if entry.pk and not request.user.has_perm('entry.can_change_author'):
            form.cleaned_data['authors'] = entry.authors.all()

        if not form.cleaned_data.get('authors'):
            form.cleaned_data['authors'].append(request.user)

        entry.last_update = datetime.now()
        entry.save()

    def queryset(self, request):
        """Make special filtering by user permissions"""
        queryset = super(EntryAdmin, self).queryset(request)
        if request.user.has_perm('entry.can_view_all'):
            return queryset
        return request.user.entries.all()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Filters the disposable authors"""
        if db_field.name == 'authors':
            if request.user.has_perm('entry.can_change_author'):
                kwargs['queryset'] = User.objects.filter(is_staff=True)
            else:
                kwargs['queryset'] = User.objects.filter(pk=request.user.pk)

        return super(EntryAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs)

    def get_actions(self, request):
        """Define user actions by permissions"""
        actions = super(EntryAdmin, self).get_actions(request)
        if not request.user.has_perm('entry.can_change_author') \
           or not request.user.has_perm('entry.can_view_all'):
            del actions['make_mine']
        
       

        return actions

    # Custom Actions
    def make_mine(self, request, queryset):
        """Set the entries to the user"""
        for entry in queryset:
            if request.user not in entry.authors.all():
                entry.authors.add(request.user)
        self.message_user(
            request, _('The selected entries now belong to you.'))
    make_mine.short_description = _('Set the entries to the user')

    def make_published(self, request, queryset):
        """Set entries selected as published"""
        queryset.update(status=PUBLISHED)
        self.ping_directories(request, queryset, messages=False)
        self.message_user(
            request, _('The selected entries are now marked as published.'))
    make_published.short_description = _('Set entries selected as published')

    def make_hidden(self, request, queryset):
        """Set entries selected as hidden"""
        queryset.update(status=HIDDEN)
        self.message_user(
            request, _('The selected entries are now marked as hidden.'))
    make_hidden.short_description = _('Set entries selected as hidden')

    
    def close_comments(self, request, queryset):
        """Close the comments for selected entries"""
        queryset.update(comment_enabled=False)
        self.message_user(
            request, _('Comments are now closed for selected entries.'))
    close_comments.short_description = _('Close the comments for '\
                                         'selected entries')

    def close_pingbacks(self, request, queryset):
        """Close the pingbacks for selected entries"""
        queryset.update(pingback_enabled=False)
        self.message_user(
            request, _('Linkbacks are now closed for selected entries.'))
    close_pingbacks.short_description = _(
        'Close the linkbacks for selected entries')

    def put_on_top(self, request, queryset):
        """Put the selected entries on top at the current date"""
        queryset.update(creation_date=datetime.now())
        self.ping_directories(request, queryset, messages=False)
        self.message_user(request, _(
            'The selected entries are now set at the current date.'))
    put_on_top.short_description = _(
        'Put the selected entries on top at the current date')


    def get_urls(self):
        entry_admin_urls = super(EntryAdmin, self).get_urls()
        urls = patterns(
            'django.views.generic.simple',
            url(r'^autocomplete_tags/$', 'direct_to_template',
                {'template': 'admin/entry/entry/autocomplete_tags.js',
                 'mimetype': 'application/javascript'},
                name='entry_entry_autocomplete_tags'),
            url(r'^wymeditor/$', 'direct_to_template',
                {'template': 'admin/entry/entry/wymeditor.js',
                 'mimetype': 'application/javascript'},
                name='entry_entry_wymeditor'),
            url(r'^markitup/$', 'direct_to_template',
                {'template': 'admin/entry/entry/markitup.js',
                 'mimetype': 'application/javascript'},
                name='entry_entry_markitup'),)
        return urls + entry_admin_urls

    def _media(self):
        MEDIA_URL = settings.MEDIA_URL
        media = super(EntryAdmin, self).media + Media(
            css={'all': ('%scss/jquery.autocomplete.css' % MEDIA_URL,)},
            js=('%sjs/jquery.js' % MEDIA_URL,
                '%sjs/jquery.bgiframe.js' % MEDIA_URL,
                '%sjs/jquery.autocomplete.js' % MEDIA_URL,
                reverse('admin:entry_entry_autocomplete_tags'),))

        if settings.WYSIWYG == 'wymeditor':
            media += Media(
                js=('%sjs/wymeditor/jquery.wymeditor.pack.js' % MEDIA_URL,
                    '%sjs/wymeditor/plugins/hovertools/'
                    'jquery.wymeditor.hovertools.js' % MEDIA_URL,
                    reverse('admin:entry_entry_wymeditor')))
        elif settings.WYSIWYG == 'tinymce':
            from tinymce.widgets import TinyMCE
            media += TinyMCE().media + Media(
                js=(reverse('tinymce-js', args=('admin/entry/entry',)),))
        elif settings.WYSIWYG == 'markitup':
            media += Media(
                js=('%sjs/markitup/jquery.markitup.js' % MEDIA_URL,
                    '%sjs/markitup/sets/%s/set.js' % (
                        MEDIA_URL, settings.MARKUP_LANGUAGE),
                    reverse('admin:entry_entry_markitup')),
                css={'all': (
                    '%sjs/markitup/skins/django/style.css' % MEDIA_URL,
                    '%sjs/markitup/sets/%s/style.css' % (
                        MEDIA_URL, settings.MARKUP_LANGUAGE))})
        return media
    media = property(_media)
