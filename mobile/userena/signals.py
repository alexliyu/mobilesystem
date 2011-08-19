#-*- coding:utf-8 -*-
'''
注册用户系统模块的Signal
Created on 2011-1-30

@author: 李昱
'''

from django.dispatch import Signal
from actstream import action

signup_complete = Signal(providing_args=["user", ])
activation_complete = Signal(providing_args=["user", ])
confirmation_complete = Signal(providing_args=["user", ])

def signup_complete_handler(sender, **kwargs):
    """
    注册一个handler,用于在评论后，自动添加一条用户动态
    """
    action.send(kwargs['user'], verb=u'刚注册成为会员')

signup_complete.connect(signup_complete_handler)
