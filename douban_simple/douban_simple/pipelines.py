# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
from douban_simple.items import Movie, People


class DoubanMysqlPipeline(object):

    @classmethod
    def from_settings(cls, settings):
        adbparams = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            password = settings['MYSQL_PASSWORD'],
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True,
            )
        dbpool = adbapi.ConnectionPool('MySQLdb',**adbparams)
        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)

    def handle_error(self,failure):
        print(failure)

    def do_insert(self,cursor,item):
        insert_sql = """
                    insert into article(title,url,create_date,url_object_id,front_image_url,front_image_path,
                    praise,collect_nums,comment_nums,contents,tags)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['url_object_id'],item['front_image_url'], item['front_image_path'], item['praise'],item['collect_nums'], item['comment_nums'], item['contents'], item['tags']))


class DoubanImagePipeline(ImagesPipeline):

    def file_path(self, item):
        path =  super().file_path(item);
        if isinstance(item, People):
            path = path.replace("full", "peple")
        elif isinstance(item, Moive):
            path = path.replace("full", "mov/sposter")
        return path

    def get_media_requests(self, item, info):
        # for image_url in item['image_urls']:
        #     yield scrapy.Request(image_url)
        if item['sposterUrl']:
            yield scrapy.Request(item['sposterUrl'])
        elif item['avatarUrl']:
            yield scrapy.Request(item['avatarUrl'])

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        if isinstance(item, People):
            item['avatarPath'] = image_paths[0]
        elif isinstance(item, Moive):
            item['sposterPath'] = image_paths[0]
        return item