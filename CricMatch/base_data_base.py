import mysql.connector as sql
import pandas as pd

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'testsql2025'
}

class BaseDatabase:
    def __init__(self, db_name):
        self.database_name = db_name
        self.connection = sql.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()
        print(f"My SQL Connection Established with data base: {self.database_name}")
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name};")

    def create_table(self, table_name, table_columns):
        try:
            print(f"create Table `{table_name}` with {table_columns}")
            self.cursor.execute(f"USE {self.database_name}")
            self.cursor.execute(table_columns)
            self.connection.commit()
            print(f"Table `{table_name}` created successfully")
            return True
        except sql.Error as err:
            print(f"Error creating table {table_name}: {err}")
            return False

    def _check_data_in_table(self, table_name):
        self.cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
        return self.cursor.fetchone() is None

    def save_to_db(self, df, table_name):
        if (self._check_data_in_table(table_name) == 1):
            cols = ",".join(df.columns)
            placeholders = ",".join(["%s"] * len(df.columns))
            sql_stmt = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

            print  (f" table columns ------ {cols}")
            # Convert DataFrame to list of tuples
            data = [tuple(x) for x in df.to_numpy()]
            # Insert all rows in batch
            self.cursor.executemany(sql_stmt, data)
            self.connection.commit()
            print(f"Uploaded data to {table_name}")

    def run_query(self, query):
        if query == "":
            return pd.DataFrame({})
        self.cursor.execute(f"USE {self.database_name}")
        df = pd.read_sql(query, self.connection)
        return df

    def close_db(self):
        print("...... base_data_base::close_db().........")
        self.cursor.close()
        self.connection.close()