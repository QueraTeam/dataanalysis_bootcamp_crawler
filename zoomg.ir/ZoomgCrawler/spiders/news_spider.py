import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news_spider'
    allowed_domains = ['https://www.zoomg.ir/']
    start_urls = ['https://www.zoomg.ir/page/1/']

    def parse(self, response, **kwargs):
        news_selector = 'div.centerLayout div.boxWrapper div.imgContainer'
        title_selector = 'div.Contents h3 a::text'
        author_selector = 'div.Contents ul.inline-block li a::text'
        date_selector = 'div.Contents ul.inline-block li::text'
        summery_selector = 'div.Contents p::text'
        for news in response.css(news_selector):
            yield {
                'title': news.css(title_selector).get(),
                'author': news.css(author_selector).get(),
                'date': news.css(date_selector).get(),
                'summery': news.css(summery_selector).get(),
            }
