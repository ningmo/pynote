#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'moran'
import re,smtplib
import re
import operator 
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def sendEmail(to, sub='', content=''):
    usr = '10000000'
    server = 'qq.com'
    fr = usr + '@' + server
    myName = '我就是我<%s>' % fr
    if(sub==''):
        sub = '[AD]测试标题'
    if(content==''):
        content = 'laidian内容'
    
    passwd = 'passwd'
    
    msg = MIMEMultipart('alternative')
    msg['Subject']  = sub
    msg['From']     = fr
    msg['To']       = to
    
    part2 = MIMEText(content, 'html', "utf8")
    msg.attach(part2)
    
   
    
    s = smtplib.SMTP('smtp.'+server)
    s.login(usr, passwd)
    s.sendmail(fr, myName, msg.as_string())
    s.quit()
    print 'send to %s' % to
def checkEmail(email):
    mail = email.split('@')
    rs = re.match('\w{1,20}',mail[0])
    if(rs):
        last = mail[1].split('.')
        if(len(last[0] and  last[1])):
            return True
    return False
sendEmail('2000000@qq.com')
