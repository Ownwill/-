# from gevent import monkey
# monkey.patch_all()
#
# import gevent
# import time
# import requests
#
# start_time = time.time()
#
# url_list = ['https://www.baidu.com/',
# 'https://www.sina.com.cn/',
# 'http://www.sohu.com/',
# 'https://www.qq.com/',
# 'https://www.163.com/',
# 'http://www.iqiyi.com/',
# 'https://www.tmall.com/',
# 'http://www.ifeng.com/'
# ]
#
# def crawler(url):
#     r = requests.get(url)
#     print(url,time.time(),r.status_code)
#
# #建立任务表
# tasks_list = []
#
# for url in url_list:
#     task = gevent.spawn(crawler,url)
#     tasks_list.append(task)
#
# gevent.joinall(tasks_list)
# end_time = time.time()
# print('总共花费时间%ss'%(end_time-start_time))



# # queue模块和协程配合
# from gevent import monkey
# monkey.patch_all()
#
# import gevent
# import time
# import requests
# from gevent.queue import Queue
#
# start = time.time()
#
# url_list = ['https://www.baidu.com/',
# 'https://www.sina.com.cn/',
# 'http://www.sohu.com/',
# 'https://www.qq.com/',
# 'https://www.163.com/',
# 'http://www.iqiyi.com/',
# 'https://www.tmall.com/',
# 'http://www.ifeng.com/']
#
# #模块实现跨greenlet工作的多生产者、多消费者队列
# work = Queue()
#
# #创建队列对象，并赋值给work
# for url in url_list:
#     #put_nowait函数可以把网址放进队列里
#     work.put_nowait(url)
#
# def crawler():
#     #队列不为空的话执行下面的代码
#     while not work.empty():
#         #取出url
#         url = work.get_nowait()
#         res = requests.get(url)
#         #获取网址、队列长度、请求状态码
#         print(url,work.qsize(),res.status_code)
#
# tasks_list = []
#
# #创建空任务列表
# for x in range(2):
#     #创建两个爬虫
#     task = gevent.spawn(crawler)
#     #用gevent.spawn()函数创建执行crawler()函数的任务
#     tasks_list.append(task)
# gevent.joinall(tasks_list)
# end = time.time()
# print(end - start)



#
from gevent import monkey
monkey.patch_all()

import gevent,time,requests
from bs4 import BeautifulSoup
from gevent.queue import Queue
import csv

url = 'https://book.douban.com/top250'
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}





