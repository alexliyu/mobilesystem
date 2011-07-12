#-*- coding:utf-8 -*-
"""
这是用于采集FEED与格式化显示FEED的应用程序，可以通过在批量处理里面进行同步
创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.utils.translation import ugettext_lazy as _

class Mete:
    """
    定义此应用程序的附加信息，诸如应用程序名
    """
    title = _('Feeds')
