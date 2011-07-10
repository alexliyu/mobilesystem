#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from django.db import models
from userena.models import UserenaBaseProfile


    
    
class UserProfile(UserenaBaseProfile):
    GENDER_CHOICES = (
                                    ('M', '男'),
                                    ('F', '女'),
                                    )
    #user = models.ForeignKey(User, unique=True, verbose_name=u'用户')
    birthday = models.DateField(u'用户生日')
    mac = models.CharField(u'用户mac地址', max_length=30, blank=True)
    mobile = models.CharField('移动电话', max_length=20, blank=True, null=True)
    address = models.CharField('家庭地址', max_length=100, blank=True, null=True)
    website = models.URLField('个人主页', blank=True, null=True)
    birthday = models.DateField('出生日期', blank=True, null=True)
    gender = models.CharField('性别', max_length=1, choices=GENDER_CHOICES, default='M')
    blog = models.URLField('个人主页', blank=True, null=True)
    QQ = models.CharField('QQ', max_length=50, blank=True, null=True)
    MSN = models.CharField(max_length=50, blank=True, null=True)
    IM = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField('目前所在地', max_length=200, blank=True, null=True)
    
    objects = models.Manager()
    
    class Meta:
        verbose_name = u"用户信息列表"
        verbose_name_plural = u"用户信息列表"
    
    def __unicode__(self):
        return self.mobile
    def replacestr(self):
        return "%s****%s"% (self.__str__()[0:3],self.__str__()[7:11])
