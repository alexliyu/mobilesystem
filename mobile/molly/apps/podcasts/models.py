# -*- coding:utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from mobile.molly.apps.podcasts.data import licenses

MEDIUM_CHOICES = (
    ('audio', 'audio'),
    ('video', 'video'),
    ('document', 'document'),
)

class PodcastCategory(models.Model):
    slug = models.SlugField()
    name = models.TextField(u'名称')
    order = models.IntegerField(u'序号',null=True)
    
    def get_absolute_url(self):
        return reverse('podcasts:category', args=[self.slug])
        
    def __unicode__(self):
        return self.name or ''
    class Meta:
        verbose_name = u'视频类别'
        verbose_name_plural = u'视频类别'
        ordering = ('order','name',)

class Podcast(models.Model):
    slug = models.SlugField(unique=True)
    title = models.TextField(u'标题',null=True)
    description = models.TextField(u'说明',null=True)
    rss_url = models.URLField(u'RSS路径')
    last_updated = models.DateTimeField('最后更新时间',auto_now=True)
    category = models.ForeignKey(PodcastCategory, null=True)
    most_recent_item_date = models.DateTimeField(u'最近时间',null=True)
    medium = models.CharField(u'媒介',max_length=8, choices=MEDIUM_CHOICES, null=True)
    provider = models.TextField(u'供应商')
    license = models.URLField(u'授权',null=True)
    logo = models.URLField(null=True)
    
    def get_absolute_url(self):
        return reverse(u'podcasts:podcast', args=[self.slug])
        
    def __unicode__(self):
        return self.title or ''
        
    @property
    def license_data(self):
        return licenses.get(self.license)

    class Meta:
        verbose_name = u'视频订阅'
        verbose_name_plural = u'视频订阅'
        ordering = ('title',)


class PodcastItem(models.Model):
    podcast = models.ForeignKey(Podcast)
    title = models.TextField(u'标题',null=True)
    description = models.TextField(u'说明',null=True)
    published_date = models.DateTimeField(u'出版日期',null=True)
    author = models.TextField(u'作者',null=True, blank=True)
    duration = models.PositiveIntegerField(u'持续时间',null=True)
    guid = models.TextField()
    order = models.IntegerField(u'序号',null=True)
    license = models.URLField(u'版权',null=True)

    def __unicode__(self):
        return self.title or ''
        
    @property
    def license_data(self):
        return licenses.get(self.license) or licenses.get(self.podcast.license)

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = u'视频'

MIMETYPES = {
    'audio/x-mpeg': 'MP3 audio',
    'video/mp4': 'MP4 video',
    'MPEG4 Video': 'MP4 video',
    'text/html': 'HTML document',
    'audio/mpeg': 'MP3 audio',
    'video/x-ms-wmv': 'WMV video',
    'text/plain': 'plain text',
    'application/pdf': 'PDF document',
    'audio/x-m4b': 'MP4 audio',
    'application/octet-stream': 'unknown',
    'video/mpeg': 'MPEG video',
    'video/x-m4v': 'MP4 video',
    'audio/x-m4a': 'MP4 audio',
    'application/epub+zip': 'ePub eBook'
}    

class PodcastEnclosure(models.Model):
    podcast_item = models.ForeignKey(PodcastItem)
    url = models.URLField(u'路径')
    length = models.IntegerField(u'长度',null=True)
    mimetype = models.TextField(u'MIME类型',null=True)
    
    @property
    def medium(self):
        medium = {'application/pdf': 'document', 'MPEG4 Video': 'video'}.get(self.mimetype)
        if medium:
            return medium
        elif not self.mimetype:
            return self.podcast_item.podcast.medium or 'unknown'
        elif self.mimetype.startswith('audio/'):
            return 'audio'
        elif self.mimetype.startswith('video/'):
            return 'video'
        else:
            return self.podcast_item.podcast.medium or 'unknown'
    
    def get_mimetype_display(self):
        return MIMETYPES.get(self.mimetype, 'unknown')
    
    class Meta:
        verbose_name = '视频包含的文件'
        verbose_name_plural = '视频包含的文件'

