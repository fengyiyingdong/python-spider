# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from douban_simple.items import Movie

class DoubanSpider(Spider):
    name="douban"#爬虫名字
    allowed_domains=["douban.com"]#允许的域名
    start_urls=[#开始爬取的网站
        "https://movie.douban.com/chart"
    ]
    
    def parse(self, response):
        sel = Selector(response)
        for idx in range(1, 100):
            movieitem = Movie()
            movieitem['name'] = sel.xpath('//*[@id="content"]/div/div[1]/div/div/table[%d]/tr/td[2]/div/a/text()'%idx).extract()
            if not movieitem['name']:
                break;
            movieitem['name'] = movieitem['name'][0].strip();
            movieitem['compactSummary'] = sel.xpath('//*[@id="content"]/div/div[1]/div/div/table[%d]/tr/td[2]/div/p/text()'%idx).extract()[0].strip()
            movieitem['score'] = sel.xpath('//*[@id="content"]/div/div[1]/div/div/table[%d]/tr/td[2]/div/div/span[2]/text()'%idx).extract()[0]
            movieitem['sposterUrl'] = sel.xpath('//*[@id="content"]/div/div[1]/div/div/table[%d]/tr/td[1]/a/img/@src'%idx).extract()[0]
            yield movieitem
        # return movieitems