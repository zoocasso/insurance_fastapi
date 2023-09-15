import config

import pymysql

import pandas as pd

class mysql_session:
    def __init__(self):
        self.connection = pymysql.connect(host=config.DATABASE_CONFIG['host'],
                                    user=config.DATABASE_CONFIG['user'],
                                    password=config.DATABASE_CONFIG['password'],
                                    database=config.DATABASE_CONFIG['dbname'],
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def select_all_from_table(self,table_name):
        self.cursor.execute(f"select * from {table_name};")
        rows = self.cursor.fetchall()
        return rows
        
    def get_header_list(self,table_name):
        self.cursor.execute(f"select * from {table_name} limit 1;")
        rows = self.cursor.fetchall()
        finplot_data_columns = pd.DataFrame(rows).columns
        header_list = list()
        for column_name in finplot_data_columns:
            temp_dict = dict()
            temp_dict['title'] = column_name
            temp_dict['field'] = column_name
            header_list.append(temp_dict)
        return header_list

    def db_close(self):
        self.connection.close()