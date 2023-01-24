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
        df = pd.read_sql_query(sql_query, self.connection)
        return df
