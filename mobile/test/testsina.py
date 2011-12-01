#-*- coding:utf-8 -*-
import urllib2
import urllib
import re, time
import cookielib
import hashlib
import base64
import os 
import random

username = 'liy@eiimedia.cn'

password = '123456'

"""
根据用户名生成用于存放cookies的文件
"""
filepath = os.path.normpath(os.path.dirname(__file__))
cookiefile = os.path.join(filepath, 'sina_%s' % username)



def get_password(password, servertime, nonce):
    """
    根据明文密码计算出加密后的密码
    """
    pass1 = hashlib.sha1(password).hexdigest()
    pass2 = hashlib.sha1(pass1).hexdigest()
    pass3 = pass2 + servertime + nonce
    pass4 = hashlib.sha1(pass3).hexdigest()
    
    return pass4

def get_username(username):
    return base64.encodestring(urllib.quote(username))[:-1]


def send_post(cookies):
    
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    
    opener.addheaders = [('User-agent', 'Opera/9.23')]  
    
    urllib2.install_opener(opener)
    
    url = 'http://weibo.com/aj/mblog/add?__rnd=%s' % random.random()
    formdata = {"text":'12345678900000', "pic_id":'', "location":"home", "module":"stissue", "_t":'0'}
    post_data = urllib.urlencode(formdata)

    send = urllib2.Request(url, post_data)
    send.add_header("Host", "weibo.com")
    send.add_header("Referer", "http://weibo.com/eiimedia")
    
    """
    发布微博
    """
    conn = urllib2.urlopen(send)
    
    """
    判断是否发送成功，即如果发布微博后获取到的正文内容中有A00006，则表明发布成功了，反之则不成功
    """
    if re.findall('100000', conn.read(), re.I):
        return True
    else:
        return False
    
def get_login(update=False):
    cookies = cookielib.MozillaCookieJar(cookiefile) 
    try:
        """加载已存在的cookie，尝试此cookie是否还有效"""
        cookies.load(ignore_discard=True, ignore_expires=True)
        if not update:
            return cookies
    except Exception, e:
        """加载失败，说明从未登录过，需创建一个cookie kong 文件"""
        cookies.save(cookiefile, ignore_discard=True, ignore_expires=True)
    """
    算出用户名加密后的字符串
    """
    su = get_username(username)

    url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&client=ssologin.js(v1.3.16)&_=%s' % (su, str(time.time()).replace('.', ''))

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    
    opener.addheaders = [('User-agent', 'Opera/9.23')]  
    
    urllib2.install_opener(opener)
    """
    获取初次加密所需要的两个关键参数值
    """
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    
    """
    获取两个用来获得令牌的关键参数。这是由服务器生成的，如果获取不到，那么则是代表登录出现问题
    """
    try:
        serverdata = re.findall('{"retcode":0,"servertime":(.*?),"nonce":"(.*?)"}', response.read(), re.I)[0]
    except:
        return False
    
    """
    服务器时间
    """
    servertime = serverdata[0]
    
    """
    随机密钥
    """
    nonce = serverdata[1]
    
    """
    获得加密后的密码
    """
    sp = get_password(password, servertime, nonce)

    """
    准备获取登录令牌所需要提交的数据
    """
    formdata = {"entry" : 'weibo', "gateway" : '1', "from" : "", "savestate" : '7', "useticket" : '1', "ssosimplelogin" : '1', "su" : su, "service" : 'miniblog', "servertime" : servertime, "nonce" : nonce, "pwencode" : 'wsse', "sp" : sp, "encoding" : 'utf-8', "url" : 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack', "returntype" : 'META'}

    url2 = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.16)'
    post_data = urllib.urlencode(formdata)

    req = urllib2.Request(url2, post_data)
    
    """
    获取登录令牌第一部分
    """
    conn = urllib2.urlopen(req)

    """
    访问微博真实登录地址，获取登录令牌第二部分——最后补全的cookies,如果不能获取，则代表登录出现问题
    """
    try:
        serverdata2 = re.findall(r"{location.replace\('(.*)\'", conn.read(), re.I)[0]
    except:
        return False
    
    req2 = urllib2.Request(serverdata2)

    """
    获得完整的登录令牌
    """
    conn2 = urllib2.urlopen(req2)

    urllib.urlopen('http://weibo.com')
    
    """
    保存成功的cookie到文件中去
    """
    cookies.save(cookiefile, ignore_discard=True, ignore_expires=True)
    
    return cookies


mylogin = get_login()
if mylogin:
    send_post(mylogin)
else:
    print "something is wrong"
