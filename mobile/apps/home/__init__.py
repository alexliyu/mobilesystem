#-*- coding:utf-8 -*-
"""
这是用于站点主页显示的应用，包含主体框架的实现

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.utils.translation import ugettext_lazy as _

comments_title = _('Comments')

from django.utils.translation import ugettext_lazy as _

class Mete:
    """
    定义此应用程序的附加信息，诸如应用程序名
    """
    title = _('Home')
    config = {
        'display_to_user':False
        
        }
    
