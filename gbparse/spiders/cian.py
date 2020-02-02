# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse


class CianSpider(scrapy.Spider):
    name = 'cian'
    allowed_domains = ['krasnodar.cian.ru']
    start_urls = ['https://krasnodar.cian.ru/snyat/']

    def parse(self, response: HtmlResponse):
        categories_page = response.xpath(
            '//div[@class="cg-container-fluid-xs"]//div[@class="c-popular-links"]//a')

        for url in categories_page:
            if url.attrib.get('href'):
                yield response.follow(url, callback=self.ads_rows_parse)

    def ads_rows_parse(self, response: HtmlResponse):
        pagination = response.xpath(
            '//div[@class="_93444fe79c--wrapper--2B3If"]//ul[@class="_93444fe79c--list--HEGFW"]/li/a')

        for page_url in pagination:
            if page_url.attrib.get('href'):
                yield response.follow(page_url, callback=self.ads_rows_parse)

        ads = response.xpath('//div[@class="_93444fe79c--wrapper--E9jWb"]//a[@class="c6e8ba5398--header--1fV2A"]')

        for ads_url in ads:
            if ads_url.attrib.get('href'):
                yield response.follow(ads_url, callback=self.ads_parse)

    def ads_parse(self, response: HtmlResponse):
        print(1)
