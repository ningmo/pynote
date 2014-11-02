#coding:utf-8
__author__ = 'moran'
import urllib as u,urllib2 as u2,httplib,cookielib

def yueche():
    url = 'http://111.204.39.58:8080/DfssAjax.aspx'
    value = {'AjaxMethod':'LOGIN','.....':'........'}
    data = u.urlencode(value)
    req = u2.Request(url, data)
    try:
        response = u2.urlopen(req)
        loginR = response.read()
    except:
        pass
    else:
        if(loginR == 'success'):
            dateList = [('start=13&end=17&','date=2014-11-08','trainsessionid=03&'),
                        ('start=17&end=19&','date=2014-11-08','trainsessionid=04&')
                   ]
            for d in dateList:
                reqUrl = 'http://111.204.39.58:8080/Ajax/StuHdl.ashx?loginType=2&method=yueche&stuid=08281958&bmnum=BD14083100256&'
                reqUrl += d[0]           #TODO
                reqUrl += 'lessionid=001&trainpriceid=BD13040300001&lesstypeid=02&'
                reqUrl += d[1]            #TODO
                reqUrl += '&id=1&carid=&ycmethod=03&cartypeid=01&'
                reqUrl += d[2]         #TODO
                reqUrl += 'ReleaseCarID='
                print reqUrl
                Yreq = u2.Request(reqUrl);
                print Yreq
                Yresponse = u2.urlopen(Yreq)
                print Yresponse
                YR = Yresponse.read()
                if(YR == 'success'):
                    str = u'约车成功'
                    sendEmail(str)
        else:
            print 'login failed'


def sendEmail(con):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    sender = '***'
    receiver = '***'
    username = sender
    password = '***'
    subject = u'约车通知'
    smtpserver = 'smtp.163.com'

    msg = MIMEText(con,'html','utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

import time
for i in range(0,500):
    yueche()
    time.sleep(3)
