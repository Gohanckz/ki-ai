#!/bin/bash

echo "=========================================="
echo "   KI - Quick Diagnostics"
echo "=========================================="
echo ""

# Check Python
echo "[1] Python:"
python3 --version 2>/dev/null && echo "✓ OK" || echo "✗ NOT FOUND"
echo ""

# Check venv
echo "[2] Virtual Environment:"
VENV_PATH="/mnt/c/Users/Gohanckz/Desktop/IA-Proyect/venv/bin/activate"
if [ -f "$VENV_PATH" ]; then
    echo "✓ Found at: $VENV_PATH"
    source "$VENV_PATH"
else
    echo "✗ NOT FOUND"
fi
echo ""

# Check packages
echo "[3] Python Packages:"
python3 -c "import gradio" 2>/dev/null && echo "✓ gradio" || echo "✗ gradio (missing)"
python3 -c "import ollama" 2>/dev/null && echo "✓ ollama" || echo "✗ ollama (missing)"
python3 -c "import pydantic_settings" 2>/dev/null && echo "✓ pydantic-settings" || echo "✗ pydantic-settings (missing)"
echo ""

# Check Ollama service
echo "[4] Ollama Service:"
curl -s http://localhost:11434/api/version > /dev/null 2>&1 && echo "✓ Running" || echo "✗ Not running"
echo ""

# Summary
echo "=========================================="
echo "NEXT STEPS:"
echo ""
echo "If packages are missing, run:"
echo "  ./install.sh"
echo ""
echo "If everything is OK, run:"
echo "  ./start_ki.sh"
echo "=========================================="
