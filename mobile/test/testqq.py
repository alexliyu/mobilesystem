#-*- coding:utf-8 -*-
import urllib2
import urllib
import re, time
import cookielib
import hashlib
import base64
import os 
import random

username = '2502093450@qq.com'

password = 'eii5166918'

"""
根据用户名生成用于存放cookies的文件
"""
filepath = os.path.normpath(os.path.dirname(__file__))
cookiefile = os.path.join(filepath, 'qq_%s' % username)


def md5hash(str):
    return hashlib.md5(str).digest()
def hex_md5hash(str):
    return hashlib.md5(str).hexdigest().upper()
def md5hash_3(str):
    return hex_md5hash(md5hash(md5hash(str)))

def EncodePasswordWithVerifyCode(pwd, verifyCode):
    return hex_md5hash(md5hash_3(pwd) + verifyCode.upper())
                            
def get_password(password, verifyCode):
    """
    根据明文密码计算出加密后的密码
    """
    return hex_md5hash(md5hash_3(password) + verifyCode.upper())

def get_username(username):
    return base64.encodestring(urllib.quote(username))[:-1]


def send_post(cookies):
    
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    
    opener.addheaders = [('User-agent', 'Opera/9.23')]  
    
    urllib2.install_opener(opener)
    
    url = 'http://t.qq.com/publish.php?rnd=%s' % random.random()
    formdata = {"content":'12345678900000', "pic":'', "countType":'', "viewModel":'1'}
    post_data = urllib.urlencode(formdata)

    send = urllib2.Request(url, post_data)
    send.add_header("Referer", "http://t.qq.com")
    
    """
    发布微博
    """
    conn = urllib2.urlopen(send)
    
    """
    判断是否发送成功，即如果发布微博后获取到的正文内容中有A00006，则表明发布成功了，反之则不成功
    """
    if re.findall('广播成功', conn.read(), re.I):
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
    verifyURL = 'http://ptlogin2.qq.com/check?uin=%s&appid=46000101&r=%s' % (username, random.random())
    loginURL = 'http://ptlogin2.qq.com/login?'
    redirectURL = ''
    qqn = username
    md5Pass = ''
    verifyCode = ''

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
    loginURL += get_password(password, verifyCode)
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


mylogin = get_login()
if mylogin:
    send_post(mylogin)
else:
    print "something is wrong"
