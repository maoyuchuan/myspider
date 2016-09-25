# -*- coding: utf-8 -*-

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
}
session = requests.session()
url = 'http://www.zhihu.com'
session.cookies = cookielib.LWPCookieJar(filename='cookies')

    
def login_cookie():
    try:
        session.cookies.load(ignore_discard=True)
        page = session.get(url, headers=headers).text
        pattern = re.compile(u'<a class="question_link"',re.S)
        result = re.search(pattern,page)
        if result:
            print(u'cookie登录成功')
        else:
            print(u'cookie登录失败，使用账号密码登录')
            return False
    except:
        print(u"Cookie 未能加载")
        return False
        
def login(account, secret):
    # 通过输入的用户名判断是否是手机号
    if re.match(r"^1\d{10}$", account):
        print(u"手机号登录" + u"\n")
        post_url = 'http://www.zhihu.com/login/phone_num'
        postdata = {
            '_xsrf': get_xsrf(),
            'password': secret,
            'remember_me': 'true',
            'phone_num': account,
        }
    else:
        if "@" in account:
            print(u"邮箱登录" + u"\n")
        else:
            print(u"你的账号输入有问题，请重新登录")
            return None
        post_url = 'http://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': get_xsrf(),
            'password': secret,
            'remember_me': 'true',
            'email': account,
        }
    try:
        # 不需要验证码直接登录成功
        login_page = session.post(post_url, data=postdata, headers=headers)      
    except:
        # 需要输入验证码后才能登录成功
        postdata["authcode"] = get_authcode()
        login_page = session.post(post_url, data=postdata, headers=headers) 
    session.cookies.save()        
    return session

def login_code(session):
    profile_url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(profile_url, headers=headers, allow_redirects=False).status_code
    if login_code == 200:
        print(u'登录成功')
    else:
        print(u'登录失败,请检查你的输入')
        
    
def get_xsrf():
    '''_xsrf 是一个动态变化的参数'''
    # 获取登录时需要用到的_xsrf
    index_page = session.get(url, headers=headers)
    html = index_page.text
    pattern = r'name="_xsrf" value="(.*?)"'
    # 这里的_xsrf 返回的是一个list
    _xsrf = re.findall(pattern, html)
    return _xsrf[0]
    
def get_authcode():
    t = str(int(time.time() * 1000))
    auth_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(auth_url, headers=headers)
    with open('authcode.jpg', 'wb') as f:
        f.write(r.content)
    authcode = raw_input("plz enter authcode:")
    return authcode
   
if __name__ == '__main__':
    if login_cookie() == False:
        username = raw_input("plz enter username:")
        password = raw_input("plz enter password:")
        session = login(username, password) 
        if session != None:
            login_code(session)
    
