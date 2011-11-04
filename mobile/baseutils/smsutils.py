#-*- coding:utf-8 -*-
"""
这是短信收发模块.

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.conf import settings
from sms.models import sms_history
import md5, suds
import sms

class sms(object):
    def __init__(self):
        self.url = 'http://sdk2.entinfo.cn:8060/webservice.asmx?WSDL'
        self.sn = settings.SMS_SN
        self.pwd = settings.SMS_PWD
        self.province = settings.SMS_PROVINCE
        self.city = settings.SMS_CITY
        self.trade = settings.SMS_TRADE
        self.entname = settings.SMS_ENTNAME
        self.linkman = settings.SMS_LINKMAN
        self.phone = settings.SMS_PHONE
        self.mobile = settings.SMS_MOBILE
        self.email = settings.SMS_EMAIL
        self.fax = settings.SMS_FAX
        self.address = settings.SMS_ADDRESS
        self.postcode = settings.SMS_POSTCODE = 361000
        self.sign = settings.SMS_SIGN
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
    
    def post_sms(self, title, mobile, content):
        """
        发送短信方法，其中
        @param mobile 手机号码，字符串，可以是多个手机号码，中间才用，隔开
        @param content 短信具体内容 
        """
        content += u'[娱讯&119互动平台]'
        if mobile.find(',') != -1:
            mobile_list = mobile[:-1]
        else:
            mobile_list = mobile
        result = self.client.service.mt(self.sn, self.md5pwd, mobile_list, content, '', '', '')
        stat = 0
        if len(result) > 3:
            stat = 1
        else:
            stat = 3
            
        sms_history().save_result(title, content, str(result), mobile_list, 0, stat, str(result))
        
        return result
    
    
    def reg_sms(self):
        result = self.client.service.Register(self.sn, self.pwd, self.province, self.city, self.trade, self.entname, self.linkman, self.phone, self.mobile, self.email, self.fax, self.address, self.postcode, self.sign)
        return result
    
    def balance(self):
        result = self.client.service.balance(self.sn, self.md5pwd)
        return result