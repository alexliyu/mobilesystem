#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from django.db import models
from datetime import datetime
from lincdm.entry.models import Category
# Create your models here.

        

class FeedList(models.Model):
        name = models.CharField(u'名称', default=u'李昱的博客', max_length=20)
        feedurl = models.CharField(u'rss订阅地址', default='http://alexliyu.blog.163.com/rss', max_length=300)
        latest = models.CharField(default='first', max_length=300)
        last_retrieved = models.DateTimeField(default=datetime.today().fromtimestamp(0))
        remotecategory = models.CharField(u'远程栏目', default='douban', max_length=300)
        remoteconf = models.CharField(u'远程配置', default='0', max_length=30)
        start_target = models.CharField(u'起始位置', default='nohtml', max_length=300)
        stop_target = models.CharField(u'结束位置', default='nohtml', max_length=300)
        allow_target = models.CharField(u'允许的标签', default='p i strong b u a h1 h2 h3 br img div embed span', max_length=300)
        mid_target = models.CharField(u'禁止的属性', default='ad1 ad2 href text/javascript st-related-posts h4 tags meta crinfo style randompost subscribe-af', max_length=300)
        end_target = models.CharField(u'允许的属性', default='src allowscriptaccess allowNetworking pluginspage width allowScriptAccess type wmode height quality invokeurls allownetworking invokeURLs', max_length=300)       
        category = models.ForeignKey(Category, verbose_name=u'所属栏目')
        #last_modified = models.DateTimeField(u'最后修改时间', null=True, blank=True, db_index=True)
        # 最后一次检查的时间
        #last_checked = models.DateTimeField(u'最后检查时间', null=True, blank=True)
        # 是否激活
        #is_active = models.BooleanField(u'激活', default=True, db_index=True,
        #help_text=u'如果没有激活，那么将不会自动更新')
        
        objects = models.Manager()
        
        def __unicode__(self):
            return self.name
        
        class Meta:
            verbose_name = u"采集列表"
            verbose_name_plural = u"采集列表"
            ordering = ('name', 'feedurl',)
            



class FeedsResult(models.Model):
    
        GENDER_CHOICES = (
        (0, u'未采集'),
        (1, u'已采集'),
        (2, u'采集出错'),
        (3, u'已放弃采集'),
        (4, u'已存储数据库'),
        )
        
        title = models.CharField(u'标题', default='', max_length=50)
        author_name = models.CharField(u'作者', max_length=15)
        date = models.DateTimeField(u'添加时间', auto_now_add=True)
        link = models.URLField(u'原文地址')
        excerpt = models.TextField(u'摘要', blank=True, max_length=500)
        content = models.TextField(u'内容', blank=True)
        feed = models.ForeignKey(FeedList, verbose_name=u'采集订阅')
        category = models.ForeignKey(Category, verbose_name=u'目标栏目')
        fetch_stat = models.IntegerField(u'采集状态', default=0, max_length=1, choices=GENDER_CHOICES)
        objects = models.Manager()
        
        def __unicode__(self):
            return self.title
        
        class Meta:
            verbose_name = u"采集结果列表"
            verbose_name_plural = u"采集结果列表"
            
        
        
class FeedSet(models.Model):
        defDate = models.IntegerField(default=3600)
        defStat = models.BooleanField(default=True)
        defDir = models.CharField(default='', max_length=300)
        last_checked = models.DateTimeField(default=datetime.today().fromtimestamp(0))
        stat = models.BooleanField(default=False)
        delitems = models.IntegerField(default=0)
        delitemi = models.IntegerField(default=0)
        chnitemi = models.IntegerField(default=0)
        entryerrs = models.IntegerField(default=0)
        entryerri = models.IntegerField(default=0)
        last_entry = models.DateTimeField()
        last_feedslist = models.IntegerField(default=0)
        check_db_num = models.IntegerField(default=50)
        fetch_db_num = models.IntegerField(default=50)
        imgchecked_num = models.IntegerField(default=0)
        last_imgchecked = models.DateTimeField()

class TempImages(models.Model):
    GENDER_CHOICES = (
        (0, u'未采集'),
        (1, u'已采集'),
        (2, u'采集出错'),
        (3, u'已放弃采集'),
        (4, u'已存储数据库'),
        )
    oldurl = models.URLField(u'旧图片网址', blank=True, max_length=400)
    newurl = models.URLField(u'新图片网址', blank=True, max_length=400)
    stat = models.IntegerField(u'替换状态', default=0, max_length=1, choices=GENDER_CHOICES)
    greatdate = models.DateTimeField(u'创建时间', auto_now_add=True)
    parsedate = models.DateTimeField(verbose_name=u'采集替换时间', auto_now=True)
    entry = models.ForeignKey(FeedsResult, verbose_name=u'所属文章')
    objects = models.Manager()
        
    def __unicode__(self):
        return self.oldurl
        
    class Meta:
        verbose_name = u"图片采集列表"
        verbose_name_plural = u"图片采集列表"
            


