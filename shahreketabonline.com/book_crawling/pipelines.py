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
        database_handler.create_table_product_info()
    def process_item(self, item, spider):
        database_handler = DatabaseHandling()
        con, cur = database_handler.get_connection()
        df = pd.DataFrame({"url": item["url"],
                           "name": item["name"],
                           "image_link": item["image_link"],
                           "page_number": item["page_number"]})
        df["updated_at"] = str(datetime.now())

        # clean data

        # 1_check if df["name"] and df["url"] not null and drop duplicates
        df = df[df["name"] != ""]
        df = df[df["url"] != ""]
        df.drop_duplicates(subset=["url"], inplace=True)
        df = df.astype({"page_number": "str"}).copy()

        # 2_get data from database
        df_database = database_handler.get_all_data("product_info")

        # 3_create merged df
        merged_df = pd.merge(left=df,
                             right=df_database,
                             how="outer",
                             left_on=["url", "name", "image_link", "page_number", "updated_at"],
                             right_on=["url", "name", "image_link", "page_number", "updated_at"],
                             indicator=True)

        # 4_drop duplicates
        merged_df = merged_df[merged_df["_merge"] != "both"].copy()

        # new data
        new_df = merged_df[merged_df["_merge"] == "left_only"].copy()
        new_df = new_df[~(new_df["url"].isin(df_database["url"]))].copy()
        new_df.drop(columns=["_merge"], inplace=True)

        new_df["updated_at"] = str(datetime.now())
        new_df.to_sql("product_info", con, if_exists="append", index=False)

        # update data
        update_df = merged_df[merged_df["_merge"] == "left_only"].copy()
        update_df = update_df[update_df["url"].isin(df_database["url"])].copy()
        update_df.drop(columns=["_merge"], inplace=True)

        database_handler.update_table_product_info(update_df)

        return item



