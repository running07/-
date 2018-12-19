# -*- coding: utf-8 -*-
import re
import urllib
# url='https://search.jd.com/Search?keyword=%E7%8F%A0%E5%AE%9D&enc=utf-8'
# ret = re.search(r'keyword=(.+)&', url)
# keyword = ret.group(1)
# print keyword

import chardet
# mstr='手机'
# # print chardet.detect(mstr)
# nstr='%E7%8F%A0%E5%AE%9D'
# nstr= nstr.encode('utf-8')
# print nstr
# # print chardet.detect(nstr)
#
# s=urllib.unquote(nstr)
# print s
# url='//health.jd.com'
# url='//channel.jd.com/1315-1342.html'
# if 'html'in url:
#     ret=re.search(r'jd.com/(.+).html',url)
# else:
#     ret=re.match('//(\w+)',url)
# print ret.group(1)
from selenium import webdriver
import time
# driver=webdriver.Chrome()
# driver.get('https://www.baidu.com/')
# driver.find_element_by_id('kw').send_keys(u'鹿晗')
# driver.find_element_by_id('su').click()
# time.sleep(5)
import shutil
shutil.copyfile(f)