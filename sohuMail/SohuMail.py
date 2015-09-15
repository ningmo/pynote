#!/usr/bin/python
#coding:utf-8
import datetime,re,time
import requests
import sys
import MySQLdb

class SohuMail(object):
    """sohu邮件发送类"""
    curDate = ''
    oldDate = ''

    def __init__(self):
        object.__init__(self)
        self.curDate = datetime.datetime.now()
        self.oldDate = datetime.datetime.now() - datetime.timedelta(days=90)

    def connectDatabase(self):
        try:
            conn = MySQLdb.connect(host="10.10.102.60",user="root",passwd="root",db="yymail",charset="utf8")
        except Exception,e:
            print 'connect database Error'
            sys.exit()
        else:
            cur = conn.cursor()
            return cur

    def getData(self, type='new', nums=10000):
        cur = self.connectDatabase()
        if type=='old':
            sql = 'select fs_qq from t_qq where ft_time < "%s" and length(fs_qq)>4 order by ft_time desc limit 0,%s' % (self.oldDate, nums)
        else:
            sql = 'select fs_qq from t_qq where ft_time > "%s" and  ft_time < "%s" and length(fs_qq)>4 order by ft_time desc limit 0,%s' % (self.oldDate, self.curDate, nums)
        cur.execute(sql)
        search = cur.fetchall()
        list = [l[0] for l in search if l[0]]
        return list


sohu = SohuMail()
sohu.getData()