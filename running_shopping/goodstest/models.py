# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# 富文本编译器，存放商品详情
from tinymce.models import HTMLField

'''
商品类别表的外键是商品         一对多
商品的外键是评论              一对一
'''


# 商品分类
# 新鲜水果      海鲜水产    猪牛羊肉    禽类蛋品    新鲜蔬菜    速冻食品
class CategoryInfo(models.Model):
    # 标题，逻辑删除
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=0)

    category = models.Manager()

    # 指定编码格式为utf-8 防止中文乱码
    def __str__(self):
        return self.ttitle.encode('utf-8')

    # 修改数据库表名
    class Meta():
        db_table = 'categoryinfo'


# 商品详情类
class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)  # 商品名称
    ggoods_info = models.CharField(max_length=100)  # 商品简介
    gimage = models.ImageField(upload_to='good_image/')  # 商品图片
    gweight = models.CharField(max_length=10, default='500g')  # 商品重量
    gprice = models.DecimalField(max_digits=5, decimal_places=2)  # 商品价格
    # gsales_volume=models.IntegerField()
    gclick = models.IntegerField(default=0)  # 商品点击量
    gintroduction = HTMLField(default='')  # 商品详情
    gstore = models.CharField(max_length=20)  # 商品商店
    isDelete = models.BooleanField(default=0)  # 是否删除
    gtype = models.ForeignKey(CategoryInfo)  # 商品类别

    goods = models.Manager()

    # 指定编码格式为utf-8 防止中文乱码
    def __str__(self):
        return self.gtitle.encode('utf-8')

    # 修改数据库表名
    class Meta():
        db_table = 'goodsinfo'


# 商品评论，和商品一对一
class CommentInfo(models.Model):
    content = models.CharField(max_length=200)  # 评论内容
    time = models.DateTimeField(auto_now=True)  # 评论时间
    likenum = models.IntegerField(default=0)  # 评论点赞数量
    dislikenum = models.IntegerField(default=0)  # 评论不喜欢数量
    grade = models.IntegerField(default=5)  # 评分
    goods = models.ForeignKey(GoodsInfo)  # 商品
    user = models.ForeignKey('usertest.UserInfo')  # 评论用户
