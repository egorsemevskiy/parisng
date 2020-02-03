# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from PIL import Image
import scrapy


mongo_client = MongoClient()


class GbparsePipeline(object):

    def process_item(self, item, spider):
        database = mongo_client[spider.name]
        collection = database[type(item).__name__]
        collection.insert_one(item)
        return item


class HhparsePipiline(object):

    def process_item(self, item, spider):
        database = mongo_client[spider.name]
        collection = database['db_parse_29_01']
        collection.insert_one(item)
        return item


class PhotoDownloadPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item.get('photos'):
            for img in item.get('photos'):
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results]
        return item


class InstaPipeline(object):

    def process_item(self, item, spider):
        database = mongo_client[spider.name]
        collection = database[type(item).__name__]
        collection.insert_one(item)
        return item