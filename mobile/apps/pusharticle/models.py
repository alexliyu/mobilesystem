#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from django.db import models
from datetime import datetime
from entry.models import Category, Entry

        
class PushList(models.Model):
    PUSHURL_CHOICES = (
                       ('send_sina_msgs', u'新浪微博'),
                       ('send_qq_msgs', u'腾讯微博'),
    )
    CATEGORY_CHOICES = (
                       ('send_entry', u'包含文章内容的栏目'),
                       ('send_business', u'最新优惠资讯栏目'),
                       ('send_forum', u'社区帖子'),
                       ('send_interactive', u'互动节目栏目'),
    )
    name = models.CharField(u'名称', default=u'李昱的博客', max_length=20)
    pushurl = models.CharField(u'推送地址', choices=PUSHURL_CHOICES, max_length=3000)
    username = models.CharField(u'用户名', default='alexliyu', max_length=50)
    password = models.CharField(u'密码', default='password', max_length=50)
    latest = models.IntegerField(u'最后推送ID', default=0)
    last_retrieved = models.DateTimeField(u'最后推送时间', default=datetime.today().fromtimestamp(0))
    category = models.CharField(u'推送栏目', choices=CATEGORY_CHOICES, max_length=50)
    pushtime = models.IntegerField(u'推送间隔', default=120)
    is_active = models.BooleanField(u'启动', default=False)
    
    objects = models.Manager()
        
    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name = u"推送列表"
        verbose_name_plural = u"推送列表"
        ordering = ('name', 'pushurl',)
                

class PushResult(models.Model):
    
        GENDER_CHOICES = (
        (0, u'未推送'),
        (1, u'已推送'),
        (2, u'推送出错'),
        (3, u'已放推送集'),
        )
        
        title = models.CharField(u'推送内容标题', default='', max_length=100)
        push_name = models.CharField(u'推送设置标题', max_length=100)
        push_date = models.DateTimeField(u'推送时间', auto_now_add=True)
        push_stat = models.IntegerField(u'推送状态', default=0, max_length=1, choices=GENDER_CHOICES)
        
        objects = models.Manager()
        
        def __unicode__(self):
            return self.title
        
        class Meta:
            verbose_name = u"推送结果列表"
            verbose_name_plural = u"推送结果列表"
            
        
            


