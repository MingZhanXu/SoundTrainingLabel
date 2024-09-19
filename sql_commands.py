import sqlite3
import atexit
import time
from datetime import datetime


class SqlCommands:
    def __init__(self, db_name="recording_file_sequence", table_name="RECORDING_FILE_SEQUENCE"):
        self.db_name = db_name
        self.table_name = table_name
        self.initialization_connect()

    # Timestamp string
    def timestamp(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + '{:03d}'.format(datetime.now().microsecond % 1000)

    # Set SQL commands
    def set_sql_commands(self):
        # SQL instruction
        self.check_table_sql = '''
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name='{table_name}';
            '''.format(table_name=self.table_name)
        self.create_table_sql = '''
            CREATE TABLE {table_name}
            (TIMESTAMP TEXT PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
            FILE_PATH TEXT NOT NULL);
            '''.format(table_name=self.table_name)
        # INSERT
        self.insert_data = '''
            INSERT INTO {table_name} (FILE_PATH, TIMESTAMP) VALUES (?, ?);
            '''.format(table_name=self.table_name)
        # SELECT
        self.select_table_sql = '''
            SELECT * FROM {table_name};
            '''.format(table_name=self.table_name)
        self.select_latest_record_sql = '''
            SELECT * FROM {table_name} ORDER BY TIMESTAMP DESC LIMIT 1;
            '''.format(table_name=self.table_name)
        self.delete_by_timestamp_sql = '''
            DELETE FROM {table_name} WHERE TIMESTAMP = ?;
            '''.format(table_name=self.table_name)
    
    # Connect to database
    def connect_to_database(self):
        try:
            self.conn = sqlite3.connect(f'{self.db_name}.db')
            print("Opened database successfully")
        except Exception as e:
            print("SQL Open Error: ", e)
            exit()

    # Create table if not exists
    def create_table_if_not_exists(self):
        try:
            cursor = self.conn.cursor()
            sql = self.check_table_sql
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
            if result is None:
                try:
                    sql = self.create_table_sql
                    cursor.execute(sql)
                    print("Table created successfully")
                except Exception as e:
                    print("SQL Table Error[1]: ", e)
                    exit()
            else:
                print("Table already exists")
        except Exception as e:
            print("SQL Table Error[2]: ", e)
            exit()

    # Register a function to close the database connection at exit
    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    # Initialize connection
    def initialization_connect(self):
        self.set_sql_commands()
        self.connect_to_database()
        atexit.register(self.close_connection)
        self.create_table_if_not_exists()

    # Insert file path
    def insert_file_path(self, file_path):
        ts = self.timestamp()
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.insert_data, (file_path, ts))
            self.conn.commit()
            print("Record inserted successfully")
        except Exception as e:
            print("SQL Insert Error: ", e)
            exit()

    # Select all records
    def select_all_records(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.select_table_sql)
            records = cursor.fetchall()
            records = [record for record in records]
            return records
        except Exception as e:
            print("SQL Select Error: ", e)
            exit()

    # Select latest record
    def select_latest_record(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.select_latest_record_sql)
            record = cursor.fetchone()
            return record
        except Exception as e:
            print("SQL Select Error: ", e)
            exit()

    # Delete by timestamp
    def delete_by_timestamp(self, timestamp):
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.delete_by_timestamp_sql, (timestamp,))
            self.conn.commit()
            print("Record deleted successfully")
        except Exception as e:
            print("SQL Delete Error: ", e)
            exit()

    # Delete last record
    def delete_last_record(self):
        timestamp = self.select_latest_record()[0]
        self.delete_by_timestamp(timestamp)

if __name__ == '__main__':
    # 初始設定
    sql = SqlCommands()
    # 模擬新增檔案路徑
    for i in range(10):
        input_file_path = f'test.mp4{i}'
        sql.insert_file_path(input_file_path)

    print()
    last_timestamp = sql.select_latest_record()
    print(sql.select_latest_record())
    # 模擬刪除最後一筆紀錄
    sql.delete_last_record()
