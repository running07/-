# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# class OrderDetailManagerInfo(models.Manager):
#     def create_orderdetail(self,goods,money,order):
#         detail=self.create(goods_id=goods,money=money,order_id=order)
#         return detail


# 订单
class OrderInfo(models.Model):
    oid = models.CharField(primary_key=True, max_length=20)  # 订单编号,主键
    odate = models.DateTimeField(auto_now=True)  # 创建日期
    statu = models.IntegerField()  # 订单状态
    omoney = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 订单总价
    oaddress = models.ForeignKey('usertest.UserAddressInfo')  # 收货地址
    ouser = models.ForeignKey('usertest.UserInfo')  # 订单用户

    class Meta():
        db_table = 'orderinfo'

    # def __str__(self):
    #     return self.pk.encode('utf-8')

    def str_statu(self):
        if self.statu == 0:
            return u'未支付'
        elif self.statu == 1:
            return u'已支付'
        elif self.statu == 2:
            return u'已收货'
        else:
            return u'已评价'
    # ststu_str.short_description('')


# 订单详情
class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('goodstest.GoodsInfo', default=0)  # 商品
    money = models.DecimalField(max_digits=8, decimal_places=2)  # 单件
    count = models.IntegerField()  # 商品数量
    order = models.ForeignKey(OrderInfo)  # 订单编号

    # def __str__(self):
    #     return self.pk.encode('utf-8')
    # orderdetail=OrderDetailManagerInfo()
    class Meta():
        db_table = 'orderdetailinfo'
