#encoding=utf-8
__author__ = 'yang'
import jieba
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')  

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    body = environ['PATH_INFO'][1:]
    l = jieba.cut(body,cut_all=False)
    r = '--'.join(l)
    return [r.encode('utf-8')]
