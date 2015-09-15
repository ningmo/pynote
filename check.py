#encoding:utf-8
__author__ = 'yang'

"""
    网站运行监测
    执行计划任务 定时检测网页内容 出现异常时 及时发出警告提醒
    域名：时间 状态
    响应：匹配指定 匹配长度
"""
import requests
import datetime
import sys
import re
import os
import re
warningMsg = ['网站监测警告信息']

def app():
    list = {
        'gbicom':{
            'domain'    : ['http://www.gbicom.cn' , 'http://jy.ipr123.com'],
            'content'   : ['<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />' , '中华商标超市网' , '旗下网站','<div class="block"></div>'],
            'cdn' : {
                'randUrl'   : ['http://cdn0.gbicom.cn','http://cdn1.gbicom.cn','http://cdn2.gbicom.cn','http://cdn3.gbicom.cn','http://cdn4.gbicom.cn','http://misc.gbicom.cn'],
                'sourceUrl' : ['http://misc.gbicom.cn/themes/images/gbicom_01.png','http://misc.gbicom.cn/themes/css/index.css','http://misc.gbicom.cn/themes/js/jquery-1.7.2.js']
            },
            'data':'http://www.gbicom.cn/ajax/addProxyBuy?customer=%E4%BA%A4%E6%98%93%E6%B5%8B%E8%AF%95&telephone=13211112222&price=10000&qq=123456&brandname=%E5%BE%B7%E6%9E%97%E5%BA%84%E5%9B%AD&product=181657&brandtype=%E7%AC%AC33%E7%B1%BB'
        },
        'vip':{
            'domain'    : ['http://vip.gbicom.cn' , 'http://v.ipr123.com'],
            'content'   : ['国内商标' , '国际商标' , '专利服务','版权服务','商标超市','其他服务','领证通知','商标注册4大理由','公司简介'],
            'cdn' : {
                'randUrl'   : ['http://vip-cdn0.gbicom.cn'],
                'sourceUrl' : ['http://vip-cdn0.gbicom.cn/Public/css/style.css']
            },
            'date':'http://vip.gbicom.cn/saveData?brandCate=1&brandName=VIP%E6%B5%8B%E8%AF%95&userName=VIP%E6%B5%8B%E8%AF%95%E4%BF%A1%E6%81%AF&mobile=13211112222&qq=123456'
        },
        'zl':{
            'domain'    : ['http://zl.gbicom.cn' , 'http://zl.ipr123.com'],
            'content'   : ['国内商标' , '国际商标' , '专利服务','版权服务','商标超市','其他服务','外观专利申请','发明专利申请','专利申请流程'],
            'cdn' : {
                'randUrl'   : ['http://zl-cdn.gbicom.cn'],
                'sourceUrl' : []
            },
            'data':'http://zl.gbicom.cn/saveData?apply_type=PPOIReg&apply_area=%E6%9C%BA%E6%A2%B0&apply_name=ZL%E6%B5%8B%E8%AF%95&designer=ZL%E6%B5%8B%E8%AF%95%E4%BF%A1%E6%81%AF&telphone=13211112222'
        },
        'bq':{
            'domain'    : ['http://bq.gbicom.cn' , 'http://bq.ipr123.com'],
            'content'   : ['国内商标' , '国际商标' , '专利服务','版权服务','商标超市','其他服务','作品版权','著作权','版权登记'],
            'cdn' : {
                'randUrl'   : ['http://bq-cdn0.gbicom.cn'],
                'sourceUrl' : []
            },
            'data':'http://g.gbicom.cn/ajax_commit?country=%E9%A9%AC%E5%BE%B7%E9%87%8C%E5%9B%BD%E9%99%85%E6%B3%A8%E5%86%8C&cate=%E7%AC%AC01%E7%B1%BB-%E5%8C%96%E5%AD%A6%E5%8E%9F%E6%96%99&brand_name=G%E6%B5%8B%E8%AF%95&link_man=G%E6%B5%8B%E8%AF%95%E4%BF%A1%E6%81%AF&link_phone=13211112222'
        },
        'global':{
            'domain'    : ['http://g.gbicom.cn' , 'http://g.ipr123.com'],
            'content'   : ['国内商标' , '国际商标' , '专利服务','版权服务','商标超市','其他服务','选择中细软','联系方法'],
            'cdn' : {
                'randUrl'   : ['http://global-cdn.gbicom.cn'],
                'sourceUrl' : []
            },
            'data':'http://bq.gbicom.cn/ajax_commit?type=%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%BD%AF%E4%BB%B6%E8%91%97%E4%BD%9C%E6%9D%83%E7%99%BB%E8%AE%B0&desc=BQ%E6%B5%8B%E8%AF%95&link_man=BQ%E6%B5%8B%E8%AF%95%E4%BF%A1%E6%81%AF&link_phone=13211112222&link_qq=123456'
        },
    }
    for item in list.items():
        print
        print '%s 页面检测开始' % getTime()
        pageCon = ''
        for url in item[1]['domain']:
            #print '%s 开始检测 %s ' % (getTime(),url)
            req = openSource(url)                   ## 打开资源
            pageCon = req.content
            ckeckDomain(req)                       ## 检测站点域名状态
            checkContent(req,item[1]['content'])   ## 从内容匹配关键字
        checkCdn(item[1]['cdn'],pageCon)            ## 检测cdn资源
        #print item[1]['data']                      ## 表单测试暂存在问题 不开启
        #r =  checkForm(item[1]['data'])
        #print r.url,r.status_code

