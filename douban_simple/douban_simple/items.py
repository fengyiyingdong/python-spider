# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DoubanSimpleItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class Movie(Item):
    subject = Field()
    name = Field()
    year = Field()
    director = Field()
    scenarist = Field()
    actor = Field()
    mtype = Field()
    country = Field()
    releaseDate = Field()
    language = Field()
    runtime = Field()
    rating = Field()
    name2 = Field()
    IMDb = Field()
    summary = Field()
    tags = Field()
    sposterUrl = Field()
    sposterPath = Field()

class Review(Item):
    id = Field()
    subject = Field()
    title = Field()
    rating = Field()
    createAt = Field()
    content = Field()
    authorName = Field()
    authorId = Field() #people id
    usefulCount = Field() #有用
    uselessCount = Field() #无用
    donateNum = Field() #打赏数量
    recNum = Field() #转发数量
    commentsCount = Field() #评论数
    images = Field()
    

class People(Item):
    id = Field()
    name = Field()
    signature = Field()
    address = Field()
    registerTime = Field()
    intro = Field()
    groups = Field()
    doulists = Field()
    friendNum = Field()
    revNum = Field() #被关注的人数
    avatarUrl = Field()
    avatarPath = Field()


