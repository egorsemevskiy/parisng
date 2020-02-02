from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gbparse import settings
from gbparse.spiders.cian import CianSpider
from gbparse.spiders.geekbrains import GeekbrainsSpider
from gbparse.spiders.avito import AvitoSpider
from gbparse.spiders.hh import HhSpider
from gbparse.spiders.instagram import InstagramSpider

if __name__ == '__main__':
    scr_settings = Settings()
    scr_settings.setmodule(settings)
    scr_settings.setmodule(settings)
    process = CrawlerProcess(settings=scr_settings)
    # process.crawl(GeekbrainsSpider)
    # process.crawl(AvitoSpider)
    # process.crawl(HhSpider)
    # process.crawl(InstagramSpider)
    process.crawl(CianSpider)
    process.start()


