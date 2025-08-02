import numpy as np
import pandas as pd
from faker import Faker
from base_data_base import BaseDatabase
import os

fake = Faker(locale='en_IN')

class BaseData(BaseDatabase):
    def __init__(self, table_name, table_columns, num_data=200):
        super().__init__()
        self.num_data = num_data
        self.data = []
        self.file_path = ""
        self.table_name = table_name
        self.table_columns = table_columns
        self.create_table(table_name, table_columns)

    def generate_id(self):
        return [f"{i+1:03d}" for i in range(self.num_data)]

    def save_to_file(self, file_name, folder='data'):
        self.file_path = os.path.join(folder, f"{file_name}.csv")
        os.makedirs(folder, exist_ok=True)

        # load data into DataFrame object
        df = pd.DataFrame(self.data)
        # print(df)

        # write values to (csv) file
        df.to_csv(self.file_path, index=False)
        return self.file_path

    def store_data_in_db(self):
        self.save_to_db(self.file_path, self.table_name)
