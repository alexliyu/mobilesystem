# -*- coding: utf-8 -*-
from dateutil.tz import tzutc, tzlocal
from lxml import etree
import simplejson

from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings

from external_media import resize_external_image
from apps.places.models import Entity
from gmapsfield.fields import GoogleMapsField
FEED_TYPE_CHOICES = (
    ('n', 'tuan'),
    ('e', 'zine'),
)


PROVIDER_CHOICES = tuple(
    (provider().class_path, provider().verbose_name)
        for app in settings.APPLICATIONS
        for provider in app.providers
        if app.application_name == 'apps.feeds'
)

FORMAT_CHOICES = tuple((x, x) for x in (
    'lecture', 'class', 'tutorial', 'seminar', 'performance', 'workshop',
    'exhibition', 'meeting',
))



class EventsManager(models.Manager):
    def get_query_set(self):
        return super(EventsManager, self).get_query_set().filter(ptype='e')
class NewsManager(models.Manager):
    def get_query_set(self):
        return super(NewsManager, self).get_query_set().filter(ptype='n')


class Tag(models.Model):
    value = models.CharField(max_length=128)

class Feed(models.Model):
    title = models.TextField(u'订阅标题', default='', max_length=50)
    unit = models.CharField(u'单位', max_length=10, null=True, blank=True)
    rss_url = models.URLField(u"路径", blank=True)
    slug = models.SlugField()
    last_modified = models.DateTimeField(u"最后修改日期", null=True, blank=True) # this one is in UTC
    
    ptype = models.CharField(u'类型', max_length=1, choices=FEED_TYPE_CHOICES)
    provider = models.CharField(u'供应商', max_length=128, choices=PROVIDER_CHOICES)
    
    def _set_importer_params(self, value):
        self._importer_params = simplejson.dumps(value)
    def _get_importer_params(self):
        return simplejson.loads(self._importer_params)
    importer_params = property(_get_importer_params, _set_importer_params) 
    
    objects = models.Manager()
    events = EventsManager()
    news = NewsManager()

    tags = models.ManyToManyField(Tag, blank=True)
    
    def __unicode__(self):
        return self.title
        
    def get_absolute_url(self):
        if self.ptype == 'n':
            return reverse('tuan:item-list', args=[self.slug])
        else:
            return reverse('zine:item-list', args=[self.slug])
        
    class Meta:
        ordering = ('title',)
        verbose_name = u"订阅"
        verbose_name_plural = u"订阅"

class vCard(models.Model):
    uri = models.TextField()

    name = models.TextField(u'名称', blank=True, max_length=50)
    address = models.TextField(u'地址', blank=True)
    telephone = models.TextField(u'联系电话', blank=True)
    location = GoogleMapsField(u'位置')
    entity = models.ForeignKey(Entity, null=True, blank=True, verbose_name=u'所属文章')
    
    class Meta:
        verbose_name = u"电子名片"
        verbose_name_plural = u"电子名片"
    
class Series(models.Model):
    feed = models.ForeignKey(Feed)
    guid = models.TextField(u'编号', default='')
    title = models.TextField(u'标题', default='', max_length=50)
    unit = models.ForeignKey(vCard, null=True, blank=True, verbose_name=u'所属单位')

    tags = models.ManyToManyField(Tag, blank=True)
    
    class Meta:
        verbose_name = u"系列"
        verbose_name_plural = u"系列"

class Item(models.Model):
    feed = models.ForeignKey(Feed)
    title = models.TextField(u'产品标题', default='', max_length=50)
    guid = models.TextField(u'编号', default='')
    description = models.TextField(u'产品描述', default='', max_length=500)
    link = models.URLField(u'产品网址', blank=True)
    last_modified = models.DateTimeField(u"最后修改日期", null=True, blank=True) # this one is also in UTC
    
    ptype = models.CharField(u'产品类型', max_length=16, choices=FEED_TYPE_CHOICES)
    
    organiser = models.ForeignKey(vCard, related_name='organising_set', null=True, blank=True)
    speaker = models.ForeignKey(vCard, related_name='speaking_set', null=True, blank=True)
    venue = models.ForeignKey(vCard, related_name='venue_set', null=True, blank=True)
    contact = models.ForeignKey(vCard, related_name='contact_set', null=True, blank=True)
    
    series = models.ForeignKey(Series, null=True, blank=True)
    ordinal = models.IntegerField(u'序数', null=True)
    track = models.TextField(u'路径', blank=True)
    
    tags = models.ManyToManyField(Tag, blank=True)

    objects = models.Manager()
    events = EventsManager()
    news = NewsManager()

    dt_start = models.DateTimeField(null=True, blank=True)
    dt_end = models.DateTimeField(null=True, blank=True)
    dt_has_time = models.BooleanField(default=False)
    
    @property
    def location_mobile_url(self):
        return self.location_url.replace('/reviews/venue/', '/reviews/phone/venue/')
    
    @property
    def last_modified_local(self):
        try:
            return self.last_modified.replace(tzinfo=tzutc()).astimezone(tzlocal())
        except Exception, e:
            return repr(e)
    
    def get_absolute_url(self):
        if self.ptype == 'n':
            return reverse('tuan:item-detail', args=[self.feed.slug, self.id])
        else:
            return reverse('zine:item-detail', args=[self.feed.slug, self.id])
        
        
    def get_description_display(self, device):
        html = etree.fromstring('<div>%s</div>' % self.description, parser=etree.HTMLParser())
        for img in html.findall('.//img'):
            eis = resize_external_image(img.attrib['src'], device.max_image_width - 40)
            if eis != None:
                img.attrib['src'] = eis.get_absolute_url()
                img.attrib['width'] = '%d' % eis.width
                img.attrib['height'] = '%d' % eis.height
        return etree.tostring(html.find('.//div'), method="html")[5:-6]
    
    def save(self, *args, **kwargs):
        self.ptype = self.feed.ptype
        super(Item, self).save(*args, **kwargs)
        
    
    class Meta:
        ordering = ('-last_modified',)

        verbose_name = u"产品列表"
        verbose_name_plural = u"产品列表"

    
