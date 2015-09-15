#!/usr/bin/python
#coding:utf-8
import datetime,re,time
import requests
import MySQLdb
def sendMail(to):
    url = "http://sendcloud.sohu.com/webapi/mail.send_template.json"
    params = {
        "api_user": "ciprun",
        "api_key": "kcG3cQAGM0dclty7",
        "to": to,
        "from": "mail@gbicom.cn",
        "fromname": "中细软知识产权",
        "subject": "[AD]中细软电子微刊——智能商标管理软件《知库宝》全能上线，前1000名用户免费领用",
        "template_invoke_name": "week3_2",
        "substitution_vars": '{"to": ["%s"]}' % (to)
    }
    try:
        r = requests.post(url,files={}, data=params)
    except Exception,e:
        print '111'
    else:
        print "%s : %s" % (datetime.datetime.now(),r.text)

def checkMail(qq):
    r = re.findall(r"^\d{5,12}$",qq)
    if r:
        return True
    else:
        r2 = re.findall(r'\d{5,12}@\w{1,15}\.\w{1,10}',qq)
        if r2:
            return True
        else:
            return False

def connDatabase():
    try:
        #conn=MySQLdb.connect(host="127.0.0.1",user="yymail",passwd="YDJ2e8yW",db="yymail",charset="utf8")
        conn=MySQLdb.connect(host="10.10.102.60",user="root",passwd="root",db="yymail",charset="utf8")
        cur = conn.cursor()
        return cur
    except Exception,e:
        print 'Error : %s 链接数据库时产生异常(%s)' % (datetime.datetime.now(),e)

def getData(nums=8200):
    sqls = "select distinct fs_qq from t_qq where length(fs_qq)>=5 order by ft_time desc  limit 70,7200"
    cur = connDatabase()
    cur.execute(sqls)
    qqlist = cur.fetchall()

    sqls2 = "select distinct fs_qq from t_qq where length(fs_qq)>=5 and ft_time<'2014-11-01 00:00:00' order by ft_time desc  limit 0,2100"
    cur2 = connDatabase()
    cur2.execute(sqls2)
    qqlist2 = cur2.fetchall()
    qqlist = qqlist + qqlist2
    for m in qqlist:
        if checkMail(m[0]):
	    mailto = '%s@qq.com' % m[0]
	    print mailto
            sendMail(mailto)
            time.sleep(1)


def dev():
    qqlist = ['251809397']
    for m in qqlist:
        if checkMail(m):
            mailto = '%s@qq.com' % m
            sendMail(mailto)
            time.sleep(1)



if __name__ == '__main__':
#    getData()
    dev()
