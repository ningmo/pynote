#!/usr/bin/python
#coding:utf-8
__author__ = 'yangsf'
import threading
import time
exitFlag = 0
class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, nums=30000):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = nums
    def run(threadID,nums):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print threadID,nums
        #print_time(self.name, self.counter, 100)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            thread.exit()
        print "%s: %s" % (threadName, time.time())
        counter -= 1
"""
# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# 开启线程
thread1.start()
thread2.start()
print "Exiting Main Thread"
"""

