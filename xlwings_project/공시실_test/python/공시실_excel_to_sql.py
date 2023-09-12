# -*- coding: utf-8 -*-

import sys
sys.path.append("./")
import config

import os
import pandas as pd
from tqdm import tqdm
from openpyxl import load_workbook

#sqlalchemy 연동
from sqlalchemy import create_engine
db_connection_str = f"mysql+pymysql://{config.DATABASE_CONFIG['user']}:{config.DATABASE_CONFIG['password']}@{config.DATABASE_CONFIG['host']}/{config.DATABASE_CONFIG['dbname']}"
db_connection = create_engine(db_connection_str)

input_insurance_list = ['변액보험','보장성보험','실손의료보험','연금저축','저축성보험','퇴직보험']
for input_insurance in input_insurance_list:
    default_dir = config.default_dir[input_insurance]
    header_len = config.header_len[input_insurance]

    for file_name in tqdm(os.listdir(default_dir)):
        #openpyxl로 액셀 다루기
        wb = load_workbook(default_dir+file_name, data_only=False)
        ws = wb.active

        # 모든 행과 열 출력
        sheet_list = list()
        for row in ws.rows:
            row_list = list()
            for cell in row:
                row_list.append(cell.value)
            sheet_list.append(row_list)
        test_df = pd.DataFrame(sheet_list[:header_len])
        test_df = test_df.T
        for i in range(header_len):
            if i != header_len-1:
                test_df.iloc[:,[i]] = test_df.iloc[:,[i]].fillna(method="ffill")
        test_df.fillna('', inplace=True)
        test_df['header'] = test_df[:].apply('_'.join, axis=1)
        header_list = test_df['header'].to_list()
        header_list = [v.rstrip('_') for v in header_list]
        header_list = [v.strip() for v in header_list]
        sheet_df = pd.DataFrame(sheet_list[header_len:], columns=header_list)        
        sheet_df = sheet_df.fillna(method="ffill")
        
        # sqlalchemy 활용하여 mysql 적재 
        sheet_df.to_sql(name=file_name.split('.')[0],con=db_connection, if_exists='append', index=False)