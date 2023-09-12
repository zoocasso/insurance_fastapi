@echo off
cd app_on_windowsOS
uvicorn app.main:app --host=0.0.0.0 --port=8001