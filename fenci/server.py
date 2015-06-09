#encoding:utf-8

from wsgiref.simple_server import make_server
from fenci import application

# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('', 8088, application)
print('中文分词端口 Serving HTTP on port 8088...')
# 开始监听HTTP请求:
httpd.serve_forever()
