# -*- coding:utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from redis import Redis
from scrapy import log
from time import sleep


class Myspider(RedisSpider):
    name = '58spider_shouji'
    redis_key = 'myspider:58_urls'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(Myspider, self).__init__(*args, **kwargs)
        self.url = 'http://su.58.com'

    def parse(self, response):
       
        r = Redis()
        exist = response.xpath('//dd[contains(@zwnameid, "5463")]')
        if exist != []:
            select = response.xpath('//dd[contains(@zwnameid, "5463")]/a[contains(@class, "select")]/@name').extract()
            if select == []:
                XinghaoUrl = response.xpath('//dd[contains(@zwnameid, "5463")]/a[contains(@name, "b_link")]/@href').extract()
                for x in range(len(XinghaoUrl)):
                    r.lpush('myspider:58_urls', XinghaoUrl[x])
            else:
                r.lpush('myspider:xinghao_urls', response.url)
                PageUrl = response.xpath('//a[contains(@class, "next")]/@href').extract()
                self.log(PageUrl, level=log.DEBUG)
                if PageUrl != []:
                    r.lpush('myspider:58_urls', self.url + PageUrl[0])
                    sleep(1)
                    
       
                
        else:
            BrandUrl = response.xpath('//dd[contains(@zwnameid, "36")]/a[contains(@name, "b_link")]/@href').extract()
            initurl = response.xpath('//dd[contains(@zwnameid, "36")]/a[contains(@class, "select")]/@href').extract()[0]
            if initurl == '/shouji/':
                for i in range(len(BrandUrl)):
                    r.lpush('myspider:58_urls', BrandUrl[i])
        