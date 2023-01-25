import sqlite3
from sqlite3 import Error
import os
import pandas as pd


class DatabaseHandling:
    def __init__(self):
        self.path = "..\\Databases\\"
        self.create_directory()
        self.connection = sqlite3.connect(self.path + 'shahreketabonline.db')
        self.cursor = self.connection.cursor()

    def create_directory(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def get_connection(self):
        return self.connection, self.cursor

    def get_all_data(self, table_name):
        sql_query = "SELECT * FROM {}".format(table_name)
        try:
            df = pd.read_sql_query(sql_query, self.connection)
        except Error as e:
            df = pd.DataFrame()
        return df

    def create_table_product_info(self):
        sql_query = """CREATE TABLE IF NOT EXISTS product_info (
                    'url' text PRIMARY KEY,
                    'name' text,
                    'image_link' text,
                    'page_number' INTEGER,
                    'updated_at' INTEGER
                    );"""
        self.cursor.execute(sql_query)
        self.connection.commit()

    def update_table_product_info(self, df):
        for index, row in df.iterrows():
            sql_query = """UPDATE product_info SET page_number = '{}',
             updated_at = '{}',
             'name' = '{}',
             image_link = '{}'
             WHERE url = '{}'""".format(row["page_number"], row["updated_at"], row["name"], row["image_link"], row["url"])
            self.cursor.execute(sql_query)
            self.connection.commit()

    def get_data(self, sql_query):
        df = pd.DataFrame()
        try:
            df = pd.read_sql_query(sql_query, self.connection)
        except Error as e:
            print(e)
        finally:
            return df

    def vacuum(self):
        self.cursor.execute("VACUUM")
        self.connection.commit()


