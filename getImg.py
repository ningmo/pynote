#!/usr/bin/env python
# -*- coding: utf8 -*-
"""    
        抓取图片
    读取列表集  进入单页  分析单页内容  获取制定内容 保存
"""
import os
import urllib as u
import urllib2 as u2
import re
import random

#正则转换
def makeRegular(oneListUrlExmple):
    #先处理链接 生成正则
    oneListUrlExmple = oneListUrlExmple.lower()
    str1 = oneListUrlExmple.split('/')
    str2 =''
    str2T = []
    for i in str1:
        if(i.isalpha()):
            str2T.append(r'\w{1,%s}' % (len(i)+1))
        elif(i.isdigit()):
            str2T.append(r'\d{1,%s}' % (len(i)+1))
        else:
            prefix = i.split('.')
            str2M = []
            for ii in prefix:
                if(ii.isalpha()):
                    str2M.append(r'\w{1,%s}' % (len(ii)+1))
                elif(ii.isdigit()):
                    str2M.append(r'\d{1,%s}' % (len(ii)+1))
                else:
                    pass
                    #str2M.append(r'\/%s' % (i))
            str2T.append('\.'.join(str2M))
         
    preg = r'\/'.join(str2T) 
    return preg
#返回url列表
def getList(listUrl, oneListUrlExmple, keyword=''):
    preg = makeRegular(oneListUrlExmple)
    patten = re.compile(preg, re.I)     #    正则完成
    try:
        r = u2.urlopen(listUrl)
        listCon = r.read()
        r.close()
        macth = patten.findall(listCon)
        return macth
    except:
        print '列表打不开'
        exit()
def getFiles(pageUrl):
    savePath = './images/'
    if(os.path.exists(savePath) == False):
        os.mkdir(savePath)
    
    #打开单页
    try:
        r = u2.urlopen(pageUrl)
        pageCon = r.read()
        r.close()
    except:
        print pageUrl+'打不开'
        exit()
    
    pregImg = r'http\:\/\/up.*?jpg'
    part = re.compile(pregImg,re.I)
    r = part.findall(pageCon);
    def cbk(a, b, c):
        '''回调函数
        @a: 已经下载的数据块
        @b: 数据块的大小
        @c: 远程文件的大小
        '''
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        print '%.2f%%' % per

    for im in r:
        u.urlretrieve(im, '%s%s.jpg' % (savePath ,random.uniform(1, 200)), cbk)    # 保存
  
def main():
    listurl = ''
    oneListUrlExmple = '/2014/0721/23670.html'
    keyword = ''
    urllist = getList(listurl, oneListUrlExmple, keyword)
    for url in urllist:
        u = listurl + url
        getFiles(u)
    
main()
