# 🐧 KI Platform - Guía para Linux/WSL

## ⚠️ Importante: Estás en Linux/WSL

Si estás viendo este archivo, estás usando Linux o WSL (Windows Subsystem for Linux).
**NO uses los archivos `.bat`** - esos son para Windows CMD/PowerShell.

---

## ⚡ Inicio Rápido (3 pasos)

### Paso 1: Verificar Setup
```bash
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki
./check_setup.sh
```

### Paso 2: Instalar Dependencias
```bash
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki
./install.sh
```

### Paso 3: Iniciar KI Platform
```bash
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki
./start_ki.sh
```

---

## 📋 Scripts Disponibles (Linux)

| Script | Descripción | Cuándo Usar |
|--------|-------------|-------------|
| `check_setup.sh` | Diagnóstico del setup | Primero, para ver qué falta |
| `install.sh` | Instalador automático | Si faltan dependencias |
| `start_ki.sh` | Launcher principal | Para iniciar la app |
| `KI.sh` | Launcher simple | Alternativa básica |

**❌ NO uses:** `*.bat` (son para Windows CMD)
**✅ USA:** `*.sh` (son para Linux/WSL)

---

## 🔧 Instalación Manual (si install.sh falla)

### 1. Activar venv
```bash
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect
source venv/bin/activate
```

### 2. Actualizar pip
```bash
python3 -m pip install --upgrade pip
```

### 3. Instalar dependencias core
```bash
pip install pydantic-settings python-dotenv rich
```

### 4. Instalar Gradio y Ollama
```bash
pip install gradio ollama
```

### 5. Instalar parsers
```bash
pip install PyPDF2 python-docx beautifulsoup4 markdown
```

### 6. Verificar instalación
```bash
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki
python3 -c "import gradio; print('Gradio OK:', gradio.__version__)"
python3 -c "import ollama; print('Ollama OK')"
python3 -c "from backend.utils.config import settings; print('Config OK')"
```

### 7. Iniciar aplicación
```bash
./start_ki.sh
```

---

## 🔍 Diagnóstico de Errores

### Error: "Permission denied"
```bash
# Dar permisos de ejecución
chmod +x /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki/*.sh

# Luego ejecutar
./start_ki.sh
```

### Error: "./ki/START_KI.bat: command not found"
**Problema:** Estás intentando ejecutar un script de Windows en Linux

**Solución:** Usa el script `.sh` en su lugar
```bash
# ❌ NO hagas esto en Linux:
./START_KI.bat

# ✅ Haz esto:
./start_ki.sh
```

### Error: "ModuleNotFoundError: No module named 'gradio'"
```bash
# Activar venv primero
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect
source venv/bin/activate

# Instalar gradio
pip install gradio

# O ejecutar instalador completo
cd ki
./install.sh
```

### Error: "Virtual environment not found"
```bash
# Verificar si existe
ls -la /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/venv

# Si no existe, crear
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect
python3 -m venv venv

# Activar
source venv/bin/activate

# Instalar dependencias
cd ki
./install.sh
```

### Error: Ollama connection failed
**No es crítico** - La UI funcionará sin Ollama.

**Para instalar Ollama en Linux:**
```bash
# Opción 1: Script oficial
curl -fsSL https://ollama.ai/install.sh | sh

# Opción 2: Manual desde https://ollama.ai/download
```

**Para iniciar Ollama:**
```bash
# Terminal 1: Iniciar servidor
ollama serve

# Terminal 2: Descargar modelo
ollama pull llama3.1

# Terminal 3: Iniciar KI
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki
./start_ki.sh
```

---

## 🎯 Flujo Completo de Instalación

```bash
# 1. Ir al proyecto
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki

# 2. Verificar setup
./check_setup.sh

# 3. Instalar dependencias
./install.sh

# 4. (Opcional) Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
ollama pull llama3.1

# 5. Iniciar KI Platform
./start_ki.sh

# 6. Abrir navegador en: http://localhost:7860
```

---

## 💡 Diferencias Windows vs Linux

| Tarea | Windows | Linux/WSL |
|-------|---------|-----------|
| Ejecutar diagnóstico | `CHECK_SETUP.bat` | `./check_setup.sh` |
| Instalar dependencias | `INSTALL.bat` | `./install.sh` |
| Iniciar aplicación | `START_KI.bat` | `./start_ki.sh` |
| Activar venv | `venv\Scripts\activate.bat` | `source venv/bin/activate` |
| Python command | `python` | `python3` |

