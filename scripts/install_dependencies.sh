#!/bin/bash
# Script para instalar dependencias adicionales en venv existente

echo "🔧 Instalando dependencias adicionales para KI..."

# Activar venv existente
source /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/venv/bin/activate

echo "📦 Venv activado: $(which python)"
echo "Python version: $(python --version)"

# Instalar dependencias adicionales
echo "📥 Instalando paquetes adicionales..."

pip install -q gradio==4.12.0
pip install -q fastapi==0.109.0 uvicorn[standard]==0.27.0
pip install -q pydantic-settings==2.1.0
pip install -q ollama==0.1.6
pip install -q pdfplumber==0.10.3
pip install -q python-markdown==3.5.1
pip install -q rich==13.7.0
pip install -q aiofiles==23.2.1
pip install -q chromadb==0.4.22
pip install -q plotly==5.18.0
pip install -q gpustat==1.1.1

echo "✅ Instalación completada"
echo ""
echo "📋 Paquetes instalados:"
pip list | grep -E "(gradio|fastapi|ollama|pydantic-settings)"

echo ""
echo "🚀 Para usar KI:"
echo "  cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki"
echo "  source ../venv/bin/activate"
echo "  python frontend/app.py"
