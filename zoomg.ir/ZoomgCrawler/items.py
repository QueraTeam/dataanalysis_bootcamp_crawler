import scrapy


class News(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    summery = scrapy.Field()
