# -*- coding:utf-8 -*-
from django.db import models

from userena.models import UserProfile
from tinymce import models as tinymce_models


class lottery(models.Model):
    lottery_title = models.CharField(u"活动标题", max_length=50, blank=False)
    UserProfile = models.ManyToManyField(UserProfile, verbose_name=u'获奖会员')
    addTime = models.DateTimeField(u"添加时间", auto_now=True)
    description = tinymce_models.HTMLField(u"活动简介", blank=True)
    sms_content = models.TextField(u'发送短信内容', blank=True)
    
    def __unicode__(self):
        return self.lottery_title
    
    def getidUrl(self):
        return '%s' % self.id

    class Meta:
        verbose_name = "抽奖活动"
        verbose_name_plural = "抽奖活动"

#def notify_sms(sender, instance, created, **kwargs):
#    '''当新创建一个获奖通知时进行发送短信处理'''
#    if created:
#        send_users = ''
#        sms_object = sms()
#        for user_object in instance.UserProfile.all():
#            send_users += user_object.get_profile().mobile + ','
#        send_result = sms_object.post_sms(send_users, instance.sms_content)
#      
#
#signals.post_save.connect(notify_sms, sender=lottery)
