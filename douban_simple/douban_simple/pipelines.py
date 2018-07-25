# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import pymysql
import pymysql.cursors
import os
import shutil
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
from douban_simple.items import Movie, People, Review


class DoubanMysqlPipeline(object):

    @classmethod
    def from_settings(cls, settings):
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        func = None
        if isinstance(item, Movie):
            func = self.do_insert_movie
        elif isinstance(item, People):
            func = self.do_insert_people
        elif isinstance(item, Review):
            func = self.do_insert_review
        else:
            raise DropItem('Item type %s invalid' % type(item))
        query = self.dbpool.runInteraction(func, item)
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        print(failure)

    def do_insert_movie(self, cursor, item):
        insert_sql = """
            INSERT INTO movie (subject, name, year,director,
                 scenarist, actor, mtype, country,
                 releaseDate,language, runtime, rating,
                 name2, IMDb, summary, tags, sposterUrl,
                 sposterPath)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s);
                    """
        cursor.execute(insert_sql, (item['subject'], item['name'], item['year'],
                                    item['director'], item['scenarist'], item[
                                        'actor'], item['mtype'],
                                    item['country'], item[
                                        'releaseDate'], item['language'],
                                    item['runtime'], item['rating'], item[
                                        'name2'], item['IMDb'],
                                    item['summary'], item[
                                        'tags'], item['sposterUrl'],
                                    item['sposterPath']))

    def do_insert_people(self, cursor, item):
        insert_sql = """ 
            INSERT INTO people (id, name, signature, address,
                    registerTime, intro, groups, doulists,
                    friendNum, revNum, avatarUrl, avatarPath)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s)
        """
        cursor.execute(insert_sql, (item['id'], item['name'], item['signature'],
                                    item['address'], item['registerTime'], item[
                                        'intro'], item['groups'],
                                    item['doulists'], item[
                                        'friendNum'], item['revNum'],
                                    item['avatarUrl'], item['avatarPath']))

    def do_insert_review(self, cursor, item):
        insert_sql = """
            INSERT INTO review (id, subject, title, rating,
                createAt, content, authorName, authorId, usefulCount,
                uselessCount, donateNum, recNum, commentsCount)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s)
        """
        cursor.execute(insert_sql, (item['id'], item['subject'], item['title'],
                                    item['rating'], item['createAt'], item[
                                        'content'], item['authorName'],
                                    item['authorId'], item[
                                        'usefulCount'], item['uselessCount'],
                                    item['donateNum'], item['recNum'], item['commentsCount']))


def movefile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.move(srcfile, dstfile)


class DoubanImagePipeline(ImagesPipeline):

    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, download_func, settings)
        self.store_uri = store_uri

    def get_media_requests(self, item, info):
        if isinstance(item, Movie):
            yield scrapy.Request(item['sposterUrl'])
        elif isinstance(item, People):
            yield scrapy.Request(item['avatarUrl'])
        elif isinstance(item, Review):
            for image_url in item['images']:
                yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]

        if isinstance(item, People):
            item['avatarPath'] = image_paths[0]
        elif isinstance(item, Movie):
            item['sposterPath'] = image_paths[0]
        elif isinstance(item, Review):
            url_paths = [x for ok, x in results if ok]
            for url_path in url_paths:
                srcfile = self.store_uri + "/" + url_path['path']
                dstfile = self.store_uri + url_path['url'].split(":")[1][1:]
                movefile(srcfile, dstfile)
        return item
