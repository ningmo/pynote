#!/usr/bin/python
# encoding=utf8
import MySQLdb
from pyquery import PyQuery as pq
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import cgi


def main():
    base = 'http://www.dhzw.org/'
    listObj = pq(url='http://www.dhzw.org/sort1/1.html')
    listObj = listObj('.l ul li .s2 a').items()
    for a in listObj:
        novleHref = a.attr('href')
        novleName = a.text().encode('iso-8859-1').decode('gbk').encode("utf8")
        arcListObj = pq(url=novleHref)
        author = arcListObj('.infotitle i').eq(0).text().encode('iso-8859-1').decode('gbk').encode("utf8")
        arcArea = arcListObj('.box_con #list dd a').items()
        desc = arcListObj('.intro').text().encode('iso-8859-1').decode('gbk').encode("utf8")
        sql = 'insert into nv_novel_list set title="%s",author="%s",cat_id="%s",desc="%s";' % (novleName,author,'1',cgi.escape(desc))
        id = insert(sql,True)
        print id,novleName
        for aa in arcArea:
            arcHref = base + aa.attr('href')
            arcName = aa.text().encode('iso-8859-1').decode('gbk').encode("utf8")
            conObj = pq(url = arcHref)
            con = conObj('#BookText').text().encode('iso-8859-1').decode('gbk').encode("utf8")
            print arcName.encode('iso-8859-1').decode('gbk')
            sql = 'insert into nv_novel_article set title="%s",content="%s",novel_id="%s";' % (arcName, MySQLdb.escape_string(con), '1')
            print sql
            insert(sql)


def insert(sql,id=False):
    db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456', db='novel',charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    if id:
        cursor.execute('select novel_id from nv_novel_list order by novel_id desc')
        data = cursor.fetchone()
        return data['novel_id']

main()
