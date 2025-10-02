#!/bin/bash
clear
echo "=========================================="
echo "   KI - AI Training Platform"
echo "=========================================="
echo ""
source /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/venv/bin/activate
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki
echo "Starting server..."
echo "Open: http://localhost:7860"
echo ""
python3 frontend/app.py
