import numpy as np
import pandas as pd
from faker import Faker
import os

fake = Faker(locale='en_IN')

class BaseData:
    def __init__(self, num_data=10):
        self.num_data = num_data
        self.data = []
        self.file_path = None

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