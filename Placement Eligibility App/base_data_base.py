import mysql.connector as sql
import pandas as pd

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'testsql2025'
}

class BaseDatabase:
    def __init__(self):
        self.connection = sql.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()
        print("My SQL Connection Established")
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS pes_db;")
        # self.cursor.close()
        # self.connection.close()

        # check if database exists
        # self.cursor.execute("SHOW DATABASES")
        # databases = self.cursor.fetchall()
        # for db in databases:
        #     if 'pes_db' in db:
        #         print (f"Database {db} exists")
        #         break

    def create_table(self, table_name, table_columns):
        try:
            self.cursor.execute("USE pes_db")
            self.cursor.execute(table_columns)
            self.connection.commit()
            print(f"Table `{table_name}` created successfully")
        except sql.Error as err:
            print(f"Error creating table {table_name}: {err}")

    def save_to_db(self, csv_path, table_name):
        df = pd.read_csv(csv_path)
        cols = ",".join(df.columns)
        placeholders = ",".join(["%s"] * len(df.columns))

        for _, row in df.iterrows():
            sql_stmt = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
            print(row)
            self.cursor.execute(sql_stmt, tuple(row))

        self.connection.commit()
        print(f"Uploaded data to {table_name}")

