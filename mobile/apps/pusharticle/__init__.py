#-*- coding:utf-8 -*-
"""
这是信息推送模块，用来把数据库内的信息推送到其他网站上去
创建于 2011-10-19.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.utils.translation import ugettext_lazy as _

class Mete:
    """
    定义此应用程序的附加信息，诸如应用程序名
    """
    title = _('Pusharticle')
    config = {
        'display_to_user':False,
        'providers':['apps.pusharticle.providers.SinaMsgsProvider', ]
        
        }
