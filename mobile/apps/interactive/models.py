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
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from apps.gift.models import Gift_History
from utils.smsutils import sms
# Create your models here.

class Interactive_Categries(models.Model):
    """
    互动分类
    """
    title = models.CharField(u'分类名称', default='', max_length=70)
    slug = models.CharField(max_length=20)
    description = tinymce_models.HTMLField(u'分类简介', default='', max_length=500)
    create_time = models.DateTimeField(u'创建时间', default=datetime.now())
   
    def get_absolute_url(self):
        return reverse('interactive:interactivelist', args=[self.slug])
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"互动分类"
        verbose_name_plural = u"互动分类"
        
class Interactive_Info(models.Model):
    """
    互动广告及节目模型类
    """
    title = models.CharField(u'活动名称', default='', max_length=70)
    description = tinymce_models.HTMLField(u'活动简介', default='', max_length=500)
    gift = models.ForeignKey(Gift_Info, verbose_name=u'奖品')
    start_time = models.DateTimeField(u'开始时间', default=datetime.now())
    end_time = models.DateTimeField(u'结束时间', default=datetime.now())
    category = models.ForeignKey(Interactive_Categries, verbose_name=u'分类')
    
    
    def get_absolute_url(self):
        return reverse('interactive:interactivedetail', args=[self.pk])
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"互动广告及节目"
        verbose_name_plural = u"互动广告及节目"
        
        


class Interactive_User(models.Model):
    """
    互动参与用户表
    """
    STAT_CHOICES = (
                    (0, u'未获奖'),
                    (1, u'已获奖'),
                    (2, u'已入围'),
                    (3, u'已淘汰')
                    )
    interactive_user = models.ForeignKey(User, verbose_name=u'参与会员')
    content = tinymce_models.HTMLField(u'提交内容', default='', blank=True)
    create_time = models.DateTimeField(u'提交时间', auto_now_add=True)
    interactive_info = models.ForeignKey(Interactive_Info, verbose_name=u'参与活动')
    upload_file = models.CharField(u'上传文件', blank=True, max_length=200)
    stat = models.IntegerField(u'状态', choices=STAT_CHOICES, default=0)
    
    def save_gift(self):
        gift_object = Gift_History()
        gift_object.title = self.interactive_info.title
        gift_object.gift = self.interactive_info.gift
        gift_object.user = self.interactive_user
        gift_object.gift_active = self.interactive_info.title
        gift_object.stat = 0
        gift_object.save()
    
    def __unicode__(self):
        return self.interactive_user.username
    
    class Meta:
        verbose_name = u"互动参与用户列表"
        verbose_name_plural = u"互动参与用户列表"

def notify_sms(sender, instance, created, **kwargs):
    '''当新创建一个获奖通知时进行发送短信处理'''
    send_users = instance.interactive_user.get_profile().mobile
    sms_object = sms()
    content = u'感谢您参与娱讯互动活动,稍后我们会进行进一步的评奖,结果会以短信通知'
    if not created:
        if instance.stat == 2:
            content = u'您所提交的%s的答案已入围,稍后我们会进行进一步的评奖,结果会以短信通知' % instance.interactive_info.title
        elif instance.stat == 1:
            content = u'您所提交的%s的答案已获奖，稍后我们会以电话联系您' % instance.interactive_info.title
            instance.save_gift()
        elif instance.stat == 3:
            content = u'不好意思，您所提交的%s的答案已被淘汰，欢迎您继续参与我们其他的互动活动' % instance.interactive_info.title
    send_result = sms_object.post_sms(u'互动节目获奖通知短信', send_users, content)
      

post_save.connect(notify_sms, sender=Interactive_User)
