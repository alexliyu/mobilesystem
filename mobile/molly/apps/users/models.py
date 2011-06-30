#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
import re
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from mobile.molly.apps.users.decorators import USER_AGENT_BLACKLIST
from mobile.molly.apps.users.forms import UserCreationForm
from mobile.molly.apps.users.exceptions import NotLazyError
from mobile.molly.apps.users.utils import is_lazy_user
from mobile.userena.models import UserenaBaseProfile
DEFAULT_BLACKLIST = (
    'slurp',
    'googlebot',
    'yandex',
    'msnbot',
    'baiduspider',
)

for user_agent in getattr(settings, 'LAZYSIGNUP_USER_AGENT_BLACKLIST', DEFAULT_BLACKLIST):
    USER_AGENT_BLACKLIST.append(re.compile(user_agent, re.I))


class LazyUserManager(models.Manager):

    def create_lazy_user(self, username):
        """ Create a lazy user.
        """
        user_class = LazyUser.get_user_class()
        user = user_class.objects.create_user(username, '')
        self.create(user=user)
        return user

    def convert(self, form):
        """ Convert a lazy user to a non-lazy one. The form passed
        in is expected to be a ModelForm instance, bound to the user
        to be converted.

        The converted ``User`` object is returned.

        Raises a TypeError if the user is not lazy.
        """
        if not is_lazy_user(form.instance):
            raise NotLazyError, 'You cannot convert a non-lazy user'

        user = form.save()

        # We need to remove the LazyUser instance assocated with the
        # newly-converted user
        self.filter(user=user).delete()
        return user


class LazyUser(models.Model):
    user = models.ForeignKey(
        getattr(settings, 'LAZYSIGNUP_USER_MODEL', 'auth.User'),
        unique=True)
    objects = LazyUserManager()

    @classmethod
    def get_user_class(cls):
        return cls._meta.get_field('user').rel.to
    
    
class UserProfile(UserenaBaseProfile):
    GENDER_CHOICES = (
                                    ('M', '男'),
                                    ('F', '女'),
                                    )
    #user = models.ForeignKey(User, unique=True, verbose_name=u'用户')
    birthday = models.DateField(u'用户生日')
    mac = models.CharField(u'用户mac地址', max_length=16, blank=True)
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
    
