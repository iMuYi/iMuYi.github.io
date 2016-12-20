# -*- coding:utf-8 -*-
import MySQLdb
import os
import re
import time
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
db = MySQLdb.connect("103.37.161.243", "imuyi", "admin",
                     "crawl_data", charset="utf8")
cursor = db.cursor()
newfile = "Job.md"
filename = os.path.abspath(__file__)
filepath = filename.split("\\")
parentpath = "\\".join(filepath[:-1])
filename = parentpath + "\\" + newfile
f = open(filename, 'w')
sql = "select title,url,time from bbs"
cursor.execute(sql)
data = cursor.fetchall()
insert = """---
title: Job
date: %s
tags: Job
categories: Job
---
这是爬取自北邮人论坛的招聘信息，点击即可跳转到北邮人论坛。\n
time: %s\n
<!--more-->\n"""%(datetime.datetime.now(),datetime.datetime.now())
f.write(insert)
i = 0
for each in data:
    if i == 0:
        insert = "[<font color=red>" + each[0] + \
            "</font>](" + each[1] + ")\n"
        i = 1
    else:
        insert = "[<font color=blue>" + each[0] + \
            "</font>](" + each[1] + ")\n"
        i = 0
    f.write(insert)

f.close()
