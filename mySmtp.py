#!/usr/bin/python
# -*- coding: utf8 -*-
### 调用  python .py 1-type(dev/main) 2-path 3-appendMail(me)
import smtplib, operator
import os,re,sys,time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from MySqlHelper import *
import thread

def sendmail(id,you,subject,content):
    me = "中细软知识产权 <gbicom@gbicom.cn>"
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you
    #text/plain and text/html
    part2 = MIMEText(content, 'html', "utf8")

    msg.attach(part2)
    s = smtplib.SMTP('127.0.0.1')
    s.login("mailuser", "111222")
    #s.set_debuglevel(1)
    s.sendmail(me, you, msg.as_string())
    s.quit()
    print '线程',id,":send mail to:",you

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

def main(id,paths,index=30000):
    start = (id-1)*index
    stop  = id*index
    sql = "select fs_qq from t_qq limit %d,%d" % (start,stop)
    maillist = MySqlHelper.FetchSql("127.0.0.1",'root','rgsh-xyrh#3Q','test',sql)
    print sql
    if(len(maillist))<1:
        thread.exit_thread()
    else:
        subject=u"[AD]中细软知识产权周报--第002期"
        fch = open(paths)
        content = fch.read()
        fch.close()
        for m in maillist:
            try:
                #if checkEmail(m[0]):
                mail = "%s@qq.com" % m[0]
                #sendmail(id,mail,subject,content)
            except UnicodeEncodeError,err:
                print 'error:',m
            except smtplib.SMTPRecipientsRefused, err:
                fh = open("domaens.txt", "a")
                fh.write("%s\n" % m[0])
                fh.close()
        thread.exit_thread()

def dev(id,paths,index=30000):
    subject=u"[AD]中细软知识产权周报"
    fch = open(paths)
    content = fch.read()
    fch.close()

    mailto=["251809397@qq.com"]
    for to in mailto:
       try:
           #if checkEmail(to):
           sendmail(id,to,subject,content)
       except smtplib.SMTPRecipientsRefused, err:
           u, domaen = re.split("@", to)
           fh = open("domaens.txt", "a")
           fh.write("%s\n" % domaen)
           fh.close()
    thread.exit_thread()

if __name__ == "__main__":
    ###################参数确认####################
    #当前文件名  发送类型    邮件内容路径
    parms = sys.argv
    fileName, types,     paths = parms
    if(types != 'main'):
        type= 'dev'
        if(types == 'main'):
            print '模式：正式发送模式'
        else:
            print '模式：调试模式'

    if(not os.path.isfile(paths)):
        print '邮件内容不存在'
        exit()
    else:
        print '发送邮件内容路径',paths
    sure = raw_input('请仔细核对以上信息，是否确认发送(yes/no)：');
    if(sure not in ('yes','y')):
        print '程序终止'
        exit()


    def ctl(types,paths):
        fun = eval(types)
        for ii in range(1,20):
            time.sleep(1)
            thread.start_new_thread(fun, (ii,paths))

    ctl(types,paths)
    ################线程创建##############单个线程3W数据
### 调用  python .py 1-type(dev/main) 2-path 3-appendMail(me)