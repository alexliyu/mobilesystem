#-*- coding:utf-8 -*-
"""
这是短信收发模块.

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.conf import settings
import md5, suds

class sms(object):
    def __init__(self):
        self.url = 'http://sdk2.entinfo.cn:8060/webservice.asmx?WSDL'
        self.sn = settings.SMS_SN
        self.pwd = settings.SMS_PWD
        self.md5pwd = self.get_md5pwd(self.sn, self.pwd)
        self.client = suds.client.Client(self.url)
    def get_md5pwd(self, sn, pwd):
        m1 = md5.new()
        tmppwd = sn + pwd
        m1.update(tmppwd)
        result = m1.hexdigest()
        return result.upper()
    
    def parse_content(self, content):
        return content.decode('gbk').encode('gbk')
    
    def post_sms(self, mobile, content):
        result = self.client.service.mt(self.sn, self.md5pwd, mobile[:-1], self.parse_content(content), '', '', '')
        return result
