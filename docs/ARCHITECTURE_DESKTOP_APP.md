# 🖥️ KI - Arquitectura Aplicación de Escritorio

## 🎯 Cambio Importante: De Web a Desktop

### Decisión Arquitectónica
**KI será una aplicación de escritorio nativa** que corre 100% local, con:
- ✅ Interfaz gráfica moderna
- ✅ Drag & drop de documentos
- ✅ Visualización en tiempo real
- ✅ Sin servidor web externo
- ✅ Ejecutable standalone

---

# 📊 Comparación de Tecnologías UI

## Opción 1: **Gradio con Interface Blocks** ⭐ RECOMENDADO

### Ventajas:
- ✅ **Interfaz nativa de navegador (localhost)**
- ✅ Drag & drop built-in
- ✅ Progress bars en tiempo real
- ✅ File upload visual
- ✅ Actualización automática UI
- ✅ Gráficas integradas (Plotly)
- ✅ **Zero setup** - Solo Python
- ✅ Se ejecuta local (no internet)
- ✅ Portable como .bat/.sh

### Desventajas:
- ⚠️ Requiere navegador (pero es local)
- ⚠️ No es "aplicación nativa" tradicional

### Código ejemplo:
```python
import gradio as gr

with gr.Blocks() as app:
    with gr.Tab("Dataset Manager"):
        files = gr.File(
            file_count="multiple",
            file_types=[".pdf", ".docx", ".md"],
            label="Drag & Drop Documents"
        )
        progress = gr.Progress()
        generate_btn = gr.Button("Generate Dataset")

app.launch(
    server_name="127.0.0.1",  # Solo local
    server_port=7860,
    share=False,              # No compartir online
    inbrowser=True            # Abre navegador automáticamente
)
```

---

## Opción 2: **PyQt6 / PySide6**

### Ventajas:
- ✅ Aplicación 100% nativa
- ✅ Se compila a .exe
- ✅ No requiere navegador
- ✅ Control total del UI

### Desventajas:
- ❌ Desarrollo MÁS LENTO (4-6 semanas vs 1-2)
- ❌ Requiere aprender Qt
- ❌ Más complejo para gráficas
- ❌ Deployment más pesado

---

## Opción 3: **Electron + Python (Eel/PyWebView)**

### Ventajas:
- ✅ UI moderna (HTML/CSS/JS)
- ✅ Aplicación standalone
- ✅ Empaquetable

### Desventajas:
- ❌ Requiere Node.js
- ❌ Más complejo (2 stacks)
- ❌ Pesado (Electron ~100MB+)
- ❌ Overhead adicional

---

# 🏆 DECISIÓN FINAL: Gradio + Script Launcher

## Arquitectura Híbrida Óptima

```
┌─────────────────────────────────────────────────────┐
│  KI.bat / KI.sh (Double-click para iniciar)         │
│  ↓                                                   │
│  Inicia Python + Gradio                             │
│  ↓                                                   │
│  Abre navegador en http://localhost:7860            │
│  ↓                                                   │
│  Interfaz Gradio Blocks (Drag & Drop, etc.)         │
│  ↓                                                   │
│  Backend Python (Ollama, Training, etc.)            │
│  ↓                                                   │
│  Todo corre LOCAL (sin internet)                    │
└─────────────────────────────────────────────────────┘
```

### Por qué es la mejor opción:
1. ✅ **User Experience:** Doble-click → listo (como app de escritorio)
2. ✅ **Development Speed:** 1-2 semanas vs 4-6 con PyQt
3. ✅ **Modern UI:** Drag & drop, progress bars, gráficas
4. ✅ **100% Local:** No requiere internet después de setup
5. ✅ **Portable:** Un folder, corre en cualquier PC
6. ✅ **Mantenible:** Stack Python puro

---

# 🎨 Diseño de Interfaz UI

## Layout Principal (Gradio Blocks)

```
┌──────────────────────────────────────────────────────────────┐
│  KI - AI Training Platform                          [Minimize]│
├──────────────────────────────────────────────────────────────┤
│  [📁 Dataset Manager] [🎓 Training] [🧪 Testing] [⚙️ Settings]│
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  TAB: Dataset Manager                                        │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  📄 Drag & Drop Documents Here                        │ │
│  │                                                        │ │
│  │  [Click to Browse] or Drag files                      │ │
│  │                                                        │ │
│  │  Supported: PDF, DOCX, TXT, Markdown                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Category: [SSRF ▼]  Examples per doc: [5 ▼]               │
│  Model: [llama3.1 ▼]  Quality: [High ▼]                    │
│                                                              │
│  [▶️ Generate Dataset]                                       │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  📊 Generation Progress                               │ │
│  │  [████████████░░░░░] 75% (45/60 documents)            │ │
│  │                                                        │ │
│  │  Current: processing "ssrf_kubernetes.pdf"            │ │
│  │  Generated: 387 examples | Validated: 372 ✅          │ │
│  │  Rejected: 15 ❌ (quality threshold)                   │ │
│  │                                                        │ │
│  │  [Pause] [Stop] [View Log]                            │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  📚 Generated Datasets                                │ │
│  │                                                        │ │
│  │  ☑ ssrf_dataset_final.json (388 examples)            │ │
│  │     Created: 2025-10-02 14:30                         │ │
│  │     Sources: 60 documents                             │ │
│  │     [Preview] [Edit] [Export] [Delete]                │ │
│  │                                                        │ │
│  │  ☐ xss_dataset.json (145 examples)                   │ │
│  │     Created: 2025-10-01 10:15                         │ │
│  │     [Preview] [Edit] [Export] [Delete]                │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

# 🚀 Launcher Scripts

## Windows: `KI.bat`

```batch
@echo off
title KI - AI Training Platform
color 0A

