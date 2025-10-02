#!/bin/bash

clear

cat << "EOF"
╔════════════════════════════════════════╗
║   KI - AI Training Platform v0.1.0    ║
╚════════════════════════════════════════╝
EOF

echo ""
echo "[*] Starting KI Platform..."
echo ""

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Activar venv
echo "[*] Activating virtual environment..."
source ../venv/bin/activate

# Verificar Ollama
echo "[*] Checking Ollama..."
if ! curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "[!] Warning: Ollama not running"
    echo "[*] Starting Ollama..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

# Verificar que Ollama esté respondiendo
if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "[✓] Ollama is running"
else
    echo "[!] Warning: Ollama may not be running correctly"
fi

# Iniciar aplicación
echo "[*] Launching UI..."
echo ""
python frontend/app.py

read -p "Press any key to exit..."
