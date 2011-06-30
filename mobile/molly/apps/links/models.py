# -*- coding:utf-8 -*-
from django.db import models

class links_class(models.Model):
    class_title=models.CharField("类别名称",max_length=50,blank=False)
    addTime = models.DateField("添加时间",auto_now=True,blank=True)
    
    def __unicode__(self):
        return self.class_title
    
    class Meta:
        verbose_name="导航类别"
        verbose_name_plural="导航类别"

class Links(models.Model):
    link_title = models.CharField("标题",max_length=50,blank=False)
    link_url = models.CharField("路径",max_length=255,blank=False)
    addTime = models.DateField("添加时间",auto_now=True,blank=True)
    links_class=models.ForeignKey(links_class,verbose_name="所属类别")
    
    class Meta:
        verbose_name="网址导航"
        verbose_name_plural="网址导航"





