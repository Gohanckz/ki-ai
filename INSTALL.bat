@echo off
chcp 65001 > nul
title KI - Automatic Installation
cls

echo ========================================
echo    KI - Automatic Installation
echo ========================================
echo.
echo This script will install all required dependencies
echo.

cd /d "%~dp0"

REM Step 1: Verify Python
echo [STEP 1/4] Verifying Python installation...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo [INFO] Please install Python 3.8+ from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python detected
echo.

REM Step 2: Activate venv
echo [STEP 2/4] Activating virtual environment...
set VENV_ACTIVATE=%~dp0..\venv\Scripts\activate.bat

if exist "%VENV_ACTIVATE%" (
    call "%VENV_ACTIVATE%"
    echo [OK] Virtual environment activated
) else (
    echo [ERROR] Virtual environment not found at:
    echo        %VENV_ACTIVATE%
    echo.
    echo [INFO] Creating new virtual environment...
    cd /d "%~dp0.."
    python -m venv venv
    if %errorlevel% equ 0 (
        echo [OK] Virtual environment created
        call venv\Scripts\activate.bat
        cd /d "%~dp0"
    ) else (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)
echo.

REM Step 3: Install dependencies
echo [STEP 3/4] Installing required packages...
echo [INFO] This may take a few minutes...
echo.

echo [*] Installing core dependencies...
pip install pydantic-settings python-dotenv rich --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install core dependencies
    pause
    exit /b 1
)
echo [OK] Core dependencies installed

echo [*] Installing UI framework (Gradio)...
pip install gradio --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Gradio
    pause
    exit /b 1
)
echo [OK] Gradio installed

echo [*] Installing Ollama client...
pip install ollama --quiet
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install Ollama (not critical)
) else (
    echo [OK] Ollama client installed
)

echo [*] Installing document parsers...
pip install PyPDF2 python-docx beautifulsoup4 markdown --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install parsers
    pause
    exit /b 1
)
echo [OK] Document parsers installed

echo.

REM Step 4: Verify installation
echo [STEP 4/4] Verifying installation...
python -c "import gradio; print('[OK] Gradio version:', gradio.__version__)" 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Gradio verification failed
    pause
    exit /b 1
)

python -c "import ollama; print('[OK] Ollama client ready')" 2>&1
python -c "from backend.utils.config import settings; print('[OK] Config module loaded')" 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Config verification failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo [NEXT STEPS]
echo.
echo 1. Install Ollama (optional, for dataset generation):
echo    Download from: https://ollama.ai/download
echo.
echo 2. Start Ollama service (if installed):
echo    Open new terminal and run: ollama serve
echo.
echo 3. Launch KI Platform:
echo    Run: START_KI.bat
echo.
echo ========================================
echo.

pause
