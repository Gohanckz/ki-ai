#!/bin/bash

clear

cat << "EOF"
========================================
   KI - Automatic Installation
========================================
EOF

echo ""
echo "This script will install all required dependencies"
echo ""

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Step 1: Verify Python
echo "[STEP 1/4] Verifying Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python not found!"
    echo "[INFO] Please install Python 3.8+ first"
    exit 1
fi
echo "[OK] Python detected: $(python3 --version)"
echo ""

# Step 2: Activate venv
echo "[STEP 2/4] Activating virtual environment..."
VENV_PATH="$DIR/../venv/bin/activate"

if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
    echo "[OK] Virtual environment activated"
else
    echo "[ERROR] Virtual environment not found at: $VENV_PATH"
    echo "[INFO] Creating new virtual environment..."

    cd "$DIR/.."
    python3 -m venv venv

    if [ $? -eq 0 ]; then
        echo "[OK] Virtual environment created"
        source venv/bin/activate
        cd "$DIR"
    else
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
fi
echo ""

# Step 3: Install dependencies
echo "[STEP 3/4] Installing required packages..."
echo "[INFO] This may take a few minutes..."
echo ""

echo "[*] Installing core dependencies..."
pip install pydantic-settings python-dotenv rich --quiet
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install core dependencies"
    exit 1
fi
echo "[OK] Core dependencies installed"

echo "[*] Installing UI framework (Gradio)..."
pip install gradio --quiet
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install Gradio"
    exit 1
fi
echo "[OK] Gradio installed"

echo "[*] Installing Ollama client..."
pip install ollama --quiet
if [ $? -ne 0 ]; then
    echo "[WARNING] Failed to install Ollama (not critical)"
else
    echo "[OK] Ollama client installed"
fi

echo "[*] Installing document parsers..."
pip install PyPDF2 python-docx beautifulsoup4 markdown --quiet
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install parsers"
    exit 1
fi
echo "[OK] Document parsers installed"

echo ""

# Step 4: Verify installation
echo "[STEP 4/4] Verifying installation..."
python3 -c "import gradio; print('[OK] Gradio version:', gradio.__version__)" 2>&1
if [ $? -ne 0 ]; then
    echo "[ERROR] Gradio verification failed"
    exit 1
fi

python3 -c "import ollama; print('[OK] Ollama client ready')" 2>&1
python3 -c "from backend.utils.config import settings; print('[OK] Config module loaded')" 2>&1
if [ $? -ne 0 ]; then
    echo "[ERROR] Config verification failed"
    exit 1
fi

echo ""
cat << "EOF"
========================================
   Installation Complete!
========================================

[NEXT STEPS]

1. Install Ollama (optional, for dataset generation):
   Download from: https://ollama.ai/download
   Or on Linux: curl -fsSL https://ollama.ai/install.sh | sh

2. Start Ollama service (if installed):
   ollama serve

3. Launch KI Platform:
   ./start_ki.sh

========================================
EOF

echo ""
