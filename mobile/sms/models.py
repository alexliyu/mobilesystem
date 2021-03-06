#-*- coding:utf-8 -*-
"""
这是项目的基本配置文件.

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050

@param DEBUG 是否开启调试模式

@param TEMPLATE_DEBUG 是否开启模板调试模式

@event event 无事件

@exception exception 无返回

@keyparam  param 无参数

@return 无返回
       
"""
from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User, Group

# Create your models here.


class sms_entry(models.Model):
    GENDER_CHOICES = (
                       (0, u'短信发送'),
                       (1, u'首页显示'),
                       (2, u'短信发送及首页显示'),
                                    )
    title = models.CharField(u'短信标题', default='', max_length=50)
    content = models.TextField(u'短信内容', default='', max_length=200)
    creat_date = models.DateTimeField(u'创建时间', default=datetime.now)
    stat = models.IntegerField(u'短信用途', default=0, max_length=1, choices=GENDER_CHOICES)
    
    
    def get_random(self):
        return sms_entry.objects.exclude(stat=0).order_by('?')[:1].get()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"短信库"
        verbose_name_plural = u"短信库"
    
class sms_list(models.Model):
    GENDER_CHOICES = (
                       (0, u'未发送'),
                       (1, u'已发送'),
                       (2, u'已回复'),
                       (3, u'发送错误'),
                       (4, u'部分发送失败'),
                                    )
    title = models.CharField(u'短信标题', default='', max_length=50)
    content = models.TextField(u'短信内容', default='', max_length=200)
    creat_date = models.DateTimeField(u'创建时间', default=datetime.now)
    sms_id = models.CharField(u'短信流水号', blank=True, max_length=20)
    stat = models.IntegerField(u'发送状态', default=0, max_length=1, choices=GENDER_CHOICES)
    errors = models.TextField(u'错误信息', blank=True)
    sms_users = models.ManyToManyField(User, verbose_name=u'收信人列表', blank=True)
    sms_groups = models.ManyToManyField(Group, verbose_name=u'收信人群组', blank=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"群发短信"
        verbose_name_plural = u"群发短信"
        

class sms_time_list(models.Model):
    GENDER_CHOICES = (
                       (0, u'未启动'),
                       (1, u'已启动'),
                       (2, u'已发送'),
                       (3, u'发送错误'),
                       (4, u'部分发送失败'),
                                    )
    title = models.CharField(u'短信标题', default='', max_length=50)
    content = models.TextField(u'短信内容', default='', max_length=200)
    creat_date = models.DateTimeField(u'创建时间', default=datetime.now)
    send_date = models.DateTimeField(u'发送时间')
    sms_id = models.CharField(u'短信流水号', blank=True, max_length=20)
    stat = models.IntegerField(u'发送状态', default=0, max_length=1, choices=GENDER_CHOICES)
    errors = models.TextField(u'错误信息', blank=True)
    sms_users = models.ManyToManyField(User, verbose_name=u'收信人列表', blank=True)
    sms_groups = models.ManyToManyField(Group, verbose_name=u'收信人群组', blank=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"定时短信"
        verbose_name_plural = u"定时短信"
        

class sms_history(models.Model):
    GENDER_CHOICES = (
                       (0, u'未发送'),
                       (1, u'已发送'),
                       (2, u'已回复'),
                       (3, u'发送错误'),
                                    )
    SEND_TYPE_CHOICES = (
                       (0, u'下行'),
                       (1, u'上行'),
                                    )
    title = models.CharField(u'短信标题', default='', max_length=50)
    content = models.TextField(u'短信内容', default='', max_length=500)
    creat_date = models.DateTimeField(u'发送时间', default=datetime.now)
    sms_id = models.CharField(u'短信流水号', blank=True, max_length=50)
    sms_users = models.TextField(verbose_name=u'收信人列表', null='')
    send_type = models.IntegerField(u'短信类型', default=0, max_length=1, choices=SEND_TYPE_CHOICES)
    stat = models.IntegerField(u'发送状态', default=0, max_length=1, choices=GENDER_CHOICES)
    errors = models.TextField(u'错误信息', blank=True)

    objects = models.Manager()
    
    
    def __unicode__(self):
        return self.title
    
    def save_result(self, title, content, sms_id, sms_users, send_type, stat, errors=None):
        self.title = title
        self.content = content
        self.sms_id = sms_id
        self.sms_users = sms_users
        self.send_type = send_type
        self.stat = stat
        self.errors = errors
        self.save()
        
    class Meta:
        verbose_name = u"短信历史记录"
        verbose_name_plural = u"短信历史记录"
