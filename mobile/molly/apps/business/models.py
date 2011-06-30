#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from mobile import settings

# Create your models here.
class BusinessInfo(models.Model):
    businessName = models.CharField(u'商家名称',default='',max_length=50)
    introdution = models.TextField(u'商家简介',default='',max_length=200)
    businessUrl = models.URLField(u'商家网址',blank=True)
    telephone = models.CharField(u'联系电话',default='0592-5166918',max_length=15)
    businessLogo = models.FileField(u'商家LOGO', upload_to=settings.MEDIA_ROOT,blank=True)
    
    objects = models.Manager()
    
    def get_bidUrl(self):
        return 'pro/%s'% self.id
    
    def get_logoUrl(self):
        try:
            a = self.businessLogo.__str__().split('/media/')
            return '/media/'+a[1]
        except:
            return '/media/111.jpg'

    def __unicode__(self):
        return self.businessName
    
    class Meta:
        verbose_name = u"商家列表"
        verbose_name_plural = u"商家列表"

class PromotionsInfo(models.Model):
    title = models.CharField(u'活动标题',default='',max_length=50)
    content = models.TextField(u'活动内容',default='',max_length=500)
    beginTime = models.DateTimeField(u'开始时间',blank=True)
    endTime = models.DateTimeField(u'结束时间',blank=True)
    publishTime = models.DateTimeField(u'发布时间', auto_now_add=True)
    business = models.ForeignKey(BusinessInfo,verbose_name=u'所属商家')
    picSrc = models.FileField(u'优惠劵上传', upload_to=settings.MEDIA_ROOT,blank=True)

    objects = models.Manager()
    
    
    def get_beginTime(self):
        return "%d-%d-%d %d:%d:%d"% self.beginTime[:6]
        
    def get_endTime(self):
        return "%d-%d-%d %d:%d:%d"% self.endTime[:6]

    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"活动列表"
        verbose_name_plural = u"活动列表"