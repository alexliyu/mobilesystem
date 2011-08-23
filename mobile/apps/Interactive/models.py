#-*- coding:utf-8 -*-
"""
这是互动活动模块的模型文件
创建于 2011-8-23.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.db import models
from django.conf import settings
from tinymce import models as tinymce_models
from datetime import datetime

from apps.gift.models import Gift_Info
# Create your models here.

class Interactive_Info(models.Model):
    """
    互动广告及节目模型类
    """
    title = models.CharField(u'活动名称', default='', max_length=70)
    description = tinymce_models.HTMLField(u'活动简介', default='', max_length=500)
    gift = models.ForeignKey(Gift_Info, verbose_name=u'奖品')
    start_time = models.DateTimeField(u'开始时间', default=datetime.now())
    end_time = models.DateTimeField(u'结束时间', default=datetime.now())
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"互动广告及节目"
        verbose_name_plural = u"互动广告及节目"

class Interactive_User(models.Model):
    """
    互动参与用户表
    """
    title = models.CharField(u'活动标题', default='', max_length=50)
    content = tinymce_models.HTMLField(u'活动内容', default='', max_length=500)
    beginTime = models.DateTimeField(u'开始时间', blank=True)
    endTime = models.DateTimeField(u'结束时间', blank=True)
    publishTime = models.DateTimeField(u'发布时间', auto_now_add=True)
    business = models.ForeignKey(BusinessInfo, verbose_name=u'所属商家')
    picSrc = models.FileField(u'优惠劵上传', upload_to=settings.UPLOADS_ROOT, blank=True)

    objects = models.Manager()
    
    
    def get_beginTime(self):
        return "%d-%d-%d %d:%d:%d" % self.beginTime[:6]
        
    def get_endTime(self):
        return "%d-%d-%d %d:%d:%d" % self.endTime[:6]

    def get_content(self):
        
        return self.content.__str__().replace("^<[^\s]>", "")
    
    def get_picSrc(self):
        try:
            a = self.picSrc.__str__().split('/media/uploads/images/')
            
            return '/media/uploads/images/' + a[1]
        except:
            return '/media/site/images/logo.png'

    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"活动列表"
        verbose_name_plural = u"活动列表"
