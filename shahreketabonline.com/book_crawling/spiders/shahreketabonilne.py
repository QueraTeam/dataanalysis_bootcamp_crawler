import scrapy
from book_crawling.items import ProductInfo
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm


def get_start_urls() -> list:
    res_list = []
    url = "https://shahreketabonline.com/Products?ValueID=&AttributeDescriptionID=&PackageID=&CategoryID=&ProductTypeID=&TagID=&Page=1&ShowCase=False&Name=&Available=true&SortColumn=Price&DirectionTe&ValueID=&AttributeDescriptionID=&PackageID=&CategoryID=&ProductTypeID=&TagID=&Page=1&ShowCase=False&Name=&Available=&SortColumn=Price&DirectionText=DESC"
    base_headers = {
        "user-agent": """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36""",
        "x-requested-with": "XMLHttpRequest"
    }
    response = requests.get(url, headers=base_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    pages_tag = soup.find_all("li", attrs={"class": "page-item"})

    last_page_tag = pages_tag[-3]
    last_page = int(last_page_tag.getText().strip())
    for i in range(1, last_page + 1):
        res_list.append(f"https://shahreketabonline.com/Products?ValueID=&AttributeDescriptionID=&PackageID=&CategoryID=&ProductTypeID=&TagID=&Page={i}&ShowCase=False&Name=&Available=true&SortColumn=Price&DirectionTe&ValueID=&AttributeDescriptionID=&PackageID=&CategoryID=&ProductTypeID=&TagID=&Page=1&ShowCase=False&Name=&Available=&SortColumn=Price&DirectionText=DESC")

    return res_list


class ShahreketabonilneSpider(scrapy.Spider):
    name = 'shahreketabonilne'
    allowed_domains = ['shahreketabonline.com']

    """start_urls = ["https://shahreketabonline.com/Products?ValueID=&AttributeDescriptionID=&PackageID=&CategoryID=&ProductTypeID=&TagID=&Page=1&ShowCase=False&Name=&Available=true&SortColumn=Price&DirectionTe&ValueID=&AttributeDescriptionID=&PackageID=&CategoryID=&ProductTypeID=&TagID=&Page=1&ShowCase=False&Name=&Available=&SortColumn=Price&DirectionText=DESC",
                  "https://shahreketabonline.com/Products?ValueID=&AttributeDescriptionID=&PackageID=&CategoryID=&ProductTypeID=&TagID=&Page=10000&ShowCase=False&Name=&Available=&SortColumn=Price&DirectionTe&ValueID=&AttributeDescriptionID=&PackageID=&CategoryID=&ProductTypeID=&TagID=&Page=1&ShowCase=False&Name=&Available=&SortColumn=Price&DirectionText=DESC"]"""

    start_urls = get_start_urls()

    pure_url = "https://shahreketabonline.com/Products?ValueID=&AttributeDescriptionID=&PackageID=&CategoryID=&ProductTypeID=&TagID=&Page={}&ShowCase=False&Name=&Available=&SortColumn=Price&DirectionTe&ValueID=&AttributeDescriptionID=&PackageID=&CategoryID=&ProductTypeID=&TagID=&Page=1&ShowCase=False&Name=&Available=&SortColumn=Price&DirectionText=DESC"

    product_infos = []

    base_headers = {
        "user-agent": """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36""",
        "x-requested-with": "XMLHttpRequest"
        }

    base_url = "https://shahreketabonline.com"
    count = 0

    def parse(self, response, **kwargs):
        for url in self.start_urls:
            page_number = int(url.split("Page=")[1].split("&")[0])
            yield scrapy.Request(url,
                                 callback=self.parse_product,
                                 headers=self.base_headers,
                                 priority=len(self.start_urls) - page_number)

    def parse_product(self, response):
        print(response.url)
        product_info = ProductInfo()
        all_res = response.css("div.ProductWrapper")

        for each_res in all_res:
            name = each_res.css("div.text > a::text").extract()[0].strip()
            url = self.base_url + each_res.css("div.text > a::attr(href)").extract()[0].strip()
            image_link = each_res.css("div.book-wrap > img::attr(data-src)").extract()

            product_info['name'] = name
            product_info['url'] = url

            if len(image_link) == 1:
                image_link = image_link[0].strip()
                product_info["image_link"] = self.base_url + image_link
            else:
                image_link = ""
                product_info["image_link"] = image_link

            product_info['page_number'] = int(response.url.split("Page=")[1].split("&")[0])

            self.product_infos.append(product_info)
        self.count += 1
        print("{}/{}".format(self.count, len(self.start_urls)))

        """if next_page is not None:

            next_page_url = self.pure_url.format(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse_product, headers=self.base_headers)"""





