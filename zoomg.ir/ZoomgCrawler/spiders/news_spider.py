import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news_spider'
    start_urls = ['https://www.zoomg.ir/page/1/']

    def parse(self, response, **kwargs):
        news_selector = '.centerLayout .boxWrapper .imgContainer'
        title_selector = '.Contents h3 a::text'
        url_selector = '.Contents h3 a::attr(href)'
        author_selector = '.Contents .inline-block li a::text'
        date_selector = '.Contents .inline-block li::text'
        summery_selector = '.Contents p::text'
        category_selector = '.imgContainer .topicCategories a label::text'
        for news in response.css(news_selector):
            yield {
                'title': news.css(title_selector).get(),
                'author': news.css(author_selector).get(),
                'date': news.css(date_selector).get(),
                'summery': news.css(summery_selector).get(),
                'categories': news.css(category_selector).getall(),
                'url': news.css(url_selector).get()
            }
        current_page = int(response.url.split('/')[-2])
        next_page = current_page + 1

        # last_page = '.centerLayout .pagination-box .pagination-box .row .costumizPaginton .pagination li a::attr(href)'
        # last_page = int(response.css(last_page).getall()[-2].split('/')[-2])

        if next_page > 10:
            return
        else:
            yield scrapy.Request(f'https://www.zoomg.ir/page/{next_page}/')
