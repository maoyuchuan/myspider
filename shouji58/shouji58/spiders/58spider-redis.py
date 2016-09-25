# -*- coding:utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from shouji58.items import Shouji58Item


class Myspider(RedisSpider):
    name = 'myspider_58'
    redis_key = 'myspider:xinghao_urls'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(Myspider, self).__init__(*args, **kwargs)
     

    def parse(self, response):
        
        pinpai = response.xpath('//dd[contains(@zwnameid, "36")]/a[contains(@class, "select")]/text()').extract()[0].strip()
        xinghao = response.xpath('//dd[contains(@zwnameid, "5463")]/a[contains(@class, "select")]/text()').extract()[0].strip()
        xinghao = pinpai + '-' + xinghao
        citys = response.xpath('//span[contains(@class, "fl")]/span[1]/text()').extract()
        titles = response.xpath('//td[contains(@class, "t")]/a[contains(@class, "t")]/text()').extract()
        usernames = response.xpath('//div[contains(@class, "qq_attest")]/p[2]/text()').extract()
        for x in range(len(areas)):
            city = citys[x].strip()
            title = titles[x].strip()
            username = usernames[x].strip()
            item = Shouji58Item()
            item['xinghao'] = xinghao
            item['title'] = title
            item['username'] = username
            item['city'] = city
            yield item





