#-*- coding:utf-8 -*-
"""
这是用于进行批量任务处理的应用，采用多线程处理系统一些批量性的后台业务

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.utils.translation import ugettext_lazy as _

class Mete:
    """
    定义此应用程序的附加信息，诸如应用程序名
    """
    title = _('E2 Mobile System')

__version__ = '0.0.2'
