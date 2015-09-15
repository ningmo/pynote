#coding:utf-8
__author__ = 'yang'
import MySQLdb
import sys
import time

fromIP = '10.10.102.60'
fromUser = 'root'
fromPwd = 'root'
fromName = 'vip'

toIP = '10.10.102.60'
toUser = 'root'
toPwd = 'root'
toName = 'iprbank'

def connectDatabase(ip,user,pwd,name,charset='utf8'):
    try:
        conn = MySQLdb.connect(host=ip,user=user,passwd=pwd,db=name,charset=charset)
    except Exception,e:
        print 'Connect %s Database  %s Error!' % (ip, name)
        sys.exit()
    else:
        cur = conn.cursor()
        return cur

def getData(ip,user,pwd,name,startID = '',nums=30):
    if startID == '' :
        sql = 'select * from zxzl_apply order by id desc limit 5'
    else:
        sql = 'select * from zxzl_apply where id > %s order by id asc limit 0,%s' % (startID,nums)
    cur = connectDatabase(ip,user,pwd,name)
    cur.execute(sql)
    list = cur.fetchall()
    return list

def compareData():
    toData = getData(toIP,toUser,toPwd,toName)
    maxID = max([l[0] for l in toData])
    fromData = getData(fromIP,fromUser,fromPwd,fromName,maxID)
    sqls = []
    for l in fromData:
        sql = 'insert into zxzl_apply(id,apply_name,designer,apply_type,telphone,QQ,content,apply_time,patent_cate,is_handle,email,apply_area,apply_zz,source) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % l
        sqls.append(sql)
    return sqls

if __name__ == '__main__':
    while True :
        sql = compareData()
        if(len(sql)>0):
            sql = ';'.join(sql)
            cur = connectDatabase(toIP,toUser,toPwd,toName)
            cur.execute(sql)
        else :
            time.sleep(600)
