#-*- coding:utf-8 -*-
"""
网址导航应用程序的数据模型类.

创建于 2011-7-10.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050


       
"""
from django.db import models

class links_class(models.Model):
    """
    网址分类模型.
    @param class_title 分类名称
    @param addTime 添加时间
    
    """
    class_title = models.CharField("类别名称", max_length=50, blank=False)
    addTime = models.DateField("添加时间", auto_now=True, blank=True)
    
    def links(self):
        """
        返回此分类下所包含的网址记录集
        
        """
        return Links.objects.all().filter(links_class=self)
    
    def __unicode__(self):
        return self.class_title
    
    class Meta:
        verbose_name = "导航类别"
        verbose_name_plural = "导航类别"

class Links(models.Model):
    """
    网址模型.
    @param link_title 网址名称
    @param link_url 网址
    @param addTime 添加时间
    @param links_class 所属分类
    
    """
    link_title = models.CharField("标题", max_length=50, blank=False)
    link_url = models.CharField("路径", max_length=255, blank=False)
    addTime = models.DateField("添加时间", auto_now=True, blank=True)
    links_class = models.ForeignKey(links_class, verbose_name="所属类别")
    
    class Meta:
        verbose_name = "网址导航"
        verbose_name_plural = "网址导航"





