#!/bin/bash

clear

echo "=========================================="
echo "   KI - AI Training Platform"
echo "=========================================="
echo ""

# Activate venv
source /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/venv/bin/activate

# Check Ollama (optional)
if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "✓ Ollama running"
else
    echo "⚠ Ollama not running (optional - UI will work without it)"
fi

echo ""
echo "Starting KI Platform..."
echo "Open: http://localhost:7860"
echo ""

# Run app
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki
python3 frontend/app.py