"""
    t=1 网页类型 状态码code必须200
    t=2 资源类型 code需求200-399 200 301 302...
"""
def ckeckDomain(req,t=1):
    print
    shortUrl = req.url[7:-1]
    print u'%s 域名检测 Ping %s' % (getTime(),shortUrl)
    pingRes = os.popen('ping -c 5 '+ shortUrl)
    regTime = re.compile('time=(.*) ms')
    pingCon = pingRes.read()
    pingRes.close()
    pingTimeList = regTime.findall(pingCon)
    print pingCon
    print pingTimeList
    if eval(max(pingTimeList)) > 3000:
        print u'%s ping 最大时间 %s 大于 3000ms 重新ping' % (getTime(),max(pingTimeList))
        pingRes = os.popen('ping -c 5 '+ shortUrl)
        regTime = re.compile('time=(.*) ms')
        pingCon = pingRes.read()
        pingRes.close()
        pingTimeList = regTime.findall(pingCon)
        if eval(max(pingTimeList)) > 3000:
            if eval((min(pingTimeList) + max(pingTimeList))/2) > 3000:
                warningMsg.append(u'%s ping 时间过大 ' % (shortUrl))
    print u'%s 检测域名状态' % getTime()
    if t==1:
        if req.status_code !=200:
            warningMsg.append(u'域名%s响应状态 %s 异常' % (shortUrl,req.status_code))
            print u'%s %s状态码异常 %s' % (getTime(),shortUrl,req.status_code)
        else:
             print u'%s %s状态码 %s' % (getTime(),shortUrl,req.status_code)
    if t==2:
        if req.status_code >=400:
            warningMsg.append(u'域名%s响应状态 %s 异常' % (shortUrl,req.status_code))
        else:
             print u'%s %s状态码 %s' % (getTime(),shortUrl,req.status_code)
    print u'%s %s域名检测完毕' % (getTime(),shortUrl)

# 检测内容 匹配关键字
def checkContent(req,con):
    print
    print u'%s %s开始检测内容' % (getTime(),req.url)
    cnt = 0
    print u'%s 关键词：%s' % (getTime(),con)
    for c in con:
        if req.content.find(c) > -1:
            cnt = cnt +1
    print '%s 关键词匹配结果 %s/%s'   % (getTime(),cnt,len(con))
    if cnt != len(con):
        warming('%s关键词匹配不足 %s/%s' % (req.status_code,cnt,len(con)))

"""
    cdn检测  检测资源状态
"""
def checkCdn(cdn,con):
    print
    print '%s 开始抽样检测cdn资源' % getTime()
    print cdn
    for u in cdn['randUrl']:
        preg = r'(%s.*\.[a-zA-Z]{2,3})[\"?\'?]' % u
        cdnList = re.findall(preg,con)
        randSource(cdnList + cdn['sourceUrl'])

# 挑选部分cdn进行检测
def randSource(sourceList):
    for i in range(0,len(sourceList)):
        if  not i%3:
            checkStaticFile(sourceList[i])

# 检测cdn资源状态
def checkStaticFile(url):
    req = openSource(url)
    if req.status_code != 200:
        wmsg = '%s 资源异常%s %s' % (getTime(),url,req.status_code)
        print wmsg
        print warming(wmsg)
    else:
        print '%s 检测资源 %s %s' % (getTime(),url,req.status_code)

# 检测表单
def checkForm(dataUrl):
    print '%s 检测表单提交功能' % getTime()
    d = dataUrl.split('?')
    return requests.post(d[0],data=d[1])

# 使用get打开一个网络资源
def openSource(url):
    return  requests.get(url)

# 警告信息追加
def warming(msg):
    warningMsg.append("%s %s" % (getTime(),msg))

# 发送警告
def sendWarming():
    print '||'.join(warningMsg)
    url = 'http://114.255.71.158:8061/?username=xrzg&password=xrzg&message=%s&phone=%s&epid=120188&linkid=&subcode=' % ('||'.join(warningMsg), '13716388217')
    print requests.get(url).content

# 返回当前时间
def getTime():
    return datetime.datetime.today()

if __name__ == '__main__':
    print '-'*20
    app()
    print
    if len(warningMsg) > 1 :
        print '%s 发送警告信息' % getTime()
        sendWarming()
    print '%s 检测完毕' % getTime()
    print '-'*20