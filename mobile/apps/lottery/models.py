# -*- coding:utf-8 -*-
from django.db import models
from userena.models import UserProfile

class lottery(models.Model):
    lottery_title = models.CharField("活动标题", max_length=50, blank=False)
    UserProfile = models.ManyToManyField(UserProfile, verbose_name='获奖成员')
    addTime = models.DateTimeField("添加时间", auto_now=True)
    
    def __unicode__(self):
        return self.lottery_title
    
    def getidUrl(self):
        return '%s' % self.id

    class Meta:
        verbose_name = "抽奖活动"
        verbose_name_plural = "抽奖活动"
