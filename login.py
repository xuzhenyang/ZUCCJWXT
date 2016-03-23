# -*- coding: utf-8 -*-

import requests
import urllib
import urllib2
from bs4 import BeautifulSoup
import os
import getpass

#登陆界面发送get请求需要用到的headers
headers_get = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
}

#重定向前的url
loginUrl = 'http://10.61.2.3'
#重定向后获取的真实url
global trueUrl
#session
global session
#__VIEWSTATE
global viewstate
#验证码
global checkCodeUrl

global txtUserName
global TextBox2
global txtSecretCode

def getCheckCodeUrl(url):
    checkCodeUrl = ''
    for i in url.split('/')[:-1]:
        checkCodeUrl = checkCodeUrl + i
        checkCodeUrl = checkCodeUrl + '/'
    checkCodeUrl = checkCodeUrl + 'CheckCode.aspx'
    return checkCodeUrl

def getLoginData(url):
    try:
        req = urllib2.Request(url, None, headers_get)
        content = urllib2.urlopen(req)
        #获取真实url
        global trueUrl
        trueUrl = content.geturl()
        #print 'trueUrl : ' + trueUrl
        #获取session
        global session
        session = ''.join(trueUrl.split('/')[-2:-1])[1:-1]
        #print 'session : ' + session
        #获取CheckCodeUrl
        global checkCodeUrl
        checkCodeUrl = getCheckCodeUrl(trueUrl)
        #print 'checkCodeUrl : ' + checkCodeUrl
        #获取viewstate
        global viewstate
        soup = BeautifulSoup(content.read(), "html.parser")
        viewstate = soup.input.get('value')
        #print 'viewstate : ' + viewstate
    except urllib2.URLError,e:
        print 'error : ' + str(e.code) + ' ' + e.reason
        
def getData(url, headers):
    try:
        req = urllib2.Request(url, None, headers)
        content = urllib2.urlopen(req)
        return content.read()
    except urllib2.URLError,e:
        print 'error : ' + str(e.code) + ' ' + e.reason
        
def getCheckCodeImg():
    img = getData(checkCodeUrl, headers_get)
    f = file('checkCode.jpg', 'wb')
    f.write(img)
    f.close()
    
def login():
    global txtUserName
    global TextBox2
    global txtSecretCode
    global viewstate
    
    getCheckCodeImg()
    
    txtUserName = raw_input('Enter UserName : ')
    #使用getpass隐藏cmd中输入的密码
    TextBox2 = getpass.getpass('Enter UserPwd : ')
    txtSecretCode = raw_input('Enter CheckCode : ')
    
    postData = {
        '__VIEWSTATE' : viewstate,
        'txtUserName' : txtUserName,
        'TextBox2' : TextBox2,
        'txtSecretCode' : txtSecretCode,
        'RadioButtonList1' : '%D1%A7%C9%FA',
        'Button1' : '',
        'lbLanguage' : '',
        'hidPdrs' : '',
        'hidsc' : '',
    }

    headers_post = {
        'Host' : '10.61.2.3',
        'Connection' : 'keep-alive',
        'Content-Length' : '196',
        'Cache-Control' : 'max-age=0',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Origin' : 'http://10.61.2.3',
        'Upgrade-Insecure-Requests' : '1',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Referer' : 'http://10.61.2.3/(' + session + ')/',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'zh-CN,zh;q=0.8',
    }

    r = requests.post(trueUrl, data = postData, headers = headers_post)
    #r.url为返回的url链接，如果登陆成功 302重定向至首页，如果失败 重定向至登陆界面
    return r.url

def saveHtml(page):
    f = file('login.html', 'wb')
    f.write(page)
    f.close()
    
def run():
    while True:
        getLoginData(loginUrl)
        getCheckCodeImg()
        returnUrl = login()
        str = 'http://10.61.2.3/(' + session + ')/xs_main.aspx?xh=' + txtUserName
        #使用重定向的url来校验是否登陆成功
        if returnUrl == str:
            print 'login success ...'
            saveHtml(getData(str, headers_get))
            return str
        else:
            print 'Wrong info . Pls re-input info ...'
            continue

def main():
    while True:
        getLoginData(loginUrl)
        getCheckCodeImg()
        returnUrl = login()
        str = 'http://10.61.2.3/(' + session + ')/xs_main.aspx?xh=' + txtUserName
        #使用重定向的url来校验是否登陆成功
        if returnUrl == str:
            print 'login success ...'
            saveHtml(getData(str, headers_get))
            return str
        else:
            print 'Wrong info . Pls re-input info ...'
            continue

if __name__ == "__main__":
    main()
    