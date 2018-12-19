# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# 购物车
class CartInfo(models.Model):
    cuser = models.ForeignKey('usertest.UserInfo')  # 用户
    cgoods = models.ForeignKey('goodstest.GoodsInfo')  # 购物车商品
    count = models.IntegerField()  # 商品数量

    def __str__(self):
        return self.cgoods.gtitle.encode('utf-8')

    class Meta():
        db_table = 'cartinfo'
