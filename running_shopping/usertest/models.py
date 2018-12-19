# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# 创建用户
class UserInfoManager(models.Manager):
    def create_user(self, name, pwd, mail):
        user = self.create(uname=name, upwd=pwd, umail=mail)
        return user


# 创建用户收货地址
class UserAddressInfoManager(models.Manager):
    def create_useraddress(self, another_name, recipients, pro, city, disc, address, postcode, addphone, user):
        useraddress = self.create(another_name=another_name, urecipients=recipients, upro=pro,
                                  ucity=city, udisc=disc, uaddress=address,
                                  upostcode=postcode, uaddphone=addphone, userid_id=user)
        return useraddress


# 用户类
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)  # 用户姓名
    upwd = models.CharField(max_length=40)  # 用户密码
    # ugender = models.BooleanField()

    umail = models.CharField(max_length=30)  # 用户邮箱
    goodsids = models.CommaSeparatedIntegerField(default='', max_length=40)  # 用户最经浏览商品id
    default_id = models.IntegerField(default=0)  # 收货地址id
    isDelete = models.BooleanField(default=0)  # 逻辑删除
    user = models.Manager()
    muser = UserInfoManager()

    # 指定编码格式，防止中文乱码
    def __str__(self):
        return self.uname.encode('utf-8')

    # 修改表名
    class Meta():
        db_table = 'userinfo'

    # def gender(self):
    #     if self.ugender:
    #         return '男'
    #     else:
    #         return '女'
    #
    # gender.short_description = 'sex'


# 用户地址类
class UserAddressInfo(models.Model):
    another_name = models.CharField(max_length=20)  # 别名
    urecipients = models.CharField(max_length=20)  # 收件人
    upro = models.IntegerField(default=0)  # 省份id
    ucity = models.IntegerField(default=0)  # 市id
    udisc = models.IntegerField(default=0)  # 区、镇id
    uaddress = models.CharField(max_length=80)  # 街道信息
    upostcode = models.CharField(max_length=6)  # 邮政编码
    uaddphone = models.CharField(max_length=20)  # 用户手机号
    userid = models.ForeignKey('UserInfo')  # 用户id

    useraddress = models.Manager()
    museraddress = UserAddressInfoManager()

    # 指定编码格式，防止中文乱码
    def __str__(self):
        return self.urecipients.encode('utf-8')

    # 修改表名
    class Meta():
        db_table = 'useraddressinfo'


# 区域表 自关联
class AreaInfo(models.Model):
    atitle = models.CharField(max_length=30)  # 区域名称
    aParea = models.ForeignKey('self', null=True, blank=True)  # 外键

    # 指定编码格式，防止中文乱码
    def __str__(self):
        return '%s' % self.atitle

    # 修改表名
    class Meta():
        db_table = 'areainfo'
