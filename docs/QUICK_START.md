# 🚀 KI Platform - Quick Start Guide

## ⚡ Inicio Rápido (3 pasos)

### Paso 1: Verificar Setup
```bash
# Ejecutar diagnóstico
CHECK_SETUP.bat
```

### Paso 2: Corregir Problemas (si hay)

**Si falta el venv:**
```bash
cd C:\Users\Gohanckz\Desktop\IA-Proyect
python -m venv venv
venv\Scripts\activate.bat
pip install -r ki/requirements.txt
```

**Si falta Gradio:**
```bash
cd C:\Users\Gohanckz\Desktop\IA-Proyect
venv\Scripts\activate.bat
pip install gradio ollama beautifulsoup4 markdown
```

**Si falta Ollama:**
- Descargar: https://ollama.ai/download
- Instalar Ollama en Windows
- Abrir nuevo terminal y ejecutar: `ollama serve`

### Paso 3: Iniciar KI Platform
```bash
# Opción 1: Launcher mejorado (recomendado)
START_KI.bat

# Opción 2: Launcher simple
KI.bat

# Opción 3: Manual
cd C:\Users\Gohanckz\Desktop\IA-Proyect\ki
..\venv\Scripts\activate.bat
python frontend\app.py
```

---

## ❌ Solución de Errores Comunes

### Error: "El sistema no puede encontrar la ruta especificada"
**Causa:** El venv no está en la ubicación esperada

**Solución:**
```bash
# 1. Verificar si existe el venv
dir C:\Users\Gohanckz\Desktop\IA-Proyect\venv

# 2. Si no existe, crear:
cd C:\Users\Gohanckz\Desktop\IA-Proyect
python -m venv venv

# 3. Activar e instalar dependencias:
venv\Scripts\activate.bat
cd ki
pip install -r requirements.txt
pip install gradio ollama beautifulsoup4 markdown
```

### Error: "El sistema no puede encontrar el archivo ollama"
**Causa:** Ollama no está instalado o no está en PATH

**Solución A - Instalar Ollama:**
1. Descargar desde: https://ollama.ai/download
2. Instalar (se añade automáticamente al PATH)
3. Abrir nuevo terminal: `ollama serve`

**Solución B - Omitir Ollama (temporalmente):**
- El launcher ya permite continuar sin Ollama
- Dataset generation no funcionará, pero la UI sí se abrirá

### Error: Caracteres extraños en consola (ÔòöÔòÉ)
**Causa:** Encoding UTF-8 no configurado

**Solución:** Usar `START_KI.bat` que incluye `chcp 65001`

### Error: "ModuleNotFoundError: No module named 'gradio'"
**Causa:** Gradio no instalado en el venv

**Solución:**
```bash
cd C:\Users\Gohanckz\Desktop\IA-Proyect
venv\Scripts\activate.bat
pip install gradio ollama beautifulsoup4 markdown
```

---

## 📋 Pre-requisitos

### Requeridos:
- ✅ Python 3.8+ instalado
- ✅ Virtual environment en: `C:\Users\Gohanckz\Desktop\IA-Proyect\venv`
- ✅ Dependencias instaladas en venv

### Opcionales (para dataset generation):
- ⚙️ Ollama instalado
- ⚙️ Modelo descargado: `ollama pull llama3.1`

---

## 🔧 Comandos Útiles

### Verificar instalación:
```bash
# Ver versión Python
python --version

# Ver paquetes instalados
pip list

# Verificar Gradio
python -c "import gradio; print(gradio.__version__)"

# Verificar Ollama
curl http://localhost:11434/api/version
```

### Gestión de Ollama:
```bash
# Iniciar servidor
ollama serve

# Listar modelos
ollama list

# Descargar modelo
ollama pull llama3.1

# Test rápido
ollama run llama3.1 "Hello"
```

### Desarrollo:
```bash
# Activar venv
cd C:\Users\Gohanckz\Desktop\IA-Proyect
venv\Scripts\activate.bat

# Ir a proyecto
cd ki

# Ejecutar app directamente
python frontend\app.py

# Ejecutar con logs
python frontend\app.py --verbose
```

---

## 🎯 Flujo Completo de Instalación

### Primera vez (Setup completo):

```bash
# 1. Crear venv (si no existe)
cd C:\Users\Gohanckz\Desktop\IA-Proyect
python -m venv venv

# 2. Activar venv
venv\Scripts\activate.bat

# 3. Instalar dependencias base
pip install torch torchvision torchaudio transformers peft bitsandbytes

# 4. Instalar dependencias de KI
cd ki
pip install -r requirements.txt
pip install gradio ollama beautifulsoup4 markdown

# 5. Verificar instalación
python CHECK_SETUP.bat

# 6. Iniciar KI
START_KI.bat
```

### Ejecuciones posteriores:

```bash
# Opción 1: Doble click
START_KI.bat

# Opción 2: Desde terminal
cd C:\Users\Gohanckz\Desktop\IA-Proyect\ki
START_KI.bat
```

---

## 📁 Estructura de Directorios Esperada

```
C:\Users\Gohanckz\Desktop\IA-Proyect\
├── venv\                          ← Virtual environment (DEBE EXISTIR)
│   └── Scripts\
│       └── activate.bat
│
└── ki\                            ← Proyecto KI
    ├── START_KI.bat              ← Launcher mejorado (USAR ESTE)
    ├── KI.bat                     ← Launcher simple
    ├── CHECK_SETUP.bat            ← Diagnóstico
    ├── frontend\
    │   └── app.py
    ├── backend\
    └── storage\
```

---

## 🌐 Acceder a la UI

Una vez iniciado:
- URL: http://localhost:7860
- Se abre automáticamente en el navegador
- 4 tabs disponibles:
  - 📁 Dataset Manager
  - 🎓 Training Studio
  - 🧪 Testing Lab
  - ⚙️ Settings

---

## 💡 Tips

1. **Siempre usar `START_KI.bat`** - Tiene mejor manejo de errores
2. **Ejecutar `CHECK_SETUP.bat` primero** si hay problemas
3. **Ollama es opcional** - La UI funciona sin él
4. **Los caracteres raros** se solucionan con UTF-8 encoding (ya incluido en START_KI.bat)

---

## 🆘 Ayuda Adicional

Si persisten errores:
1. Ejecutar: `CHECK_SETUP.bat`
2. Leer los mensajes de error
3. Seguir las instrucciones [FIX]
4. Si falla, compartir output de CHECK_SETUP.bat

---

**Última actualización:** 2025-10-02
**Versión:** v0.1.0
