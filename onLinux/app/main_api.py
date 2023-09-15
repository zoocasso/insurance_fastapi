# -*- coding: utf-8 -*-

import sys
sys.path.append("./")

from app import db_session
from script import xlsx_parsing
from script import json_

import os
import uvicorn
from fastapi import FastAPI, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

@app.get('/table_view')
async def table_view(request: Request, table_name: str):
    # db_session.py에서 클래스 호출하여 db 적재 작업
    mysql_session = db_session.mysql_session()
    
    db_data = mysql_session.select_all_from_table(table_name)
    mysql_session.db_close()

    # return된 data를 정제 및 가공 작업
    result_json = json_.main(db_data)
    return result_json

@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

if __name__ == "__main__":
    uvicorn.run(app, host = '0.0.0.0', port = 8000)