---

## 🔧 Comandos Útiles (Linux)

### Gestión de venv:
```bash
# Activar venv
source /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/venv/bin/activate

# Desactivar venv
deactivate

# Ver paquetes instalados
pip list

# Buscar paquete específico
pip list | grep gradio
```

### Verificar instalación:
```bash
# Python version
python3 --version

# Módulos instalados
python3 -c "import gradio; print(gradio.__version__)"
python3 -c "import ollama; print('OK')"
python3 -c "from backend.utils.config import settings; print(settings.storage_path)"
```

### Ollama:
```bash
# Verificar si está instalado
which ollama

# Ver modelos instalados
ollama list

# Iniciar servidor
ollama serve

# Pull modelo
ollama pull llama3.1

# Test rápido
ollama run llama3.1 "Hello"
```

### Debugging:
```bash
# Ver logs de la app
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki
source ../venv/bin/activate
python3 frontend/app.py 2>&1 | tee app.log

# Ver errores de import
python3 -c "from backend.utils.config import settings" 2>&1

# Verificar permisos
ls -la *.sh
```

---

## 📁 Estructura de Directorios

```
/mnt/c/Users/Gohanckz/Desktop/IA-Proyect/
├── venv/                          ← Virtual environment
│   └── bin/
│       └── activate              ← Activar con: source venv/bin/activate
│
└── ki/                            ← Proyecto KI
    ├── start_ki.sh               ← Launcher principal (USAR)
    ├── install.sh                 ← Instalador automático
    ├── check_setup.sh             ← Diagnóstico
    ├── KI.sh                      ← Launcher simple
    │
    ├── START_KI.bat              ← Para Windows (NO usar en Linux)
    ├── INSTALL.bat                ← Para Windows (NO usar en Linux)
    ├── CHECK_SETUP.bat            ← Para Windows (NO usar en Linux)
    │
    ├── frontend/
    │   └── app.py
    ├── backend/
    └── storage/
```

---

## ✅ Checklist de Instalación Exitosa

- [ ] Scripts `.sh` tienen permisos de ejecución (`chmod +x *.sh`)
- [ ] Python 3 detectado (`python3 --version`)
- [ ] Venv existe en `/mnt/c/Users/Gohanckz/Desktop/IA-Proyect/venv`
- [ ] Venv activado correctamente (`source venv/bin/activate`)
- [ ] `import gradio` funciona
- [ ] `import ollama` funciona
- [ ] `from backend.utils.config import settings` funciona
- [ ] `./start_ki.sh` abre la UI en el navegador
- [ ] http://localhost:7860 muestra 4 tabs

---

## 🆘 Si Nada Funciona

### Opción 1: Instalación limpia
```bash
# 1. Borrar venv actual
rm -rf /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/venv

# 2. Crear nuevo venv
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect
python3 -m venv venv

# 3. Activar
source venv/bin/activate

# 4. Instalar todo
cd ki
pip install pydantic-settings python-dotenv rich gradio ollama PyPDF2 python-docx beautifulsoup4 markdown

# 5. Iniciar
./start_ki.sh
```

### Opción 2: Ejecución manual
```bash
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect
source venv/bin/activate
cd ki
python3 frontend/app.py
```

---

## 🔄 WSL vs Windows Native

Si estás en WSL pero quieres usar Windows native:

1. Abre **PowerShell** o **CMD** (Windows, no WSL)
2. Navega a: `C:\Users\Gohanckz\Desktop\IA-Proyect\ki`
3. Ejecuta: `START_KI.bat`

O si estás en WSL y quieres continuar en WSL:

1. Usa los scripts `.sh`
2. Ejecuta: `./start_ki.sh`

---

## 💡 Tips

1. **Siempre usa `./start_ki.sh`** en Linux/WSL
2. **NO intentes ejecutar `.bat` en Linux** - no funcionará
3. **`python3` no `python`** en Linux
4. **`source` no `call`** para activar venv
5. **Dar permisos con `chmod +x`** si sale "Permission denied"

---

**Última actualización:** 2025-10-02
**Versión:** v0.1.0
**Plataforma:** Linux/WSL

**Siguiente paso:** Ejecuta `./check_setup.sh` y comparte el resultado
