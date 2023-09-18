# -*- coding: utf-8 -*-

import sys
sys.path.append("./")

from app import db_session
from python import excel_to_sql
from python import excute_vba

import os
import time
import uvicorn
import pandas as pd
import multiprocessing
from typing import List
from pathlib import Path
from pydantic import BaseModel
from fastapi import FastAPI, Request, File, UploadFile
from threading import Thread

def file_upload(file):
    print(file.filename)
    UPLOAD_DIRECTORY = "./input_file/"
    contents = file.file.read()
    with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as f:
        f.write(contents)

## fastapi 인스턴스 저장
app = FastAPI()

@app.get('/')
def main(request: Request):
    print('hi')
    time.sleep(5)
    print('done')
    return 'onWindows main page'

@app.post("/upload1")
def upload(file: UploadFile = File(...)):
    UPLOAD_DIRECTORY = "./input_file/"
    contents = file.file.read()
    with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as f:
        f.write(contents)
    excute_vba.excute_vba(file.filename)
    # excel_to_sql.excel_to_sql(file.filename
    return {"message": f"Successfully uploaded {file.filename}"}

@app.post("/upload2")
def upload(file: UploadFile = File(...)):
    file_upload(file)
    excute_vba.excute_vba(file.filename)
    # excel_to_sql.excel_to_sql(file.filename
    return {"message": f"Successfully uploaded {file.filename}"}

@app.post("/vba_parsing")
def upload(files: List[UploadFile] = File(...)):
    for file in files:
        p = multiprocessing.Process(target=excute_vba.excute_vba, args=(file.filename, ))
        p.start()
        p.join()
        # excute_vba.excute_vba(file.filename)
        # excel_to_sql.excel_to_sql(file.filename)
    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}

if __name__ == "__main__":
    uvicorn.run(app, host = '127.0.0.1', port = 8001)