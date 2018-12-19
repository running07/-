from scrapy import cmdline
cmdline.execute('scrapy runspider D:\python\TestScrapy\day05\JDRedisSpider\JDRedisSpider\spiders\jdredis.py '.split())


#jdspider:start_urls https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8
#lpush jdspider:start_urls https://www.jd.com/
# scrapy runspider jdredis.py