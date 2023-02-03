import scrapy

class ArticalSpider(scrapy.Spider) :
    
    
    name='articalSpider'

    def start_requests(self): 
        urls= ['https://www.parsehub.com/blog/']
        return [scrapy.Request(url=url, callback=self.parse) for url in urls]

    def parse(self, response):

            if response.url == 'https://www.parsehub.com/blog/' :
                res = response.css('a[class="post-card-image-link"]::attr(href)').extract()
                for lin in res :
                    nn= 'https://www.parsehub.com'+ lin
                    yield scrapy.Request( nn  ) 
             
            else :
                full = response.css('.post-full-content').get() 
                yield { 'name' : full }

                