# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Lottery(models.Model):
    Lottery_title=models.CharField("活动标题",max_length=50,blank=False)
    User=models.ManyToManyField(User,verbose_name='获奖成员')
    addTime=models.DateTimeField("添加时间",auto_now=True)
    
    def __unicode__(self):
        return self.Lottery_title
    
    def getidUrl(self):
        return '%s'% self.id
    
    class Meta:
        verbose_name="抽奖活动"
        verbose_name_plural="抽奖活动"