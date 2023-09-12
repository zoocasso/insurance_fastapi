# -*- coding: utf-8 -*-

import sys
sys.path.append("./")

from app import db_session
from python import excel_to_sql
from python import excute_vba

import os
import uvicorn
import pandas as pd
from pathlib import Path
from pydantic import BaseModel
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

## fastapi 인스턴스 저장
app = FastAPI()

## static 폴더 mounting작업
app.mount("/static", StaticFiles(directory="static"), name="static")

## 템플릿 구성을 위해 Jinja2 활용
templates = Jinja2Templates(directory="templates")


@app.post('/uploadfile/')
async def uploadfile(request: Request, file: UploadFile):
    UPLOAD_DIRECTORY = "./input_file/"
    contents = await file.read()
    with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as f:
        f.write(contents)
    excute_vba.excute_vba(file.filename)
    excel_to_sql.excel_to_sql(file.filename)
    mysql_session = db_session.mysql_session()
    # #next step
    # db_data = mysql_session.select_all_from_table("생보사_Test_샘플_Result")
    # header_list = mysql_session.get_header_list("생보사_Test_샘플_Result")
    # mysql_session.db_close()
    return templates.TemplateResponse("excel_view.html", {"request":request, "db_data":db_data, "header_list":header_list})

# class Item(BaseModel):
#     name: str

# @app.post("/create")
# async def create(request:Request, item:Item):
#     mysql_session = db_session.mysql_session()
#     mysql_session.alter_table_add_column(item.name)
#     mysql_session.db_close()

# @app.post("/delete")
# async def delete(request:Request, item:Item):
#     mysql_session = db_session.mysql_session()
#     mysql_session.alter_table_drop_column(item.name)
#     mysql_session.db_close()

# class Row_form(BaseModel):
#     date: str
#     open: str
#     high: str
#     low: str
#     close: str
#     volume: str
#     change: str


# @app.post("/row_insert")
# async def row_insert(request:Request, row_form:Row_form):
#     mysql_session = db_session.mysql_session()
#     mysql_session.insert_into_table_value(row_form)
#     mysql_session.db_close()

# 메인페이지
@app.get("/")
async def main(request:Request):
    return templates.TemplateResponse("index.html", {"request":request})

@app.get("/excel_view")
async def excel_view(request:Request):
    mysql_session = db_session.mysql_session()
    db_data = mysql_session.select_all_from_table("생보사_Test_샘플_Result")
    header_list = mysql_session.get_header_list("생보사_Test_샘플_Result")
    mysql_session.db_close()
    return templates.TemplateResponse("excel_view.html", {"request":request, "db_data":db_data, "header_list":header_list})

# @app.get("/view")
# async def finplot_data(request:Request):
#     mysql_session = db_session.mysql_session()
#     finplot_data = mysql_session.select_all_from_finplot()
#     header_list = mysql_session.get_header_list()
#     mysql_session.db_close()
#     return templates.TemplateResponse("finplot.html", {"request":request, "finplot_data":finplot_data, "header_list":header_list})


if __name__ == "__main__":
    uvicorn.run(app, host = '127.0.0.1', port = 8001)