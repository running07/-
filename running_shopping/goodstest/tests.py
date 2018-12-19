# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# from django.test import TestCase
#
# class Encryption(object):
#     """整形数字简单的一个加密/解密算法"""
#     def encryption(self,num):
#         """对数字进行加密解密处理每个数位上的数字变为与7乘积的个位数字，再把每个数位上的数字a变为10-a．"""
#         newNum=[]
#
#         for i in str(num):
#             if int(i):
#                 newNum.append(str(10-int(i)*7%10))
#             else:
#                 newNum.append(str(0))
#
#         # print int(''.join(newNum))
#         return int(''.join(newNum))
#
#
#     def decryption(self,num):
#         """对数字进行解密处理，把每个数位上的数字乘以7再进行与10求余即可"""
#         oldNum=[]
#         [oldNum.append(str(int(i)*7%10)) for i in str(num)]
#         # print int(''.join(oldNum))
#         return int(''.join(oldNum))
#
#
#
# if __name__ == '__main__':
#     encryption=Encryption()
#     print encryption.encryption(100)
#     print encryption.decryption(300)


import hashlib

#
# # def get_md5(url):
#     """
#     由于hash不处理unicode编码的字符串（python3默认字符串是unicode）
#         所以这里判断是否字符串，如果是则进行转码
#         初始化md5、将url进行加密、然后返回加密字串
#     """
mlist = ['a', 'b', 'c', 'c']
# mlist.append('')
# mlist.insert(1,'z')
# mlist.pop()
# del mlist[1]
mlist.remove('b')
print mlist
# for index in range(page.number, page.number + 4)
