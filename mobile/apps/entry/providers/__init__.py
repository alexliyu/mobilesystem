#-*- coding:utf-8 -*-
"""
这是用于其他模块调用Entry数据的providers的基类定义

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050

       
"""
class BaseEntryProvider(object):

    pass

from apps.entry.providers.categories import CategoriesEntryProvider
from apps.entry.providers.zine import ZineEntryProvider
