#-*- coding:utf-8 -*-
"""
这是用于显示天气的应用

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.utils.translation import ugettext_lazy as _

class Mete:
    """
    定义此应用程序的附加信息，诸如应用程序名
    """
    title = _('Weather')
    config = {
            'location_id':'1832',
            'display_to_user':True,
            'providers':['apps.weather.providers.BBCWeatherProvider', ]
            }
