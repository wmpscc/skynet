#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests


r=requests.get(url="https://www.baidu.com/")

a = 12

print "Content-type:text/html"
print
print r.status_code
print a