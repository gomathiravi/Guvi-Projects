import mysql.connector as sql
import pandas as pd

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'testsql2025'
}

class BaseDatabase:
    def __init__(self):
        self.database_name = "students_db"
        self.connection = sql.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()
        print(f"My SQL Connection Established with data base: {self.database_name}")
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name};")

    def create_table(self, table_name, table_columns):
        try:
            self.cursor.execute(f"USE {self.database_name}")
            self.cursor.execute(table_columns)
            self.connection.commit()
            print(f"Table `{table_name}` created successfully")
        except sql.Error as err:
            print(f"Error creating table {table_name}: {err}")

    def _check_data_in_table(self, table_name):
        self.cursor.execute("SELECT 1 FROM students LIMIT 1")
        return self.cursor.fetchone() is None

    def save_to_db(self, csv_path, table_name):
        if (self._check_data_in_table(table_name) == 1):
            df = pd.read_csv(csv_path)
            cols = ",".join(df.columns)
            placeholders = ",".join(["%s"] * len(df.columns))

            for _ , row in df.iterrows():
                sql_stmt = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
                print(row)
                self.cursor.execute(sql_stmt, tuple(row))

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