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
from django.contrib.auth.models import User
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
    user = models.ForeignKey(User, verbose_name=u'参与会员')
    content = tinymce_models.HTMLField(u'提交内容', default='', blank=True)
    create_time = models.DateTimeField(u'提交时间', auto_now_add=True)
    interactive_info = models.ForeignKey(Interactive_Info, verbose_name=u'参与活动')
    upload_file = models.CharField(u'上传文件', blank=True, max_length=200)

    def __unicode__(self):
        return self.user
    
    class Meta:
        verbose_name = u"互动参与用户列表"
        verbose_name_plural = u"互动参与用户列表"
