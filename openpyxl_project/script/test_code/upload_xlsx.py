# -*- coding: utf-8 -*-

import sys
sys.path.append("./")
import config

import os
import pandas as pd

#sqlalchemy 연동
from sqlalchemy import create_engine, text
db_connection = create_engine(f"mysql+pymysql://{config.DATABASE_CONFIG['user']}:{config.DATABASE_CONFIG['password']}@{config.DATABASE_CONFIG['host']}/{config.DATABASE_CONFIG['dbname']}")
conn = db_connection.connect()

def upload_xlsx(input_xlsx_path):
        input_xlsx_df = pd.read_excel(input_xlsx_path,sheet_name = 1)
        input_xlsx_df.columns = input_xlsx_df.iloc[8]
        input_xlsx_df = input_xlsx_df.iloc[9:,2:]
        
        input_xlsx_df.to_sql(name="sample",con=db_connection, if_exists='replace', index=False)
        
        conn.execute(text("alter table sample change `SUM(AMT)` `SUM(AMT)` DOUBLE;"))
        conn.commit()

if __name__ == "__main__":
    
    input_xlsx_path = "./sample.xlsx"
    upload_xlsx(input_xlsx_path)