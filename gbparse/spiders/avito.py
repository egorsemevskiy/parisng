# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse
from gbparse.items import AvitoItem


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = [f'https://www.avito.ru/sankt-peterburg/kvartiry?p={idx}' for idx in range(1, 101)]

    def parse(self, response: HtmlResponse):
        for url in response.xpath(
                '//div[contains(@data-marker, "item")]/div[@class="item__line"]//h3/a[@itemprop="url"]'):
            yield response.follow(url, callback=self.avd_parse)

    def avd_parse(self, response: HtmlResponse):
        item = ItemLoader(AvitoItem(), response)
        item.add_value('url', response.url)
        item.add_xpath('title', '//h1[@class="title-info-title"]/span/text()')
        item.add_xpath('photos', '//div[contains(@class, "js-gallery-img-frame")]/@data-url')
        yield item.load_item()

