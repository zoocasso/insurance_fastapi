# -*- coding: utf-8 -*-

import sys
sys.path.append("./")

from app import db_session

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


if __name__ == "__main__":
    uvicorn.run(app, host = '127.0.0.1', port = 8002)