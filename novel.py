#!/usr/bin/python
# encoding=utf8
import MySQLdb
from pyquery import PyQuery as pq
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def main():
    base = 'http://www.dhzw.org/'
    listObj = pq(url='http://www.dhzw.org/sort1/1.html')
    listObj = listObj('.l ul li .s2 a').items()
    for a in listObj:
        novleHref = a.attr('href')
        novleName = a.text()
        arcListObj = pq(url=novleHref)
        author = arcListObj('.infotitle i').eq(0).text()
        arcArea = arcListObj('.box_con #list dd a').items()
        desc = arcListObj('.intro').text()
        sql = 'insert into nv_novel_list set title="%s",author="%s",cat_id="%s",`desc`="%s";' % (iconv(novleName),iconv(author),'1',MySQLdb.escape_string(iconv(desc)))
        id = insert(sql,True)
        print id,iconv(novleName)
        for aa in arcArea:
            arcHref = novleHref + aa.attr('href')
            arcName = aa.text()
            try:
                print '     ',iconv(arcName),arcHref
                conObj = pq(url = arcHref)
                con = conObj('#BookText').text()
                sql = 'insert into nv_novel_article set title="%s",content="%s",novel_id="%s";' % (iconv(arcName), MySQLdb.escape_string(iconv(con)), id)
                insert(sql)
            except UnicodeDecodeError:
                pass

def insert(sql,id=False):
    db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456', db='novel',charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    if id:
        cursor.execute('select novel_id from nv_novel_list order by novel_id desc')
        data = cursor.fetchone()
        return data[0]

def iconv(str):
    return str.encode('iso-8859-1').decode('gbk').encode('utf-8')

main()
