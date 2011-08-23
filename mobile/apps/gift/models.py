#-*- coding:utf-8 -*-
"""
这是奖品管理模块的模型文件
创建于 2011-8-23.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.db import models
from django.conf import settings

from apps.business.models import BusinessInfo
from django.contrib.auth.models import User
# Create your models here.

class Gift_Info(models.Model):
    """
    奖品模型类
    """
    TYPE_CHOICES = (
                    (0, u'自备'),
                    (1, u'广告置换'),
                    (2, u'商家提供')
                    )
    title = models.CharField(u'奖品名称', default='', max_length=100)
    description = models.TextField(u'奖品简介', default='', max_length=500)
    all_count = models.IntegerField(u'奖品数量', default=0)
    left_count = models.IntegerField(u'剩余数量', default=0)
    money = models.IntegerField(u'奖品价值', default=0)
    creat_time = models.DateTimeField(u'入库时间', auto_now_add=True)
    business = models.ForeignKey(BusinessInfo, verbose_name=u'提供商家')
    gift_type = models.IntegerField(u'奖品类型', choices=TYPE_CHOICES)
    #user = models.ManyToOneRel(User, verbose_name=u'获奖人')
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"奖品管理"
        verbose_name_plural = u"奖品管理"

class Gift_History(models.Model):
    """
    奖品发放记录
    """
    STAT_CHOICES = (
                    (0, u'未领取'),
                    (1, u'已领取'),
                    (2, u'其他')
                    )
    title = models.CharField(u'发放标题', default='', max_length=100)
    gift = models.ForeignKey(Gift_Info, verbose_name=u'奖品')
    creat_time = models.DateTimeField(u'发放时间', auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=u'领奖人')
    gift_active = models.TextField(u'领奖活动', auto_now_add=True)
    stat = models.IntegerField(u'领奖状态', choices=STAT_CHOICES)
    
    

    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"奖品发放记录"
        verbose_name_plural = u"奖品发放记录"
