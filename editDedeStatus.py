#coding:utf-8
__author__ = 'yang'
import MySQLdb as m
import time,string

config = [                                          \
            {'host':'192.168.8.241','user':'root','passwd':'root#local','dbname':'register','prefix':'register'},      \
                                                    \
        ]
curtime = int(str(time.time()).split('.')[0])

for c in config:
    try:
        # 获取最新的待审核文章中的一条
        conn = m.connect(host=c['host'],user=c['user'],passwd=c['passwd'],db=c['dbname'],charset='utf8')
        cursor = conn.cursor()
        sql = 'select id,pubdate,arcrank from %s_archives where arcrank=-1 and pubdate > %s order by id asc limit 1' % (c['prefix'],curtime-86400*5)
        cursor.execute(sql)
        row = cursor.fetchall()[0]
        print row

        upsql = "update %s_archives set pubdate=%s,arcrank=0  where id= %s" % (c['prefix'],curtime,row[0])
        print cursor.execute(upsql)

    except:
        pass