echo.
echo  ╔════════════════════════════════════════╗
echo  ║   KI - AI Training Platform v0.1.0    ║
echo  ╚════════════════════════════════════════╝
echo.
echo  [*] Starting KI Platform...
echo.

cd /d "%~dp0"

REM Activar venv
call ..\venv\Scripts\activate.bat

REM Verificar Ollama
echo  [*] Checking Ollama...
curl -s http://localhost:11434/api/version > nul 2>&1
if %errorlevel% neq 0 (
    echo  [!] Warning: Ollama not running
    echo  [*] Starting Ollama...
    start /B ollama serve
    timeout /t 3 /nobreak > nul
)

REM Iniciar aplicación
echo  [*] Launching UI...
python frontend/app.py

pause
```

## Linux/Mac: `KI.sh`

```bash
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
source ../venv/bin/activate

# Verificar Ollama
echo "[*] Checking Ollama..."
if ! curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "[!] Warning: Ollama not running"
    echo "[*] Starting Ollama..."
    ollama serve &
    sleep 3
fi

# Iniciar aplicación
echo "[*] Launching UI..."
python frontend/app.py

read -p "Press any key to exit..."
```

---

# 🎨 Características UI Visuales

## 1. Drag & Drop Visual

```python
import gradio as gr

def handle_file_upload(files):
    """Maneja archivos drag & dropped"""
    file_list = []
    for file in files:
        file_list.append({
            "name": file.name,
            "size": f"{file.size / 1024:.2f} KB",
            "type": file.name.split('.')[-1].upper()
        })
    return file_list

with gr.Blocks() as app:
    gr.Markdown("# 📄 Upload Documents")

    files = gr.File(
        file_count="multiple",
        file_types=[".pdf", ".docx", ".txt", ".md"],
        label="Drag & Drop or Click to Browse",
        elem_id="file-upload"
    )

    file_display = gr.Dataframe(
        headers=["Name", "Size", "Type"],
        label="Uploaded Files"
    )

    files.change(
        fn=handle_file_upload,
        inputs=[files],
        outputs=[file_display]
    )
```

## 2. Progress Bar en Tiempo Real

```python
import gradio as gr
import time

def generate_dataset(files, category, progress=gr.Progress()):
    """Genera dataset con progreso visual"""

    total_files = len(files)
    generated_examples = []

    for i, file in enumerate(files):
        # Actualizar progreso
        progress(i / total_files, desc=f"Processing {file.name}")

        # Generar ejemplos (simulado)
        time.sleep(0.5)

        # Actualizar UI
        yield {
            "current_file": file.name,
            "progress": f"{i+1}/{total_files}",
            "examples_generated": len(generated_examples)
        }

    progress(1.0, desc="✅ Complete!")
    return "Dataset generated successfully!"

with gr.Blocks() as app:
    files = gr.File(file_count="multiple")
    category = gr.Dropdown(["SSRF", "XSS", "SQLi"])

    generate_btn = gr.Button("Generate Dataset")

    status = gr.Textbox(label="Status")

    generate_btn.click(
        fn=generate_dataset,
        inputs=[files, category],
        outputs=[status]
    )
```

## 3. Live Log Viewer

```python
import gradio as gr

def generate_with_logs():
    """Genera con logs en tiempo real"""

    logs = []

    logs.append("[INFO] Starting generation...")
    yield "\n".join(logs)

    logs.append("[INFO] Parsing document 1/10")
    yield "\n".join(logs)

    logs.append("[SUCCESS] Generated 5 examples")
    yield "\n".join(logs)

    logs.append("[WARNING] 1 example rejected (quality)")
    yield "\n".join(logs)

    logs.append("[INFO] Complete! 45 examples generated")
    yield "\n".join(logs)

with gr.Blocks() as app:
    generate_btn = gr.Button("Generate")

    log_output = gr.Textbox(
        label="Live Logs",
        lines=15,
        max_lines=30,
        interactive=False
    )

    generate_btn.click(
        fn=generate_with_logs,
        outputs=[log_output]
    )
