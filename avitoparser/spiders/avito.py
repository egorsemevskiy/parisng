# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/sankt-peterburg/kvartiry?cd=1&p=1']

    def parse(self, response: HtmlResponse):
        page_num = [t for t in range(1, 101)]
        start_urls = ['https://www.avito.ru/sankt-peterburg/kvartiry?cd=1&p=' + str(page_nums) for page_nums in page_num]
        for start_url in start_urls:
            yield response.follow(start_url, callback=self.page_parse)

    def page_parse(self, response: HtmlResponse):
        posts = response.css('div.snippet-title-row h3.snippet-title a.snippet-link::attr(href)').extract()
        for post in posts:
            yield response.follow(post, callback=self.post_parse)

    def post_parse(self, response: HtmlResponse):
        title = response.css('h1.title-info-title span.title-info-title-text::text').extract_first()
        price = response.css('span.price-value-string span.js-item-price::text').extract_first()
        tags_caption = response.css('ul.item-params-list li.item-params-list-item span.item-params-label::text').extract()
        tags_eq = response.css('ul.item-params-list li.item-params-list-item::text').extract()
        while " " in tags_eq:
            tags_eq.remove(" ")
        tags = dict(zip(tags_caption, tags_eq))

        print(1)
        yield {
            'title': title,
            'price': price,
            'tags' : tags,
        }
        pass
