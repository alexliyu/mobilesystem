#-*- coding:utf-8 -*-
"""
这是消防合作栏目模块，用于前台显示消防公益栏目
创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.utils.translation import ugettext_lazy as _

class Mete:
    """
    定义此应用程序的附加信息，诸如应用程序名
    """
    title = _('Xiaofang')
    config = {
        'display_to_user':True,
        'providers':['apps.entry.providers.CategoriesEntryProvider']
        
        }
