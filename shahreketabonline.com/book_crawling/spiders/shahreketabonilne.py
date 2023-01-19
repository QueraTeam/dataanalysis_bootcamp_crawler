import scrapy


class ShahreketabonilneSpider(scrapy.Spider):
    name = 'shahreketabonilne'
    allowed_domains = ['shahreketabonline.com']
    start_urls = ['http://shahreketabonline.com/']

    def parse(self, response):
        pass
