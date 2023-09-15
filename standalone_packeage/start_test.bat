@echo off

start cmd /C call app_on_windowsOS.bat
start cmd /C call docker_build_file.bat
start .\index.html