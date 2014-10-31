# -*- coding: utf8 -*-
__author__ = 'yang'

import os,re,MySQLdb
path = '/data/share/qq/'
fileList = os.listdir(path)
qqReg = r'Type="String">(\d{5,15})</Data'

conn=MySQLdb.connect(host="127.0.0.1",user="root",passwd="123456",db="test",charset="utf8")
cur = conn.cursor()

for f in fileList:
    h = open(path + f)

    pattern = re.compile(qqReg, re.I)
    qqList = pattern.findall(h.read())

    sqlLast = '("' + '"),("'.join(qqList) + '");'
    sql = 'insert into t_qq(fs_qq) values' + sqlLast
    print sql
    r = cur.execute(sql)
    print r
    exit()
    # insert into t_qq(fs_qq) values(111),(222);
