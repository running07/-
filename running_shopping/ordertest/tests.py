# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import time,random,datetime
print time.strftime('%m%d%H%M%S', time.localtime(time.time()))
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# print datetime.date
# list=['8', '9', '10', '11', '12', '29', '']
# nlist=[]
# for i in list:
#     if i:
#         nlist.append(int(i))
# print nlist