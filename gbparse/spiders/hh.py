# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse
from gbparse.items import HhItem
from scrapy.pipelines.images import ImagesPipeline

class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = ['https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text=Junior+python&page=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').extract_first()
        yield response.follow(next_page, callback=self.parse)
        posts = response.xpath(
            '//div[@class="resume-search-item__name"]/span[@class="g-user-content"]/a[@data-qa="vacancy-serp__vacancy-title"]/@href'
        ).extract()
        for post in posts:
            yield response.follow(post, callback=self.post_parse)

    def post_parse(self, response: HtmlResponse):
        item = ItemLoader(HhItem(), response)
        item.add_value('url', response.url)
        item.add_xpath('title', '//h1[@class="header"]//text()')
        item.add_xpath('price', '//p[@class="vacancy-salary"]//text()')
        item.add_xpath('tags', '//div[@class="vacancy-section"]//span[@data-qa="bloko-tag__text"]//text()')
        item.add_xpath('organization', '//a[@class="vacancy-company-name"]/span[@itemprop="name"]//text()')
        item.add_xpath('company_link', '//a[@class="vacancy-company-name"]/@href')
        item.add_xpath('logo', '//a[@class="vacancy-company-logo"]/img/@src')
        yield item.load_item()


class PhotoDownloadPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        pass







