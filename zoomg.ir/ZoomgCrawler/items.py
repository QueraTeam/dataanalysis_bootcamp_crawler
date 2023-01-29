import scrapy


class News(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    summery = scrapy.Field()
    categories = scrapy.Field()
    url = scrapy.Field()
