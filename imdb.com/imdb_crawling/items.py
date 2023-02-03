# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlItem(scrapy.Item):

    name = scrapy.Field()
    year = scrapy.Field()
    certificate = scrapy.Field()
    genre = scrapy.Field()
    runtime = scrapy.Field()
    rate = scrapy.Field()
    director = scrapy.Field()
    gross = scrapy.Field()



