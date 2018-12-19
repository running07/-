# -*- coding: utf-8 -*-
import scrapy
import re
import time
import urllib
from lxml import etree
from selenium import webdriver
from JDRedisSpider.items import JdredisspiderItem
from scrapy_redis.spiders import RedisSpider


class JdredisSpider(RedisSpider):
    name = 'jdredis'
    redis_key = 'jdspider:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(JdredisSpider, self).__init__(*args, **kwargs)
    # 匹配京东商品类别，每种商品封装到一个数据库中，如手机、电脑、家居、食品
    def parse(self, response):
        menu_list = response.xpath('//li[@class="cate_menu_item"]/a/@href').extract()
        print menu_list
        # print len(menu_list)
        for link in menu_list:
            if 'html' in link:
                db = 'channel_' + re.search(r'jd.com/(.+).html', link).group(1)
            else:
                db = re.match(r'//(\w+)', link).group(1)
            print db
            item = JdredisspiderItem()
            item['db'] = db
            link = 'https:' + link
            yield scrapy.Request(link, callback=self.parse_menu, meta={'meta': item})
    # 爬取每个类别的分类，分别爬取，
    #response.xpath()爬取不到的list.html地址，用webdriver模拟浏览器，爬取标签链接
    def parse_menu(self, response):
        item_list = response.xpath(
            '//a[contains(@href,"keyword")]/@href|//a[contains(@href,"list.html")]/@href').extract()
        if not item_list:
            search_url = response.url
            driver = webdriver.PhantomJS()
            driver.get(search_url)
            html = driver.page_source
            selector = etree.HTML(html)
            item_list = selector.xpath('//a[contains(@href,"keyword")]/@href|//a[contains(@href,"list.html")]/@href')
        print item_list
        for link in item_list:
            if not link.startswith('http'):
                link = 'https:' + link
            yield scrapy.Request(link, callback=self.parse_brand, meta=response.meta)
    # 对每个小类别，爬取所有品牌，对每个品牌分别爬取
    def parse_brand(self, response):
        url_list = response.xpath('//li[contains(@id,"brand")]/a/@href').extract()
        title_list = response.xpath('//li[contains(@id,"brand")]/a/@title').extract()
        print '*' * 80
        print response.url
        print url_list
        print title_list
        title_dir = {}
        # 品牌名称和url封装成字典
        for url, title in zip(url_list, title_list):
            title_dir[title] = url
        for title, url in title_dir.items():
            item = response.meta['meta']
            item['brand'] = title
            if url.startswith('/list.html'):
                url = 'https://list.jd.com' + url
            else:
                url = 'https://search.jd.com/' + url
            print '**************', url
            item['brand_url'] = url
            yield scrapy.Request(item['brand_url'], meta={'meta': item}, callback=self.parse_page)

    # 爬取每个品牌的所有网页，用webdriver模拟浏览器获取网页内容
    def parse_page(self, response):
        print '######################################################'
        print '######################################################'
        item = response.meta['meta']
        item['brand_url'] = response.url
        # print item['brand_url']
        driver = webdriver.PhantomJS()
        driver.get(response.url)
        html = driver.page_source
        selector = etree.HTML(html)
        gl_item = selector.xpath('//li[contains(@class,"gl-item")]/div')
        print len(gl_item)
        # 对每个网页内的产品爬取需求信息
        for site in gl_item:
            goods_url = site.xpath('div[contains(@class,"p-img")]/a/@href')[0]
            img_url = site.xpath(
                'div[contains(@class,"p-img")]/a/img/@src|div[contains(@class,"p-img")]/a/img/@data-lazy-img')
            # img_item=site.xpath('div[contains(@class,"p-img")]/a/img')
            # print etree.tostring(img_item[0],pretty_print=True)
            price = site.xpath('div[contains(@class,"p-price")]/strong[1]/i/text()')[0]
            name = site.xpath('div[contains(@class,"p-name")]/a/em/text()')
            parameter = site.xpath('div[contains(@class,"p-name p-name")]/span//b')
            comment = site.xpath('div[contains(@class,"p-commit")]//a/text()')[0]
            store = site.xpath('div[contains(@class,"p-shop")]//text()')
            parameter = '-'.join(parameter).replace('\n', ' ').strip(' ')
            name = ''.join(name).replace('\n', ' ').strip(' ')
            store = ''.join(store).replace('\n', ' ').strip(' ')
            if '万' in comment:
                print 'haha'
                comment = re.sub('[.]', '', comment)
                comment = re.sub('万', '0000', comment)
                comment = re.match('\d+', comment).group()
            else:
                comment = re.match('\d+', comment).group()
            item['goods_url'] = 'https:' + goods_url
            item['img_url'] = 'https:' + ''.join(img_url)
            # item['img_url']=img_item
            item['price'] = float(price)
            item['name'] = name
            item['parameter'] = parameter
            item['comment'] = int(comment)
            item['store'] = store
            yield item
        # 判断是否到最后一页
        if ('class="nf-content"' not in response.body) and ('class="p-wrap"'in response.body):
            # 修改URL,page+2
            print '**************************************************************************************'
            def fun(m):
                # print 'haha'
                return 'page=' + str(int(m.group(1)) + 2)

            url = response.url
            if 'page' in url:
                new_url = re.sub('page=(\d+)', fun, url)
            else:
                new_url = url + '&page=3'
            # print new_url
            yield scrapy.Request(new_url, meta={'meta': item}, callback=self.parse_page)
