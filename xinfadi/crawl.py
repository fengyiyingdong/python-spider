#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import logging; logging.basicConfig(level=logging.INFO)
from aiohttp import ClientSession
from lxml import etree
from models import Product
import asyncio, re
import orm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'www.xinfadi.com.cn',
    'Host': 'www.xinfadi.com.cn',
}

async def fetch(url):
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.text()

async def request():
    url = "http://www.xinfadi.com.cn/marketanalysis/{}/list/{}.shtml"
    for i in range(1, 2):
        response = await fetch(url.format(i, 1))
        pageNum = getLastPageNum(response)
        if not pageNum:
            logging.error("pageNum %s invalid" % pageNum)
            break
        logging.info("request from 1 to %s for %s" % (pageNum, i))
        for j in range(1, pageNum + 1):
            responses = await fetch(url.format(i, j))
            await parse(responses)

PageNumPattern = re.compile(r'.+/(\d+).shtml$')

def getLastPageNum(str):
    html = etree.HTML(str)
    href = "".join(html.xpath('//div[@class="manu"]/a[last()]/@href'))
    if not href:
        return None
    r = PageNumPattern.search(href)
    if r:
        return int(r.group(1))
    return None

async def parse(results):
    for result in results:
        html = etree.HTML(result)
        trs = html.xpath('//table[@class="hq_table"]/tr')[1:]
        for tr in trs:
            trhtml = etree.HTML(etree.tostring(tr).decode('utf-8'))
            tds = trhtml.xpath("//td/text()")
            name = tds[0].strip()
            low = float(tds[1]) * 100
            average = float(tds[2]) * 100
            high = float(tds[3]) * 100
            tp = tds[4].strip()
            unit = tds[5].strip()
            publish = tds[6].strip()
            p = Product(id=None, name=name, low=low, high=high, average=average, tp=tp, unit=unit, publish=publish)
            await p.save()
            logging.info("save %s" % p)

async def run(loop):
    await orm.create_pool(loop, user='douban', password='123456', db='douban')
    await request()

loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))
