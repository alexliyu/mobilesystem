#-*- coding:utf-8 -*-
"""
这是用于管理系统帐号的应用，属于系统核心应用之一，负责用户账户管理、注册等

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.utils.translation import ugettext_lazy as _

class Mete:
    """
    定义此应用程序的附加信息，诸如应用程序名
    """
    title = _('Userna')

VERSION = (1, 0, 0)

__version__ = '.'.join((str(each) for each in VERSION[:4]))

def get_version():
    """
    Returns string with digit parts only as version.

    """
    return '.'.join((str(each) for each in VERSION[:3]))
