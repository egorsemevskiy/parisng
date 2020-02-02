# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def cleaner_photo(values):
    if values[:2] == '//':
        return f'https:{values}'
    return values


def cleaner_params(item: str):
    result = item.split('">')[-1].split(':')
    key = result[0]
    value = result[-1].split('</span>')[-1].split('</')[0][:-1]
    try:
        value = int(value)
    except ValueError:
        pass
    return {key: value}


def cleaner_tags(items):
    result = {}
    for item in items:
        result.update(item)
    return result


def dict_params(items):
    result = {}
    for item in items:
        result.update(item)
    return result


def clean_price(value):
    return ' '.join(map(str, value))

class GbparseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AvitoItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    title = scrapy.Field(output_processor=TakeFirst())
    params = scrapy.Field(input_processor=MapCompose(cleaner_params), output_processor=dict_params)


class HhItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    # TODO преобразовать в список в строку price
    price = scrapy.Field()
    tags = scrapy.Field()
    organization = scrapy.Field()
    logo = scrapy.Field(output_processor=TakeFirst())
    company_link = scrapy.Field(output_process=TakeFirst())


class FollowersItem(scrapy.Item):
    _id = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    follower_id = scrapy.Field()
    follower_name = scrapy.Field()
    data = scrapy.Field()
