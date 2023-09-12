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

    def select_data_table(self,ACC_PERIOD,ACC_PERIOD_TYPE,M_LIAB_ITEM,M_ACC_EVENT):
        self.cursor.execute(f"select * from data where ACC_PERIOD = '{ACC_PERIOD}' AND ACC_PERIOD_TYPE = '{ACC_PERIOD_TYPE}' AND M_LIAB_ITEM = {M_LIAB_ITEM} AND M_ACC_EVENT = {M_ACC_EVENT};")
        rows = self.cursor.fetchall()
        return rows

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
            temp_dict['width'] = 200
            header_list.append(temp_dict)
        return header_list

    def db_close(self):
        self.connection.close()
    
    def cell_parsing(cell_coordinate):
        # openpyxl 특정값 (ACC_PERIOD, ACC_PERIOD_TYPE, UNIT, 원수출재_GOC, 원수출재_PORTF)
        # 해당 좌표값 참조 x, y의 코드 >> 해당 코드만 data시트에서 조회
        print(cell_coordinate)
        print(cell_coordinate.row)
        print(cell_coordinate.column)
        return cell_coordinate