import scrapy
from book_crawling.items import ProductInfo
import time


class ShahreketabonilneSpider(scrapy.Spider):
    name = 'shahreketabonilne'
    allowed_domains = ['shahreketabonline.com']
    start_urls = ["https://shahreketabonline.com/Products?ValueID=&AttributeDescriptionID=&PackageID=&CategoryID=&ProductTypeID=&TagID=&Page=1&ShowCase=False&Name=&Available=&SortColumn=Price&DirectionTe&ValueID=&AttributeDescriptionID=&PackageID=&CategoryID=&ProductTypeID=&TagID=&Page=1&ShowCase=False&Name=&Available=&SortColumn=Price&DirectionText=DESC"]

    pure_url = "https://shahreketabonline.com/Products?ValueID=&AttributeDescriptionID=&PackageID=&CategoryID=&ProductTypeID=&TagID=&Page={}&ShowCase=False&Name=&Available=&SortColumn=Price&DirectionTe&ValueID=&AttributeDescriptionID=&PackageID=&CategoryID=&ProductTypeID=&TagID=&Page=1&ShowCase=False&Name=&Available=&SortColumn=Price&DirectionText=DESC"

    product_infos = []

    base_headers = {
        "user-agent": """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36""",
        "x-requested-with": "XMLHttpRequest"
        }

    base_url = "https://shahreketabonline.com"

    def parse(self, response, **kwargs):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_product, headers=self.base_headers)

    def parse_product(self, response):
        print(response.url)
        product_info = ProductInfo()
        all_res = response.css("div.ProductWrapper")
        next_page = response.css("ul.pagination > li.active + li > a::text").extract_first()

        for each_res in all_res:
            name = each_res.css("div.text > a::text").extract()[0].strip()
            url = self.base_url + each_res.css("div.text > a::attr(href)").extract()[0].strip()
            product_info['name'] = name
            product_info['url'] = url
            self.product_infos.append(product_info)
        print(int(next_page) - 1)

        if next_page is not None:

            next_page_url = self.pure_url.format(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse_product, headers=self.base_headers)



