# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
from datetime import datetime
from book_crawling.Codes.database_handling import DatabaseHandling

import sqlite3
from sqlite3 import Error
import os


class BookCrawlingPipelineInfo:
    csv_path = '..\\Databases\\'

    def open_spider(self, spider):
        database_handler = DatabaseHandling()
    def process_item(self, item, spider):
        database_handler = DatabaseHandling()
        con, cur = database_handler.get_connection()
        df = pd.DataFrame({"name": item["name"],
                           "url": item["url"],
                           "image_link": item["image_link"],
                           "page_number": item["page_number"]})
        df["updated_at"] = str(datetime.now())
        df.to_sql("product_info", con, if_exists="append", index=False)
        return item


