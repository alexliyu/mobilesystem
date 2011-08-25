#-*- coding:utf-8 -*-
"""
这是互动活动模块
创建于 2011-8-23.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.utils.translation import ugettext_lazy as _

class Mete:
    """
    定义此应用程序的附加信息，诸如应用程序名
    """
    title = _('Interactive')
    config = {
        'display_to_user':False
        
        }
