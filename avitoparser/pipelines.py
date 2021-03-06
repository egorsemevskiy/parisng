# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


mongo_client = MongoClient()


class AvitoparserPipeline(object):
    def process_item(self, item, spider):
        database = mongo_client[spider.name]
        collection = database['db_parse_27_01']
        collection.insert_one(item)
        return item
