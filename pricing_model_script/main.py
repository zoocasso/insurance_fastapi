# -*- coding: utf-8 -*-

import sys
import config
sys.path.append("./")

import pandas as pd
from openpyxl import load_workbook
from sqlalchemy import create_engine
db_connection_str = f"mysql+pymysql://{config.DATABASE_CONFIG['user']}:{config.DATABASE_CONFIG['password']}@{config.DATABASE_CONFIG['host']}/{config.DATABASE_CONFIG['dbname']}"
db_connection = create_engine(db_connection_str)

def excel_to_sql(file_name,defiend_name):
    wb = load_workbook(f"{file_name}", data_only=True)
    defiend_name_object = wb.defined_names[defiend_name].destinations
    for title, coord in defiend_name_object:
        ws = wb[title][coord]

    sheet_list = list()
    for row in ws:
        row_list = list()
        for cell in row:
            row_list.append(cell.value)
        sheet_list.append(row_list)
    sheet_df = pd.DataFrame(sheet_list)

    sheet_df.to_sql(name=defiend_name, con=db_connection, if_exists='append', index=False)

if __name__ == "__main__":
    excel_to_sql("./sample_보험_PricingModel.xlsm","PDT_INFO")