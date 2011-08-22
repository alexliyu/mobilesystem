#-*- coding:utf-8 -*-
"""
这是短信发送模块
创建于 2011-8-22.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.utils.translation import ugettext_lazy as _

class Mete:
    """
    定义此应用程序的附加信息，诸如应用程序名
    """
    title = _('Sms')
    config = {
        'display_to_user':False
        
        }
