# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
list1=[5,2,3]
list2=[2,4,5]
for i in list2:
    if i not in list1:
        list1.append(i)
print list1
# list3=list1+list2
# print list3
# list3=set(list3)
# print list3
# list3=list(list3)
# print list3