# 🚀 KI Platform - Guía de Instalación

## 📋 Diagnóstico Actual

Según el diagnóstico, tienes:
- ✅ Python 3.11.4 instalado
- ✅ Estructura del proyecto OK
- ❌ Dependencias faltantes (gradio, ollama, etc.)
- ❌ Ollama no instalado

---

## ⚡ Solución Rápida (3 pasos)

### Paso 1: Instalar Dependencias
```bash
cd C:\Users\Gohanckz\Desktop\IA-Proyect\ki
INSTALL.bat
```

Esto instalará automáticamente:
- ✅ Gradio (UI framework)
- ✅ Ollama client (para LLM)
- ✅ Document parsers (PDF, DOCX, etc.)
- ✅ Todas las dependencias necesarias

### Paso 2: Instalar Ollama (Opcional pero recomendado)
1. Descargar: https://ollama.ai/download
2. Ejecutar instalador
3. Abrir nueva terminal y ejecutar:
   ```bash
   ollama serve
   ```
4. En otra terminal:
   ```bash
   ollama pull llama3.1
   ```

### Paso 3: Iniciar KI Platform
```bash
cd C:\Users\Gohanckz\Desktop\IA-Proyect\ki
START_KI.bat
```

---

## 🔧 Instalación Manual (si INSTALL.bat falla)

### 1. Activar venv y actualizar pip
```bash
cd C:\Users\Gohanckz\Desktop\IA-Proyect
venv\Scripts\activate.bat
python -m pip install --upgrade pip
```

### 2. Instalar dependencias base
```bash
pip install pydantic-settings python-dotenv rich
```

### 3. Instalar Gradio y Ollama
```bash
pip install gradio ollama
```

### 4. Instalar parsers
```bash
pip install PyPDF2 python-docx beautifulsoup4 markdown
```

### 5. Verificar instalación
```bash
cd ki
python -c "import gradio; print('Gradio OK')"
python -c "import ollama; print('Ollama OK')"
python -c "from backend.utils.config import settings; print('Config OK')"
```

### 6. Iniciar aplicación
```bash
START_KI.bat
```

---

## 📊 Comandos de Diagnóstico

### Verificar todo el setup:
```bash
cd C:\Users\Gohanckz\Desktop\IA-Proyect\ki
CHECK_SETUP.bat
```

### Verificar solo Python packages:
```bash
cd C:\Users\Gohanckz\Desktop\IA-Proyect
venv\Scripts\activate.bat
pip list | findstr gradio
pip list | findstr ollama
pip list | findstr pydantic
```

### Verificar Ollama:
```bash
# Ver si está en PATH
where ollama

# Ver si el servicio está corriendo
curl http://localhost:11434/api/version

# Iniciar manualmente
ollama serve
```

---

## ❌ Solución de Errores

### Error: "ModuleNotFoundError: No module named 'gradio'"
**Solución:**
```bash
cd C:\Users\Gohanckz\Desktop\IA-Proyect
venv\Scripts\activate.bat
pip install gradio
```

### Error: "ModuleNotFoundError: No module named 'pydantic_settings'"
**Solución:**
```bash
cd C:\Users\Gohanckz\Desktop\IA-Proyect
venv\Scripts\activate.bat
pip install pydantic-settings
```

### Error: "Virtual environment not found"
**Causa:** El venv existe pero el script no lo encuentra

**Solución:** Verificar manualmente
```bash
# Verificar que existe
dir C:\Users\Gohanckz\Desktop\IA-Proyect\venv\Scripts\activate.bat

# Si existe, activar manualmente
cd C:\Users\Gohanckz\Desktop\IA-Proyect
venv\Scripts\activate.bat

# Luego ejecutar la app
cd ki
python frontend\app.py
```

### Error: Ollama connection failed
**No es crítico** - La UI funcionará sin Ollama, solo la generación de datasets no estará disponible.

**Solución (opcional):**
1. Descargar Ollama: https://ollama.ai/download
2. Instalar
3. Abrir terminal: `ollama serve`
4. Descargar modelo: `ollama pull llama3.1`

---

## 🎯 Flujo Recomendado

```bash
# 1. Ir a la carpeta del proyecto
cd C:\Users\Gohanckz\Desktop\IA-Proyect\ki

# 2. Ejecutar instalación automática
INSTALL.bat

# 3. Esperar a que termine (puede tomar 2-5 minutos)

# 4. Iniciar KI Platform
START_KI.bat

# 5. La UI se abrirá en http://localhost:7860
```

---

## 📁 Archivos Útiles

| Archivo | Propósito |
|---------|-----------|
| `INSTALL.bat` | Instala todas las dependencias automáticamente |
| `START_KI.bat` | Inicia la aplicación con verificaciones |
| `CHECK_SETUP.bat` | Diagnóstico completo del setup |
| `KI.bat` | Launcher simple (menos robusto) |

---

## 🔍 Qué Hace Cada Script

### INSTALL.bat
1. Verifica Python
2. Activa venv (o lo crea si no existe)
3. Instala todas las dependencias
4. Verifica instalación

### START_KI.bat
1. Verifica Python
2. Activa venv
3. Verifica/instala dependencias si faltan
4. Verifica Ollama (opcional)
5. Lanza la UI en localhost:7860

### CHECK_SETUP.bat
1. Verifica Python
2. Verifica venv
3. Verifica packages instalados
4. Verifica Ollama
5. Verifica estructura del proyecto
6. Muestra resumen y soluciones

---

## 💡 Consejos

1. **Usa INSTALL.bat primero** - Automatiza todo el setup
2. **Ollama es opcional** - La UI funciona sin él
3. **Ejecuta CHECK_SETUP.bat** si algo falla
4. **Los errores de encoding** ya están solucionados en START_KI.bat

---

## 🆘 Si Nada Funciona

### Opción 1: Instalación limpia
```bash
# 1. Borrar venv actual
rmdir /s /q C:\Users\Gohanckz\Desktop\IA-Proyect\venv

# 2. Crear nuevo venv
cd C:\Users\Gohanckz\Desktop\IA-Proyect
python -m venv venv

# 3. Activar y actualizar pip
venv\Scripts\activate.bat
python -m pip install --upgrade pip

# 4. Instalar todo
cd ki
pip install -r requirements.txt
pip install gradio ollama beautifulsoup4 markdown pydantic-settings

# 5. Iniciar
START_KI.bat
```

### Opción 2: Ejecución manual completa
```bash
cd C:\Users\Gohanckz\Desktop\IA-Proyect
venv\Scripts\activate.bat
cd ki
python frontend\app.py
```

---

## ✅ Checklist de Instalación Exitosa

- [ ] Python 3.11.4 detectado
- [ ] Venv activado correctamente
- [ ] `import gradio` funciona
- [ ] `import ollama` funciona
- [ ] `from backend.utils.config import settings` funciona
- [ ] START_KI.bat abre la UI en el navegador
- [ ] http://localhost:7860 muestra 4 tabs

---

**Última actualización:** 2025-10-02
**Versión:** v0.1.0

**Siguiente paso:** Ejecuta `INSTALL.bat` y comparte el resultado
