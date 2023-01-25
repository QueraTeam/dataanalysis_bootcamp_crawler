import scrapy
from book_crawling.items import ProductInfo
import requests
from bs4 import BeautifulSoup
from book_crawling.Codes.database_handling import DatabaseHandling
import time
from tqdm import tqdm
import pandas as pd
from datetime import datetime


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

    all_page = [i for i in range(1, last_page + 1)]

    database_handler = DatabaseHandling()
    sql_query = """SELECT 
    page_number,
    AVG( updated_at ) AS avg_time 
    FROM
    "product_info" 
    GROUP BY
    page_number 
    ORDER BY
	avg_time ASC
	"""

    df = database_handler.get_data(sql_query)
    df = df.astype({"page_number": "int"}).copy()
    database_page = df["page_number"].tolist()

    new_page = list(filter(lambda x: x not in database_page, all_page))

    exists_page_with_priority = list(filter(lambda x: x not in new_page, database_page))

    page_priority = new_page + exists_page_with_priority

    for item in page_priority:
        res_list.append(
            f"https://shahreketabonline.com/Products?ValueID=&AttributeDescriptionID=&PackageID=&CategoryID=&ProductTypeID=&TagID=&Page={item}&ShowCase=False&Name=&Available=true&SortColumn=Price&DirectionTe&ValueID=&AttributeDescriptionID=&PackageID=&CategoryID=&ProductTypeID=&TagID=&Page=1&ShowCase=False&Name=&Available=&SortColumn=Price&DirectionText=DESC")

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
        info = dict()
        info["name"] = list()
        info["url"] = list()
        info["image_link"] = list()
        info["page_number"] = list()
        info["updated_at"] = list()
        all_res = response.css("div.ProductWrapper")

        for each_res in all_res:
            name = each_res.css("div.text > a::text").extract()[0].strip()
            url = self.base_url + each_res.css("div.text > a::attr(href)").extract()[0].strip()
            image_link = each_res.css("div.book-wrap > img::attr(data-src)").extract()

            info['name'].append(name)
            info['url'].append(url)

            if len(image_link) == 1:
                image_link = image_link[0].strip()
                info["image_link"].append(self.base_url + image_link)
            else:
                image_link = ""
                info["image_link"].append(image_link)

            info['page_number'].append(int(response.url.split("Page=")[1].split("&")[0]))

        product_info["name"] = info["name"]
        product_info["url"] = info["url"]
        product_info["image_link"] = info["image_link"]
        product_info["page_number"] = info["page_number"]
        self.count += 1
        print("{}/{}".format(self.count, len(self.start_urls)))

        return product_info

        """if next_page is not None:

            next_page_url = self.pure_url.format(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse_product, headers=self.base_headers)"""
