#!/usr/bin/env python
# -*- coding: utf8 -*-
import smtplib
import os
import re
import operator
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from MySqlHelper import *

def sendmail(you,subject,content):
    me = "中细软知识产权 <gbicom@gbicom.cn>"
    #me = "mailuser@gbicom.com"
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you
    # Record the MIME types of both parts - text/plain and text/html.
#    part1 = MIMEText(text, 'plain',"utf8")
    part2 = MIMEText(content, 'html', "utf8")

    msg.attach(part2)
    #s = smtplib.SMTP('127.0.0.1')
    #s.login("gbimail", "111222333")
    s = smtplib.SMTP('127.0.0.1')
    s.login("mailuser", "111222")
    #s.set_debuglevel(1)
    s.sendmail(me, you, msg.as_string())
    s.quit()
    print "send mail to:",you

def checkEmail(mail):
    #regex = re.compile(r"^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$")
    regex = re.compile(r"^\d{5,12}$")
    ms = regex.match(mail)
    if ms:
        #u, domaen = re.split("@", mail)
        #if enabledDomaen(domaen):
        return True
        #else:
        #    return True
    else:
        return False

def enabledDomaen(domaen):
    domaens = ["000.net", "00.com", "0000000.net","gbicom.cn"]
    if os.path.exists("domaens.txt"):
        fh = open("domaens.txt","r")
        for line in fh:
            domaens.append(line.replace("\n",""))
        fh.close()
    return operator.contains(domaens, domaen)

def main():
    sql = "select fs_qq from t_qq"
    maillist = MySqlHelper.FetchSql("127.0.0.1",'root','rgsh-xyrh#3Q','test',sql)
    subject=u"[AD]中细软知识产权周报"
    path ="../w20141110_002/index.html"
    fch = open(path)
    content = fch.read()
    fch.close()
    for m in maillist:
        try:
            #if checkEmail(m[0]):
            mail = "%s@qq.com" % m[0]
            sendmail(mail,subject,content)
        except UnicodeEncodeError,err:
            print 'error:',m
        except smtplib.SMTPRecipientsRefused, err:
            fh = open("domaens.txt", "a")
            fh.write("%s\n" % m[0])
            fh.close()

def dev():
    subject=u"[AD]中细软知识产权周报"
    path ="../w20141110_002/index.html"
    fch = open(path)
    content = fch.read()
    fch.close()

    mailto=["251809397@qq.com"]
    for to in mailto:
       try:
           #if checkEmail(to):
           sendmail(to,subject,content)
       except smtplib.SMTPRecipientsRefused, err:
           u, domaen = re.split("@", to)
           fh = open("domaens.txt", "a")
           fh.write("%s\n" % domaen)
           fh.close()
if __name__ == "__main__":
    dev()
#    main()
