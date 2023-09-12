# -*- coding: utf-8 -*-

import sys
sys.path.append("./")
import config

import pandas as pd
from openpyxl import load_workbook
#sqlalchemy 연동
from sqlalchemy import create_engine, text
db_connection = create_engine(f"mysql+pymysql://{config.DATABASE_CONFIG['user']}:{config.DATABASE_CONFIG['password']}@{config.DATABASE_CONFIG['host']}/{config.DATABASE_CONFIG['dbname']}")
conn = db_connection.connect()


# def header_merge_list():
#     test_df = pd.DataFrame(sheet_list[:header_len])
#         test_df = test_df.T
#         for i in range(header_len):
#             if i != header_len-1:
#                 test_df.iloc[:,[i]] = test_df.iloc[:,[i]].fillna(method="ffill")
#         test_df.fillna('', inplace=True)
#         test_df['header'] = test_df[:].apply('_'.join, axis=1)
#         header_list = test_df['header'].to_list()
#         header_list = [v.rstrip('_') for v in header_list]
#         header_list = [v.strip() for v in header_list]
#     return header_list


if __name__ == "__main__":
    input_xlsx_path = "./sample.xlsx"
    load_wb = load_workbook(input_xlsx_path, data_only=True)
    load_data_ws = load_wb['Data']
    load_ws = load_wb.active

    # 모든 행과 열 출력
    all_values = list()
    for row in load_ws.rows:
        row_value = list()
        for cell in row:
            row_value.append(cell.value)
        all_values.append(row_value)
    df = pd.DataFrame(all_values)

    header_list = list(df.iloc[24,11:21])
    new_df = df.iloc[29:161,11:21]
    new_df.columns = header_list
    
    new_df.to_sql(name="result",con=db_connection, if_exists='replace', index=False)