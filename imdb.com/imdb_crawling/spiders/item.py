import scrapy
from crawl.items import CrawlItem

class ItemSpider(scrapy.Spider):
    name = "item"
    start_urls = ['https://www.imdb.com/search/title/?genres=crime&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=f11158cc-b50b-4c4d-b0a2-40b32863395b&pf_rd_r=2YMSHDAP33XA9JQW5VRD&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_6']

    def parse(self, response):
        ci = CrawlItem()
        print('*' * 100)
        for i in response.css("div.lister-item"):
            ci['name'] = i.css(".lister-item-header a ::text").getall()
            ci['year'] = i.css(".lister-item-year ::text").getall()
            ci['certificate'] = i.css("span.certificate ::text").getall()
            ci['rate'] = i.css("strong ::text").getall()
            ci['runtime'] = i.css("span.runtime ::text").getall()
            ci['gross'] = i.css("span[name='nv'] ::text").extract()[-1]
            ci['director'] = i.css("p[class=''] a ::text").getall()[0]
            ci['genre']= i.css("span.genre ::text").extract()[0].strip()
            yield ci

        next_page = response.css('a.lister-page-next ::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://www.imdb.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)

