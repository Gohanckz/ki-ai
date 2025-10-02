@echo off
chcp 65001 > nul
title KI - AI Training Platform
cls

echo ========================================
echo    KI - AI Training Platform v0.1.0
echo ========================================
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Verificar Python
echo [1/4] Checking Python...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo [INFO] Please install Python 3.8+ and add it to PATH
    pause
    exit /b 1
)
echo [OK] Python detected

REM Verificar y activar venv
echo.
echo [2/4] Activating virtual environment...
set VENV_PATH=%~dp0..\venv\Scripts\activate.bat

if exist "%VENV_PATH%" (
    call "%VENV_PATH%"
    echo [OK] Virtual environment activated
) else (
    echo [ERROR] Virtual environment not found!
    echo [INFO] Expected location: C:\Users\Gohanckz\Desktop\IA-Proyect\venv
    echo.
    echo [FIX] Run: INSTALL.bat to set up everything automatically
    pause
    exit /b 1
)

REM Verificar Gradio instalado
echo.
echo [3/4] Checking dependencies...
python -c "import gradio" > nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Gradio not installed
    echo [INFO] Installing required packages...
    pip install gradio ollama beautifulsoup4 markdown --quiet
    if %errorlevel% equ 0 (
        echo [OK] Dependencies installed
    ) else (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo [OK] Dependencies ready
)

REM Verificar Ollama (opcional)
echo.
echo [4/4] Checking Ollama (optional)...
curl -s http://localhost:11434/api/version > nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Ollama is running
) else (
    echo [WARNING] Ollama not running
    echo [INFO] Dataset generation will not work without Ollama
    echo [INFO] To start Ollama manually:
    echo [INFO]   1. Open new terminal
    echo [INFO]   2. Run: ollama serve
    echo.
    echo [?] Continue without Ollama? (Press any key to continue, Ctrl+C to exit)
    pause > nul
)

REM Lanzar aplicación
echo.
echo ========================================
echo  Starting KI Platform...
echo ========================================
echo.
echo Opening browser at: http://localhost:7860
echo.

python frontend\app.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application failed to start
    echo [INFO] Check error messages above
    pause
    exit /b 1
)
