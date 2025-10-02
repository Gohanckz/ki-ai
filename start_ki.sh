#!/bin/bash

clear

cat << "EOF"
========================================
   KI - AI Training Platform v0.1.0
========================================
EOF

echo ""
echo "[*] Starting KI Platform..."
echo ""

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Step 1: Check Python
echo "[1/4] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python not found!"
    echo "[INFO] Please install Python 3.8+ first"
    exit 1
fi
echo "[OK] Python detected"

# Step 2: Activate venv
echo ""
echo "[2/4] Activating virtual environment..."
VENV_PATH="$DIR/../venv/bin/activate"

if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
    echo "[OK] Virtual environment activated"
else
    echo "[ERROR] Virtual environment not found!"
    echo "[INFO] Expected location: $VENV_PATH"
    echo ""
    echo "[FIX] Run: ./install.sh to set up everything automatically"
    exit 1
fi

# Step 3: Check dependencies
echo ""
echo "[3/4] Checking dependencies..."
if python3 -c "import gradio" &> /dev/null; then
    echo "[OK] Dependencies ready"
else
    echo "[WARNING] Gradio not installed"
    echo "[INFO] Installing required packages..."
    pip install gradio ollama beautifulsoup4 markdown pydantic-settings --quiet
    if [ $? -eq 0 ]; then
        echo "[OK] Dependencies installed"
    else
        echo "[ERROR] Failed to install dependencies"
        exit 1
    fi
fi

# Step 4: Check Ollama (optional)
echo ""
echo "[4/4] Checking Ollama (optional)..."
if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "[OK] Ollama is running"
else
    echo "[WARNING] Ollama not running"
    echo "[INFO] Dataset generation will not work without Ollama"
    echo "[INFO] To start Ollama manually:"
    echo "[INFO]   Open new terminal and run: ollama serve"
    echo ""
    echo "[?] Continue without Ollama? (Press Enter to continue, Ctrl+C to exit)"
    read
fi

# Launch application
echo ""
cat << "EOF"
========================================
 Starting KI Platform...
========================================
EOF
echo ""
echo "Opening browser at: http://localhost:7860"
echo ""

python3 frontend/app.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Application failed to start"
    echo "[INFO] Check error messages above"
    exit 1
fi
