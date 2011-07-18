#-*- coding:utf-8 -*-
"""
这是项目的基本模型模块，主要用于通过数据库来管理系统的APPS.

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050

"""

from django.db import models


class Apps(models.Model):
    name = models.CharField(u'插件名称', max_length=200)
    namespace = models.CharField(u'命名空间', max_length=200)
    slug = models.CharField(max_length=50)
    config = models.TextField('配置', blank=True)
    active = models.BooleanField('激活', default=False)
    create_date = models.DateTimeField('添加日期', auto_now=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = "插件管理"
        verbose_name_plural = "插件管理"

