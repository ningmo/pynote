#!/data/env/py27/bin/python
#coding:utf-8
__author__ = 'yang'
import MySQLdb
import datetime
import sys
import redis
import json

def connectDatabase():
    try:
        conn = MySQLdb.connect(host="10.10.102.60",user="root",passwd="root",db="lastgbi",charset="utf8")
    except Exception,e:
        print 'Connect Database Error!'
        sys.exit()
    else:
        cur = conn.cursor()
        return cur

def getGoodsId():
    attr = [#{'id':331,'img':'','mark':'首页左导航推广'},
            {'id':332,'img':'index_small_img','mark':'首页flash下推广'},
            {'id':333,'img':'list_big_img','mark':'列表页上部大图推广'},
            #{'id':334,'img':'','mark':'Search页推广'},
            {'id':336,'img':'index_big_img','mark':'首页大图flash推广'},
            {'id':337,'img':'hot_img','mark':'首页热门区推广'},
            {'id':338,'img':'new_lei_img','mark':'首页下分类推广'},
            {'id':340,'img':'list_small_img','mark':'列表页推广'},
            {'id':341,'img':'left_img','mark':'首页商标分类推广左侧图片幻灯推广'}
    ]
    today = datetime.date.today()
    sql = 'select ga.goods_id from ecs_goods g left join ecs_goods_attr ga on ga.goods_id=g.goods_id where g.is_delete = 0  AND g.is_on_sale=1 and ga.attr_value >= "%s" and ga.attr_value <= "%s" ' % (today-datetime.timedelta(days=2),today)
    cur = connectDatabase()
    idList = []
    for k in attr:
        sqls = sql + 'and ga.attr_id=%s and g.%s is not null '  % (k['id'],k['img'])
        cur.execute(sqls)
        r = cur.fetchall()
        idList.extend([i[0] for i in r if i[0]])
    return idList

def sendMail():
    idList = getGoodsId()
    if len(idList) <1:
        sys.exit(0)
    idList = [str(i) for i in idList]
    msg = {}
    msg['to'] = ['ysf@gbicom.org']
    msg['subject'] = '商标超市--商标推广到期提醒'
    msg['body'] = '2天内即将到期的商标GoodsID : '+ ' '.join(idList)

    r = redis.StrictRedis(host='127.0.0.1',port=6379,db=10)
    print r.lpush('mailqueue',json.dumps(msg))

if __name__ == '__main__':
    sendMail()


