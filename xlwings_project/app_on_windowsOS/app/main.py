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

## fastapi 인스턴스 저장
app = FastAPI()

@app.post('/uploadfile/')
async def uploadfile(request: Request, file: UploadFile):
    print(1)
    UPLOAD_DIRECTORY = "./input_file/"
    contents = await file.read()
    with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as f:
        f.write(contents)
    excute_vba.excute_vba(file.filename)
    excel_to_sql.excel_to_sql(file.filename)

if __name__ == "__main__":
    uvicorn.run(app, host = '0.0.0.0', port = 8001)