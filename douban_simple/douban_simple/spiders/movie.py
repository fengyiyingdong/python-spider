# -*- coding: utf-8 -*-

import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from douban_simple.items import Movie, Review, People


PeopleIdPattern = re.compile(r'^http[s]*://www\.douban\.com/people/(.+)/.*$')
NumPattern = re.compile(r'([0-9]+)')

def getNum(str):
    if not str:
        return None
    r = NumPattern.search(str)
    if r:
        return r.group(1)
    return None

def getPeopleId(str):
    if not str:
        return None
    r = PeopleIdPattern.match(str)
    if r:
        return r.group(1)
    return None;


class DoubanMovieSpider(CrawlSpider):
    name="movie"#爬虫名字
    allowed_domains=["douban.com"]#允许的域名
    start_urls=[#开始爬取的网站
        "https://movie.douban.com/"
    ]
    rules = (
        Rule(LinkExtractor(allow_domains=('movie.douban.com'), 
                allow=r'/subject/[0-9]+/\?from'), 
            callback="parse_movie", follow=True),
        Rule(LinkExtractor(allow_domains=('movie.douban.com'), 
                allow=r'/subject/[0-9]+/$',), 
            callback="parse_movie", follow=True),
        Rule(LinkExtractor(allow_domains=('movie.douban.com'), 
                allow=r'/review/[0-9]+/$',), 
            callback="parse_review", follow=True),
        Rule(LinkExtractor(allow=r'^https://www\.douban\.com/people/[a-z0-9]+/$',
                deny=r'login'),
            callback="parse_people", follow=True),
    )
    
    def parse_movie(self, response):
        sel = Selector(response)
        m = Movie()
        m['subject'] = getNum(response.url)
        try:
            m['name'] = sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()[0].strip()
        except Exception:
            return 
        m['year'] = getNum("".join(sel.xpath('//*[@id="content"]/h1/span[2]/text()').extract()).strip())
        m['director'] = "/".join(sel.xpath('//*[@id="info"]/span/span[contains(./text(), "导演")]/following-sibling::span/a/text()').extract())
        m['scenarist'] = "/".join(sel.xpath('//*[@id="info"]/span/span[contains(./text(), "编剧")]/following-sibling::span/a/text()').extract())
        m['actor'] = "/".join(sel.xpath('//*[@id="info"]/span/span[contains(./text(), "主演")]/following-sibling::span/a/text()').extract())
        m['mtype'] = "/".join(sel.xpath('//span[@property="v:genre"]/text()').extract())
        m['country'] = "/".join(sel.xpath('//*[@id="info"]/span[contains(./text(), "国家")]/following-sibling::text()[1]').extract()).strip()
        m['language'] = "/".join(response.xpath('//*[@id="info"]/span[contains(./text(), "语言")]/following-sibling::text()[1]').extract()).strip()
        m['releaseDate'] = '/'.join(sel.xpath('//span[@property="v:initialReleaseDate"]/text()').extract())
        m['runtime'] = ''.join(sel.xpath('//span[@property="v:runtime"]/text()').extract())
        m['name2'] = "/".join(sel.xpath('//*[@id="info"]/span[contains(./text(), "又名")]/following-sibling::text()[1]').extract()).strip()
        m['IMDb'] = ''.join(sel.xpath('//*[@id="info"]/a[contains(./@href, "imdb")]/text()').extract())
        m['summary'] = ''.join(sel.xpath('//*[@id="link-report"]/span/text()').extract()).strip()
        m['rating'] = ''.join(sel.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract())
        m['tags'] = "/".join(sel.xpath('//div[@class="tags-body"]/a/text()').extract())
        m['sposterUrl'] = "".join(sel.xpath('//*[@id="mainpic"]/a/img/@src').extract()).strip()
        if m['name']:
            yield m

    def parse_review(self, response):
        review = Review()
        review['id'] = getNum(response.url)
        review['subject'] = getNum(response.xpath('//a[contains(@href, "/subject/")]/@href').extract()[0])
        review['title'] = "".join(response.xpath('//span[@property="v:summary"]/text()').extract())
        review['content'] = "".join(response.xpath('//div[@property="v:description"]').extract())
        review['images'] = response.xpath('//div[@property="v:description"]//img/@src').extract()
        review['createAt'] = "".join(response.xpath('//span[@property="v:dtreviewed"]/text()').extract())
        review['rating'] = "".join(response.xpath('//span[@property="v:rating"]/text()').extract())
        review['authorName'] = "".join(response.xpath('//span[@property="v:reviewer"]/text()').extract())
        review['authorId'] = getPeopleId(response.xpath('//header//a[1]/@href').extract()[0])
        review['usefulCount'] = getNum("".join(response.xpath('//button[contains(@class, "useful_count")]/text()').extract()))
        review['uselessCount'] = getNum("".join(response.xpath('//button[contains(@class, "useless_count")]/text()').extract()))
        review['donateNum'] = "".join(response.xpath('//span[@class="js-donate-count"]/text()').extract())
        review['recNum'] = "".join(response.xpath('//span[@class="rec-num"]/text()').extract())
        review['commentsCount'] = ""
        if review['id']:
            yield review

    def parse_people(self, response):
        p = People()
        p["id"] = getPeopleId(response.url)
        p["name"] = "".join(response.xpath('//div[@class="info"]/h1/text()[1]').extract()).strip()
        p["signature"] = "".join(response.xpath('//div[@id="display"]/text()').extract())
        p["address"] = "".join(response.xpath('//div[@class="user-info"]/a[1]/text()').extract())
        p["registerTime"] = "".join(response.xpath('//div[@class="user-info"]/div/text()[2]').extract())
        p["intro"] = "".join(response.xpath('//textarea[@name="intro"]/text()').extract())
        p["groups"] = "|".join(response.xpath('//div[@id="group"]//a/text()').extract())
        p["doulists"] = "|".join(response.xpath('//div[@id="doulist"]//a/text()').extract())
        p["revNum"] = getNum("".join(response.xpath('//p[@class="rev-link"]/a/text()').extract()))
        p["friendNum"] = getNum("".join(response.xpath('//div[@id="friend"]/h2//a[1]/text()').extract()))
        p["avatarUrl"] = "".join(response.xpath('//img[@class="userface"]/@src').extract())
        if p["name"]:
            yield p
