#-*- coding:utf-8 -*-
"""
批量任务模型类.

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050

@param DEBUG 是否开启调试模式

@param TEMPLATE_DEBUG 是否开启模板调试模式

@event event 无事件

@exception exception 无返回

@keyparam  param 无参数

@return 无返回
       
"""
import simplejson, traceback, sys, logging
from datetime import datetime
from StringIO import StringIO

from django.db import models

from mobile.conf import all_apps, app_by_local_name

logger = logging.getLogger("mobile.batch_processing")

class TeeStringIO(StringIO):
    def __init__(self, *args, **kwargs):
        self.other = kwargs.pop('other')
        StringIO.__init__(self, *args, **kwargs)
        
    def write(self, *args, **kwargs):
        self.other.write(*args, **kwargs)
        StringIO.write(self, *args, **kwargs)

class Batch(models.Model):
    title = models.TextField(u'标题')
    local_name = models.TextField(u'本地名称')
    provider_name = models.TextField(u'供应商名称')
    method_name = models.TextField(u'方法名称')
    cron_stmt = models.TextField(u'参数')
    enabled = models.BooleanField(u'启用', default=True)

    _metadata = models.TextField(u'数据元', default='null')
    last_run = models.DateTimeField(u'上次运行时间', null=True, blank=True)
    pending = models.BooleanField(u'等待', default=False)
    currently_running = models.BooleanField(u'当前正在运行', default=False)
    log = models.TextField(u'日志', blank=True)
    
    def get_metadata(self):
        try:
            return self.__metadata
        except AttributeError:
            self.__metadata = simplejson.loads(self._metadata)
            return self.__metadata
    def set_metadata(self, metadata):
        self.__metadata = metadata
    metadata = property(get_metadata, set_metadata)

    def save(self, *args, **kwargs):
        try:
            self._metadata = simplejson.dumps(self.__metadata)
        except AttributeError:
            pass
        super(Batch, self).save(*args, **kwargs)

    def run(self, tee_to_stdout=False):
        if self.currently_running:
            return
        
        try:
            output = TeeStringIO(other=sys.stdout) if tee_to_stdout else StringIO()
            
            self.currently_running = True
            self.pending = False
            self.save()
            
            
            providers = app_by_local_name(self.local_name).providers
            for provider in providers:
                if provider.class_path == self.provider_name:
                    break
            else:
                raise AssertionError
            
            method = getattr(provider, self.method_name)
            
            self.metadata = method(self.metadata, output)
        except Exception, e:
            if output.getvalue():
                output.write("\n\n")
            traceback.print_exc(file=output)
            logger.exception('Batch %r threw an uncaught exception' % self.title)
        finally:
            self.log = output.getvalue()
            self.last_run = datetime.utcnow()
            self.currently_running = False
            self.save()

    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"批量列表"
        verbose_name_plural = u"批量列表"
