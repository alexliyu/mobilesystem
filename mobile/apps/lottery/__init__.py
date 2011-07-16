#-*- coding:utf-8 -*-
"""
这是抽奖公示模块，用于设置中奖结果并提供前台显示
创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.utils.translation import ugettext_lazy as _

class Mete:
    """
    定义此应用程序的附加信息，诸如应用程序名
    """
    title = _('Lottery')
    config = {
        'display_to_user':True
        
        }
