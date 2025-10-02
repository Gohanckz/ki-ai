#!/bin/bash

clear

cat << "EOF"
========================================
   KI - Setup Diagnostics
========================================
EOF

echo ""

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "[CHECK 1] Current Directory"
echo "Location: $DIR"
echo ""

echo "[CHECK 2] Python Installation"
if command -v python3 &> /dev/null; then
    python3 --version
    echo "[PASS] Python detected"
else
    echo "[FAIL] Python not found"
fi
echo ""

echo "[CHECK 3] Virtual Environment"
VENV_PATH="$DIR/../venv/bin/activate"
echo "[INFO] Looking for venv at: $VENV_PATH"
if [ -f "$VENV_PATH" ]; then
    echo "[PASS] Virtual environment found"
    source "$VENV_PATH"
    echo "[INFO] Venv activated successfully"
    echo "[INFO] Python location: $(which python3)"
else
    echo "[FAIL] Virtual environment NOT found"
    echo ""
    echo "[FIX] Create virtual environment:"
    echo "     cd $DIR/.."
    echo "     python3 -m venv venv"
fi
echo ""

echo "[CHECK 4] Required Python Packages"
source "$VENV_PATH" 2>/dev/null

if python3 -c "import gradio" 2>/dev/null; then
    python3 -c "import gradio; print('[PASS] gradio:', gradio.__version__)"
else
    echo "[FAIL] gradio not installed"
fi

if python3 -c "import ollama" 2>/dev/null; then
    echo "[PASS] ollama installed"
else
    echo "[FAIL] ollama not installed"
fi

if python3 -c "import transformers" 2>/dev/null; then
    python3 -c "import transformers; print('[PASS] transformers:', transformers.__version__)"
else
    echo "[FAIL] transformers not installed"
fi

if python3 -c "import pydantic_settings" 2>/dev/null; then
    echo "[PASS] pydantic-settings installed"
else
    echo "[FAIL] pydantic-settings not installed"
fi
echo ""

echo "[CHECK 5] Ollama Service"
if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "[PASS] Ollama is running"
    curl -s http://localhost:11434/api/version
else
    echo "[FAIL] Ollama not running"
    echo "[INFO] Start Ollama: ollama serve"
    if command -v ollama &> /dev/null; then
        echo "[INFO] Ollama binary found at: $(which ollama)"
    else
        echo "[FAIL] Ollama not found in PATH"
        echo "[INFO] Download from: https://ollama.ai/download"
        echo "[INFO] Or install on Linux: curl -fsSL https://ollama.ai/install.sh | sh"
    fi
fi
echo ""

echo "[CHECK 6] KI Project Structure"
if [ -f "frontend/app.py" ]; then
    echo "[PASS] frontend/app.py found"
else
    echo "[FAIL] frontend/app.py NOT found"
fi

if [ -f "backend/utils/config.py" ]; then
    echo "[PASS] backend/utils/config.py found"
else
    echo "[FAIL] backend/utils/config.py NOT found"
fi
echo ""

echo "[CHECK 7] Storage Directory"
if python3 -c "from backend.utils.config import settings; print('[INFO] Storage path:', settings.storage_path)" 2>/dev/null; then
    :
else
    echo "[FAIL] Cannot load config module"
fi
echo ""

cat << "EOF"
========================================
   Diagnostics Complete
========================================

[SUMMARY]
If all checks pass, you can run: ./start_ki.sh
If checks fail, run: ./install.sh to fix dependencies

========================================
EOF

echo ""
