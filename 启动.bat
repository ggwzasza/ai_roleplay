@echo off
title AI Roleplay

set PYTHON=C:\Users\ggwza\Anaconda3\python.exe
set SCRIPT=%~dp0run.py

if not exist "%PYTHON%" (
    echo [ERROR] Python not found: %PYTHON%
    echo Please edit PYTHON variable in this script
    pause
    exit /b 1
)

"%PYTHON%" "%SCRIPT%"

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Program exited with code: %ERRORLEVEL%
    pause
)
