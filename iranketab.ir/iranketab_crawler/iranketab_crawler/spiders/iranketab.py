import scrapy


class IranketabSpider(scrapy.Spider):
    name = 'iranketab'
    allowed_domains = ['iranketab.ir']
    start_urls = ['http://iranketab.ir/']

    def parse(self, response):
        pass
