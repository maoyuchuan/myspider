# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time

 

class JDlogin(object):
    def __init__(self,un,pw):
        self.headers = {'Host':"passport.jd.com",
		                'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
                        'Accept':"text/plain, */*; q=0.01",
                        'Accept-Encoding':"gzip, deflate, br",
                        'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                        'Connection':"keep-alive",
                        }
        self.session = requests.session()
        self.login_url = "http://passport.jd.com/uc/login"
        self.post_url = "http://passport.jd.com/uc/loginService"
        self.auth_url = "https://passport.jd.com/uc/showAuthCode"
        self.un = un
        self.pw = pw

    def get_authcode(self,url):
        self.headers['Host'] = 'authcode.jd.com'
        self.headers['Referer'] = 'https://passport.jd.com/uc/login'
        response = self.session.get(url, headers = self.headers)
        with open('authcode.jpg','wb') as f:
            f.write(response.content)
        authcode = raw_input("plz enter authcode:")
        return authcode

    def get_info(self):
        '''获取登录相关参数'''
        try:
            page = self.session.get(self.login_url, headers = self.headers)
            soup = BeautifulSoup(page.text, "html.parser")
            input_list = soup.select('.form input')

            data = {}
            data['uuid'] = input_list[0]['value']
            data['eid'] = input_list[4]['value']
            data['fp'] = input_list[5]['value']
            data['_t'] = input_list[6]['value']
            data['loginType'] = input_list[7]['value']
            rstr = input_list[8]['name']
            data[rstr] = input_list[8]['value']
            self.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=utf-8'
            self.headers['X-Requested-With'] = 'XMLHttpRequest'
            acRequired = self.session.post(self.auth_url, data={'loginName':self.un}, self.headers).text #返回({"verifycode":true})或({"verifycode":false})
            if 'true' in acRequired:
                print ('need authcode, plz find it and fill in ')
                acUrl = soup.select('.form img')[0]['src2']
                acUrl = 'http:{}&yys={}'.format(acUrl,str(int(time.time()*1000)))
                authcode = self.get_authcode(acUrl)
                data['authcode'] = authcode
            else:
                data['authcode'] = ''

        except Exception as e:
            print (e)
        finally:
            return data
    def login(self):
        
        postdata = self.get_info()
        postdata['loginname'] = self.un
        postdata['nloginpwd'] = self.pw
        postdata['loginpwd'] = self.pw
        try:
            self.headers['Referer'] = 'https://passport.jd.com/uc/login'
            self.headers['X-Requested-With'] = "XMLHttpRequest"
            self.headers['Content-Type'] = "application/x-www-form-urlencoded; charset=utf-8"
            login_page = self.session.post(self.post_url, data = postdata, headers = self.headers)
            print (login_page.text)  #若返回{“success”:”http://www.jd.com”}，说明登录成功
        except Exception as e:
            print (e)

if __name__=="__main__":
    username = raw_input("plz enter username:")
    password = raw_input("plz enter password:")
    JD = JDlogin(username,password)
    JD.login()