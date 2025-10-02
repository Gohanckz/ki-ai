@echo off
chcp 65001 > nul
title KI - Setup Diagnostics
cls

echo ========================================
echo    KI - Setup Diagnostics
echo ========================================
echo.

cd /d "%~dp0"

echo [CHECK 1] Current Directory
echo Location: %cd%
echo.

echo [CHECK 2] Python Installation
python --version 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Python not found in PATH
) else (
    echo [PASS] Python detected
)
echo.

echo [CHECK 3] Virtual Environment
set VENV_PATH=%~dp0..\venv\Scripts\activate.bat
echo [INFO] Looking for venv at: %VENV_PATH%
if exist "%VENV_PATH%" (
    echo [PASS] Virtual environment found
    call "%VENV_PATH%" 2>nul
    echo [INFO] Venv activated successfully
) else (
    echo [FAIL] Virtual environment NOT found
    echo.
    echo [FIX] The venv should be at: C:\Users\Gohanckz\Desktop\IA-Proyect\venv
    echo      If it exists elsewhere, update the path in START_KI.bat
)
echo.

echo [CHECK 4] Required Python Packages
call ..\venv\Scripts\activate.bat > nul 2>&1
python -c "import gradio; print('[PASS] gradio:', gradio.__version__)" 2>&1 || echo [FAIL] gradio not installed
python -c "import ollama; print('[PASS] ollama installed')" 2>&1 || echo [FAIL] ollama not installed
python -c "import transformers; print('[PASS] transformers:', transformers.__version__)" 2>&1 || echo [FAIL] transformers not installed
echo.

echo [CHECK 5] Ollama Service
curl -s http://localhost:11434/api/version > nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS] Ollama is running
    curl -s http://localhost:11434/api/version
) else (
    echo [FAIL] Ollama not running
    echo [INFO] Start Ollama: ollama serve
    where ollama 2>&1
    if %errorlevel% neq 0 (
        echo [FAIL] Ollama not found in PATH
        echo [INFO] Download from: https://ollama.ai/download
    )
)
echo.

echo [CHECK 6] KI Project Structure
if exist "frontend\app.py" (
    echo [PASS] frontend\app.py found
) else (
    echo [FAIL] frontend\app.py NOT found
)

if exist "backend\utils\config.py" (
    echo [PASS] backend\utils\config.py found
) else (
    echo [FAIL] backend\utils\config.py NOT found
)
echo.

echo [CHECK 7] Storage Directory
python -c "from backend.utils.config import settings; print('[INFO] Storage path:', settings.storage_path)" 2>&1
echo.

echo ========================================
echo    Diagnostics Complete
echo ========================================
echo.

echo [SUMMARY]
echo If all checks pass, you can run: START_KI.bat
echo If checks fail, follow the [FIX] instructions above
echo.

pause
