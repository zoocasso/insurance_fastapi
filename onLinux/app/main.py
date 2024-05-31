# -*- coding: utf-8 -*-

import sys
sys.path.append("./")

from app import db_session
from script import xlsx_parsing

##for pyinstaller
import pymysql
import pandas as pd
#################

import os
import uvicorn
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, UploadFile
# from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ## CORS
# origins = [
#     "*",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post('/xlsx_parsing')
async def uploadfile(request: Request, file: UploadFile):
    # 파일 복사하여 input_xlsx 폴더 내에 저장
    UPLOAD_DIRECTORY = "./input_xlsx"
    contents = await file.read()
    with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as f:
        f.write(contents)
    
    # xlsx_parsing.py에서 클래스 호출하여 엑셀 파싱 작업
    xlsx_parsing_class = xlsx_parsing.xlsx_parsing()
    xlsx_parsing_class.main(UPLOAD_DIRECTORY+'/'+file.filename)

@app.get('/view_xlwings')
async def view_xlwings(request: Request):
    mysql_session = db_session.mysql_session()
    db_data = mysql_session.select_all_from_table("생보사_Test_샘플_Result")
    header_list = mysql_session.get_header_list("생보사_Test_샘플_Result")
    mysql_session.db_close()
    return templates.TemplateResponse("view_xlwings.html", {"request":request, "db_data":db_data, "header_list":header_list})

@app.get('/view_portf')
async def view_portf(request: Request, portf:str):
    mysql_session = db_session.mysql_session()
    db_data = mysql_session.select_all_from_table('원수_tb_data_True_LANIXX_AZ')
    header_list = mysql_session.get_header_list('원수_tb_data_True_LANIXX_AZ')
    mysql_session.db_close()
    return templates.TemplateResponse("view_portf.html", {"request":request, "db_data":db_data, "header_list":header_list, "cell_value":portf})

@app.get('/view_data')
async def view_data(request: Request, ACC_PERIOD:str, ACC_PERIOD_TYPE:str, M_LIAB_ITEM:str, M_ACC_EVENT:str, cell_value:str = ''):
    mysql_session = db_session.mysql_session()
    db_data = mysql_session.select_data_table(ACC_PERIOD,ACC_PERIOD_TYPE,M_LIAB_ITEM,M_ACC_EVENT)
    header_list = mysql_session.get_header_list('data')
    sql_str = mysql_session.get_sql_str(ACC_PERIOD,ACC_PERIOD_TYPE,M_LIAB_ITEM,M_ACC_EVENT)
    mysql_session.db_close()
    return templates.TemplateResponse("view_data.html", {"request":request, "db_data":db_data, "header_list":header_list, "cell_value":cell_value, "sql_str":sql_str})

@app.get('/table_view')
async def table_view(request: Request, table_name: str):
    mysql_session = db_session.mysql_session()
    db_data = mysql_session.select_all_from_table(table_name)
    header_list = mysql_session.get_header_list(table_name)
    mysql_session.db_close()
    return templates.TemplateResponse("view.html", {"request":request,"db_data":db_data, "header_list":header_list, "table_name":table_name})

@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

if __name__ == "__main__":
    uvicorn.run(app, host = '0.0.0.0', port = 8000)