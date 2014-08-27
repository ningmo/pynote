#coding:utf-8
__author__ = 'yang'
import MySQLdb as m
import urllib as u
import json,time

conn = m.Connect(host="192.168.0.241",user="root",passwd="root#local",db="crm",charset="utf8")
cursor = conn.cursor()

n = cursor.execute("select fs_cellphone,fs_name from tci_customer where fs_cellphone like '1%' and ft_create_time < '2013-01-01 00:00:00' and  (`fs_name` like '%公司%' or `fs_name` like '%厂%' or `fs_name` like '%市%') limit 4700,5800 ")
rows =  cursor.fetchall()
b = []
print len(rows)
db = m.Connect(host="192.168.0.241",user="root",passwd="root#local",db="bonesite",charset="utf8")
cur = db.cursor()
for row in rows:
    url = "http://api.showji.com/Locating/www.show.ji.c.o.m.aspx?m="+ row[0] +"&output=json"
    r = u.urlopen(url).read()
    #exit()
    try:
        js = json.loads(r)
        s = "insert into customer set company='%s',prov='%s',city='%s';" % (row[1],js['Province'],js['City'])
        print s
        cur.execute(s)
        time.sleep(3)
    except:
        b.append(row[0])
        break
print '------------------------------------------------------'
print b