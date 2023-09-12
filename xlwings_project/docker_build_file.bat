@echo off
cd docker_build_file
uvicorn app.main:app --host=127.0.0.1 --port=8000