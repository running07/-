# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdredisspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #数据库名
    db = scrapy.Field()
    #品牌
    brand = scrapy.Field()
    #品牌地址
    brand_url = scrapy.Field()
    dir = scrapy.Field()
    #商品地址
    goods_url = scrapy.Field()
    #商品图片地址
    img_url = scrapy.Field()
    #商品价格
    price = scrapy.Field()
    #商品名称
    name = scrapy.Field()
    #商品参数
    parameter=scrapy.Field()
    #商品评论数
    comment = scrapy.Field()
    #商品店铺
    store = scrapy.Field()
