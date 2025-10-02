# 🚀 KI Platform - Inicio Rápido

## ✅ Estado: TODO LISTO

Tu instalación está completa:
- ✅ Python 3.13.2
- ✅ Virtual environment activado
- ✅ Gradio instalado
- ✅ Ollama client instalado
- ✅ pydantic-settings instalado
- ✅ Document parsers instalados
- ✅ App funcionando

---

## 🎯 Cómo Iniciar KI Platform

### Opción 1: Script Simple (Recomendado)
```bash
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki
./run.sh
```

### Opción 2: Manual
```bash
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect
source venv/bin/activate
cd ki
python3 frontend/app.py
```

### Opción 3: Verificar primero
```bash
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki
./quick_check.sh   # Ver estado
./run.sh           # Iniciar app
```

---

## 🌐 Acceder a la Interfaz

Una vez iniciado, abre tu navegador en:

**http://localhost:7860**

Verás 4 tabs:
- 📁 **Dataset Manager** - Drag & drop documentos, genera datasets
- 🎓 **Training Studio** - Entrena modelos (próximamente)
- 🧪 **Testing Lab** - Prueba modelos (próximamente)
- ⚙️ **Settings** - Configuración

---

## ⚙️ Ollama (Opcional)

**Dataset generation requiere Ollama**, pero la UI funciona sin él.

### Para instalar Ollama en WSL/Linux:
```bash
# Instalar
curl -fsSL https://ollama.ai/install.sh | sh

# Iniciar servidor (en otra terminal)
ollama serve

# Descargar modelo
ollama pull llama3.1
```

### Verificar Ollama:
```bash
curl http://localhost:11434/api/version
```

---

## 🔧 Scripts Disponibles

| Script | Descripción | Uso |
|--------|-------------|-----|
| `run.sh` | Inicia la app (simple) | `./run.sh` |
| `quick_check.sh` | Diagnóstico rápido | `./quick_check.sh` |
| `install.sh` | Instalador completo | `./install.sh` |
| `start_ki.sh` | Launcher con checks | `./start_ki.sh` |

---

## 📊 Verificación Final

```bash
# Ver estado completo
./quick_check.sh

# Debería mostrar:
# ✓ Python: OK
# ✓ Virtual Environment: Found
# ✓ gradio: OK
# ✓ ollama: OK
# ✓ pydantic-settings: OK
```

---

## 🎯 Siguiente Paso

**Ejecuta esto para iniciar:**
```bash
./run.sh
```

Luego abre: **http://localhost:7860** en tu navegador

---

## 📝 Uso del Dataset Manager

1. Ve a tab "Dataset Manager"
2. Arrastra PDFs/DOCX a la zona de drop
3. Click "Parse Documents"
4. Configura categoría (SSRF, XSS, etc.)
5. Click "Generate Dataset"
6. Click "Save Dataset"

*Nota: Generate Dataset está simulado por ahora (se integrará Ollama en próxima sesión)*

---

## 🆘 Problemas Comunes

### Error: "Permission denied"
```bash
chmod +x *.sh
./run.sh
```

### Error: "ModuleNotFoundError"
```bash
source ../venv/bin/activate
pip install [package-name]
```

### Reinstalar todo:
```bash
./install.sh
```

---

**Versión:** v0.1.0
**Última actualización:** 2025-10-02
**Status:** ✅ Ready to use
