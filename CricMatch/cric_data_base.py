import pandas as pd
from base_data_base import BaseDatabase

class CricketDatabase(BaseDatabase):
    def __init__(self):
        super().__init__("cricket_db")

    def create_table(self, table_name, table_columns):
        return super().create_table(table_name, table_columns)

    def save_to_db(self, df, table_name, table_columns):
        if self.create_table(table_name, table_columns) == True:
            return super().save_to_db(df, table_name)