```

---

# 🔄 Flujo de Usuario Completo

## Paso 1: Usuario inicia KI
```
1. Doble-click en KI.bat (Windows) o KI.sh (Linux)
2. Terminal muestra logo ASCII
3. Verifica Ollama (inicia si está apagado)
4. Abre navegador en localhost:7860
5. UI de Gradio se muestra
```

## Paso 2: Cargar Documentos
```
1. Usuario arrastra 50 PDFs a zona de drop
2. UI muestra lista de archivos con preview
3. Usuario selecciona categoría: "SSRF"
4. Usuario configura: 5 examples/doc, quality: High
5. Click "Generate Dataset"
```

## Paso 3: Generación con Visualización
```
1. Progress bar aparece: [████░░░░] 25%
2. Logs en tiempo real:
   [INFO] Parsing ssrf_aws.pdf...
   [SUCCESS] Generated 5 examples
   [INFO] Validating quality...
   [SUCCESS] 5/5 passed quality check

3. Estadísticas actualizadas en vivo:
   Documents: 12/50
   Examples: 58 generated, 55 validated

4. Usuario puede pausar/detener en cualquier momento
```

## Paso 4: Revisar y Exportar
```
1. Dataset completo: 245 ejemplos
2. Preview de ejemplos en UI
3. Editar ejemplos individuales
4. Merge con dataset existente
5. Export a JSON
```

## Paso 5: Entrenar (Tab Training)
```
1. Usuario cambia a tab "Training"
2. Selecciona dataset generado
3. Configura hyperparams (preset RTX 4060 Ti)
4. Click "Start Training"
5. Progress bar + loss graph en tiempo real
6. GPU monitoring visual
7. Notificación cuando termina
```

---

# 📂 Estructura Actualizada

```
ki/
├── KI.bat                    ✅ [NUEVO] Launcher Windows
├── KI.sh                     ✅ [NUEVO] Launcher Linux/Mac
├── frontend/
│   ├── app.py               🔄 [ACTUALIZAR] Gradio Blocks
│   ├── components/
│   │   ├── dataset_manager.py    🔄 Con drag & drop
│   │   ├── training_studio.py    🔄 Con progress visual
│   │   ├── testing_lab.py        🔄 Interactive UI
│   │   └── monitoring.py         🔄 Real-time graphs
│   └── assets/
│       ├── logo.png
│       └── styles.css
│
├── backend/ (sin cambios)
└── ...
```

---

# 🎯 Ventajas de Esta Arquitectura

## Para el Usuario:
✅ **Experiencia de escritorio** - Doble-click e inicia
✅ **Visual e intuitivo** - Drag & drop, progress bars
✅ **Todo local** - Sin internet, sin servidor externo
✅ **Portable** - Copias la carpeta y funciona
✅ **Rápido** - No overhead de Electron

## Para Desarrollo:
✅ **Python puro** - Un solo stack
✅ **Rápido de implementar** - Gradio Blocks
✅ **Fácil de mantener** - Código simple
✅ **Extensible** - Añadir tabs fácilmente

## Técnicas:
✅ **Real-time updates** - Progress, logs, gráficas
✅ **Responsive UI** - Ajusta a ventana
✅ **Multi-threading** - No bloquea UI
✅ **Error handling** - Mensajes claros

---

# 🚀 Timeline Actualizado

## Sesión 3 (4-5 horas):
- ✅ Crear launchers (KI.bat, KI.sh)
- ✅ Implementar Gradio Blocks base
- ✅ Tab Dataset Manager con drag & drop
- ✅ Progress bars y logs en tiempo real

## Sesión 4 (4-5 horas):
- ✅ Integrar Ollama client
- ✅ Dataset generator con visualización
- ✅ Quality validator
- ✅ Export/merge datasets

## Sesión 5 (5-6 horas):
- ✅ Tab Training Studio
- ✅ Training con progress visual
- ✅ GPU monitoring
- ✅ Checkpoint management

## Sesión 6 (3-4 horas):
- ✅ Tab Testing Lab
- ✅ Tab Settings
- ✅ Polish UI
- ✅ Testing final

**Total:** 16-20 horas → **2-3 semanas**

---

# 💡 Decisión Final

## ✅ ARQUITECTURA APROBADA:

**Gradio Blocks + Python Backend + Launcher Scripts**

Esto nos da:
1. ✅ Aplicación de escritorio (doble-click)
2. ✅ UI moderna con drag & drop
3. ✅ Visualización en tiempo real
4. ✅ 100% local
5. ✅ Desarrollo rápido (2-3 semanas)
6. ✅ Mantenible y extensible

---

**¿Procedemos con esta arquitectura?** 🚀

Si apruebas, en la siguiente sesión creo:
1. Launchers (KI.bat, KI.sh)
2. Frontend Gradio con drag & drop
3. Visualización de progreso en tiempo real
4. Tab Dataset Manager funcional
