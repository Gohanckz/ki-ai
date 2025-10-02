@echo off
chcp 65001 > nul
title KI - AI Training Platform
color 0A

echo.
echo  ========================================
echo     KI - AI Training Platform v0.1.0
echo  ========================================
echo.
echo  [*] Starting KI Platform...
echo.

cd /d "%~dp0"

REM Activar venv
echo  [*] Activating virtual environment...
if exist "..\venv\Scripts\activate.bat" (
    call ..\venv\Scripts\activate.bat
    echo  [OK] Virtual environment activated
) else (
    echo  [ERROR] Virtual environment not found at ..\venv\Scripts\activate.bat
    echo  [INFO] Please ensure the venv exists at: %~dp0..\venv
    pause
    exit /b 1
)

REM Verificar Ollama (opcional - solo warning)
echo  [*] Checking Ollama...
curl -s http://localhost:11434/api/version > nul 2>&1
if %errorlevel% equ 0 (
    echo  [OK] Ollama is running
) else (
    echo  [!] Warning: Ollama not detected
    echo  [INFO] Please start Ollama manually if you need it:
    echo  [INFO]   Open a new terminal and run: ollama serve
    echo.
)

REM Iniciar aplicación
echo  [*] Launching UI...
echo.
python frontend\app.py

if %errorlevel% neq 0 (
    echo.
    echo  [ERROR] Failed to launch application
    echo  [INFO] Check the error messages above
)

pause
