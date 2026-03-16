@echo off
title Screen Translate Tool
cd /d "%~dp0"

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python khong duoc cai dat!
    echo Tai Python tai: https://python.org/downloads
    pause
    exit /b
)

:: Install dependencies nếu chưa có
pip show mss >nul 2>&1
if errorlevel 1 (
    echo [*] Dang cai dat dependencies...
    pip install -r requirements.txt
    echo.
)

:: Run
echo ========================================
echo   Screen Translate Tool
echo   Bam mui ten TRAI de bat dau
echo   ESC de thoat
echo ========================================
echo.
python main.py
pause
