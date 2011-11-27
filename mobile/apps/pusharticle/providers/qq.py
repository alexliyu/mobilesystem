#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
import urllib2
import urllib
import re, time
import cookielib
import hashlib
import base64
import os 
import random
from datetime import datetime, tzinfo, timedelta
from xml.etree import ElementTree as ET


from conf.settings import batch


from apps.pusharticle.models import PushList, PushResult
from apps.entry.models import Entry
from apps.business.models import PromotionsInfo




class QqMsgsProvider(object):
    def __init__(self):
        self.push_objects = PushList.objects.filter(pushurl='send_qq_msgs', is_active=True)
        
    
    def send_business(self):
        """
        推送最新优惠资讯到qq微博的方法
        """
        try:
            entry = PromotionsInfo.objects.all().filter(id__gt=self.push_object.latest).order_by('id')[:1][0]
        except:
            return False

        self.messages = u'#厦门娱讯互动#%s,%s……查看全文%s' % (entry.title, entry.content[:40], 'http://www.5166918.com' + entry.get_absolute_url()) 
        self.messages = self.messages.encode('utf-8')
        self.send_id = entry.id
        self.send_title = entry.title
        
        return self.push_msg()
    
    
    def send_entry(self):
        """
        推送文章内容到新浪微博的方法
        """
        try:
            entry = Entry.published.all().filter(id__gt=self.push_object.latest).order_by('id')[:1][0]
        except:
            return False

        self.messages = u'#厦门#%s,%s……查看全文%s' % (entry.title, entry.excerpt[:40], entry.short_url) 
        self.messages = self.messages.encode('utf-8')
        self.send_id = entry.id
        self.send_title = entry.title
        
        return self.push_msg()
        
        
    def save_stat(self):
        
        self.push_object.latest = self.send_id
        self.push_object.last_retrieved = datetime.now()
        self.push_object.save(force_update=True)
        
        pushresult = PushResult.objects.create(title=self.send_title)
        pushresult.push_name = u'推送文章内容到腾讯微博'
        pushresult.push_stat = self.send_stat
        pushresult.save()
        
        
        
        
    def push_msg(self):
        
        mylogin = self.get_login(self.username, self.password, self.cookiefile)
        
        if not mylogin:
            mylogin = self.get_login(self.username, self.password, self.cookiefile, update=True)
        else:
            result = self.send_post(self.messages, mylogin)
        
        if result:
            self.send_stat = 1
            self.save_stat()
            return True
        else:
            self.send_stat = 2
            self.save_stat()
            return False
    
    @batch('*/2 * * * *')
    def send_data(self, metadata, output):
        """推送新浪微博主调用方法"""

        for push_object in self.push_objects:
            """
            遍历所有符合要求——即推送新浪微博的记录
            """
            time_check = push_object.last_retrieved + timedelta(seconds=push_object.pushtime)
            
            """
            检查上次推送时间与当前时间之间的间隔是否满足设置的推送间隔
            """
            if time_check < datetime.now():
                self.username = push_object.username
                self.password = push_object.password
                """
                根据用户名生成用于存放cookies的文件,规则是sina_用户名_id
                """
                self.filepath = os.path.normpath(os.path.dirname(__file__))
                self.cookiefile = os.path.join(self.filepath, 'qq_%s_%s' % (self.username, push_object.id))
                self.push_object = push_object
                result = getattr(self, push_object.category)()
                time.sleep(30)
            else:
                pass
                
        
        return metadata
    
    def md5hash(self, str):
        return hashlib.md5(str).digest()
    
    def hex_md5hash(self, str):
        return hashlib.md5(str).hexdigest().upper()
    
    def md5hash_3(self, str):
        return self.hex_md5hash(self.md5hash(self.md5hash(str)))


    def get_password(self, password, verifyCode):
        """
        根据明文密码计算出加密后的密码
        """
        return self.hex_md5hash(self.md5hash_3(password) + verifyCode.upper())
    
    
    def get_username(self, username):
        """
        根据明文用户名，计算出加密后的用户名
        """
        return base64.encodestring(urllib.quote(username))[:-1]
    
    
    def send_post(self, content, cookies):
        
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    
        opener.addheaders = [('User-agent', 'Opera/9.23')]  
        
        urllib2.install_opener(opener)
        
        url = 'http://t.qq.com/publish.php?rnd=%s' % random.random()
        formdata = {"content":content, "pic":'', "countType":'', "viewModel":'1'}
        post_data = urllib.urlencode(formdata)
    
        send = urllib2.Request(url, post_data)
        send.add_header("Referer", "http://t.qq.com")
        
        """
        发布微博
        """
        conn = urllib2.urlopen(send)
        
        """
        判断是否发送成功，即如果发布微博后获取到的正文内容中有广播成功，则表明发布成功了，反之则不成功
        """
        if re.findall('广播成功', conn.read(), re.I):
            return True
        else:
            return False
        
    def get_login(self, username, password, cookiefile, update=False):
        
        cookies = cookielib.MozillaCookieJar(cookiefile) 
        try:
            """加载已存在的cookie，尝试此cookie是否还有效"""
            cookies.load(ignore_discard=True, ignore_expires=True)
            if update or time.time() - os.stat(cookiefile).st_ctime > 18000:
                os.remove(cookiefile)
                cookies.save(cookiefile, ignore_discard=True, ignore_expires=True)
            else:
                return cookies
        except Exception, e:
            """加载失败，说明从未登录过，需创建一个cookie kong 文件"""
            cookies.save(cookiefile, ignore_discard=True, ignore_expires=True)
        """
        算出用户名加密后的字符串
        """
        verifyURL = 'http://ptlogin2.qq.com/check?uin=%s&appid=46000101&r=%s' % (username, random.random())
        loginURL = 'http://ptlogin2.qq.com/login?'
    
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
        
        opener.addheaders = [('User-agent', 'Opera/9.23')]  
        
        urllib2.install_opener(opener)
        """
        获取初次加密所需要的一个关键参数值
        """
        request = urllib2.Request(verifyURL)
        response = urllib2.urlopen(request)
        verifyCode = response.read()[18:-3]
        
        if len(verifyCode) > 4:
                return False
        """
        获取两个用来获得令牌的关键参数。这是由服务器生成的，如果获取不到，那么则是代表登录出现问题
        """
        loginURL += "u=%s&p=" % username
        loginURL += self.get_password(password, verifyCode)
        loginURL += "&verifycode=" + verifyCode + "&aid=46000101&u1=http%3A%2F%2Ft.qq.com&ptredirect=1&h=1&from_ui=1&fp=loginerroralert"
        
        req = urllib2.Request(loginURL)
        req.add_header('Referer', 'http://t.qq.com')
        
        """
        获取登录令牌第一部分
        """
        conn = urllib2.urlopen(req)
    
        """
        访问微博真实登录地址，获取登录令牌第二部分——最后补全的cookies,如果不能获取，则代表登录出现问题
        """
        urlhome = 'http://t.qq.com'
        
        req2 = urllib2.Request(urlhome)
    
        """
        获得完整的登录令牌
        """
        conn2 = urllib2.urlopen(req2)
        
        """
        保存成功的cookie到文件中去
        """
        cookies.save(cookiefile, ignore_discard=True, ignore_expires=True)
        
        return cookies
    
