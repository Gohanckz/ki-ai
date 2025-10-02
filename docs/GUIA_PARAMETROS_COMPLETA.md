# 📖 KI Platform - Guía Completa de Parámetros

## Índice

1. [Tab 1: Dataset Manager](#tab-1-dataset-manager)
2. [Tab 2: Dataset Review](#tab-2-dataset-review)
3. [Tab 3: Training Manager](#tab-3-training-manager)
4. [Tab 4: Testing System](#tab-4-testing-system)
5. [Tab 5: Settings](#tab-5-settings)
6. [CLI Tool: dataset_cli.py](#cli-tool-dataset_clipy)
7. [Archivos de Configuración](#archivos-de-configuración)

---

# Tab 1: Dataset Manager

## 📤 Upload Documents

### **File Upload**
- **Tipo:** File uploader (drag & drop)
- **Formatos soportados:**
  - `.pdf` - Documentos PDF
  - `.docx` - Microsoft Word
  - `.txt` / `.text` - Texto plano
  - `.md` / `.markdown` - Markdown
  - `.log` - Archivos log
- **Múltiples archivos:** Sí
- **Límite de tamaño:** Sin límite específico (depende de memoria)
- **Uso:** Arrastra archivos o haz click para seleccionar

**Ejemplo:**
```
Upload 10 PDFs sobre SSRF vulnerability reports
→ Archivos se muestran en tabla con:
  - Name: nombre del archivo
  - Size: tamaño en KB
  - Type: PDF/DOCX/TXT
  - Status: ✅ Supported / ❌ Unsupported
```

---

## ⚙️ Dataset Configuration

### **Vulnerability Category**
- **Tipo:** Dropdown
- **Valores:**
  - `SSRF` - Server-Side Request Forgery
  - `XSS` - Cross-Site Scripting
  - `SQLi` - SQL Injection
  - `IDOR` - Insecure Direct Object Reference
  - `RCE` - Remote Code Execution
  - `XXE` - XML External Entity
  - `CSRF` - Cross-Site Request Forgery
  - `LFI/RFI` - Local/Remote File Inclusion
  - `Authentication Bypass` - Bypass de autenticación
  - `Custom` - Categoría personalizada
- **Default:** `SSRF`
- **Uso:** Selecciona el tipo de vulnerabilidad de tus documentos

**Qué hace:**
- Define la categoría de los ejemplos generados
- Influye en los prompts usados para generación con Ollama
- Organiza los datasets por tipo de vulnerabilidad

**Ejemplo:**
```
Category: SSRF
→ Ollama genera ejemplos específicos de SSRF
→ Dataset guardado con metadata: {"category": "SSRF"}
```

---

### **Examples per Document**
- **Tipo:** Slider
- **Rango:** 1 - 20
- **Default:** 5
- **Paso:** 1
- **Uso:** Número de ejemplos de entrenamiento a generar por cada documento

**Qué hace:**
- Controla cuántos ejemplos se extraen de cada documento
- Más ejemplos = dataset más grande, pero puede tener redundancia
- Menos ejemplos = dataset más pequeño, pero más conciso

**Recomendaciones:**
- **Documentos cortos (< 1000 palabras):** 3-5 ejemplos
- **Documentos medianos (1000-3000 palabras):** 5-10 ejemplos
- **Documentos largos (> 3000 palabras):** 10-15 ejemplos

**Ejemplo:**
```
10 documentos × 5 ejemplos/doc = 50 ejemplos totales
→ Si subes 10 PDFs y configuras 5 ejemplos
→ Resultado: dataset con ~50 ejemplos
```

---

### **Quality Threshold**
- **Tipo:** Dropdown
- **Valores:**
  - `High` - Alta calidad (score mínimo: 0.7)
  - `Medium` - Calidad media (score mínimo: 0.5)
  - `Low` - Baja calidad (score mínimo: 0.3)
- **Default:** `High`
- **Uso:** Define el umbral mínimo de calidad aceptable

**Qué hace:**
- Filtra automáticamente ejemplos de baja calidad
- Ejemplos con score inferior al threshold son rechazados
- Afecta la tasa de rechazo durante generación

**Cálculo de Quality Score:**
```python
score = 0.0

# Required fields (30%)
if tiene instruction + input + output:
    score += 0.3

# Output length (30%)
if output > 200 caracteres:
    score += 0.3
elif output > 100 caracteres:
    score += 0.15

# Instruction clarity (20%)
if 20 < len(instruction) < 200:
    score += 0.2

# Input context (20%)
if len(input) > 20:
    score += 0.2

total_score = min(score, 1.0)
```

**Ejemplo:**
```
Quality: High (threshold 0.7)
→ Genera 50 ejemplos
→ 45 tienen score >= 0.7 (validados)
→ 5 tienen score < 0.7 (rechazados)
→ Dataset final: 45 ejemplos
→ Tasa de rechazo: 10%
```

---

### **Dataset Name**
- **Tipo:** Text input
- **Default:** `my_dataset`
- **Caracteres permitidos:** Alfanuméricos, guiones, guiones bajos, espacios
- **Uso:** Nombre para guardar el dataset

**Qué hace:**
- Define el nombre del archivo JSON
- Sanitiza caracteres especiales automáticamente
- Agrega extensión `.json` automáticamente

**Convenciones recomendadas:**
```
ssrf_v1             → Primera versión de dataset SSRF
ssrf_raw_v1         → Dataset sin revisar
ssrf_reviewed_v1    → Dataset revisado manualmente
ssrf_final          → Dataset final listo para entrenar
xss_writeups        → XSS desde writeups
sqli_merged         → SQLi mergeado de varias fuentes
```

**Ejemplo:**
```
Dataset Name: ssrf_hackerone_v1
→ Guarda en: storage/datasets/ssrf_hackerone_v1.json
```

---

## 🎯 Action Buttons

### **📄 Parse Documents**
- **Acción:** Parsea los documentos subidos
- **Requiere:** Archivos subidos
- **Proceso:**
  1. Lee cada archivo soportado
  2. Extrae texto completo
  3. Cuenta palabras
  4. Muestra resultados en tabla

**Output:**
```
Parsing Results:
┌─────────────────┬──────┬────────┬───────────┐
│ File            │ Type │ Words  │ Status    │
├─────────────────┼──────┼────────┼───────────┤
│ ssrf_report.pdf │ PDF  │ 2,345  │ ✅ Success│
│ xxe_guide.docx  │ DOCX │ 1,890  │ ✅ Success│
└─────────────────┴──────┴────────┴───────────┘

Status: ✅ Parsed 2 documents (4,235 total words)
```

---

### **🎯 Generate Dataset**
- **Acción:** Genera ejemplos de entrenamiento usando Ollama
- **Requiere:** Documentos parseados
- **Proceso:**
  1. Verifica si Ollama está disponible
  2. Por cada documento:
     - Crea prompt con contexto del documento
     - Llama a Ollama (Llama 3.1)
     - Genera N ejemplos
     - Valida calidad de cada ejemplo
     - Rechaza ejemplos con score bajo
  3. Compila estadísticas
  4. Retorna dataset completo

**Generation Log (ejemplo):**
```
[INFO] Starting dataset generation with Ollama
[INFO] Category: SSRF
[INFO] Target: 5 examples per document
[INFO] Quality level: High
[INFO] Total documents: 10

[✓] Ollama is running - using real AI generation

[SUCCESS] Dataset generation complete!

📊 Statistics:
  • Documents processed: 10
  • Examples generated: 50
  • Examples validated: 45
  • Examples rejected: 5

[INFO] Quality rejection rate: 10.0%
```

**Si Ollama NO está disponible:**
```
[!] Ollama not available - using simulated generation
[!] Install Ollama and run 'ollama serve' for real generation
```

---

### **💾 Save Dataset**
- **Acción:** Guarda el dataset generado
- **Requiere:** Dataset generado
- **Formato:** JSON
- **Ubicación:** `storage/datasets/`

**Estructura del archivo JSON:**
```json
{
  "metadata": {
    "name": "ssrf_v1",
    "created_at": "2025-10-02T19:30:00",
    "category": "SSRF",
    "total_examples": 45,
    "quality_level": "High",
    "stats": {
      "total_documents": 10,
      "total_generated": 50,
      "total_validated": 45,
      "total_rejected": 5
    }
  },
  "examples": [
    {
      "instruction": "Explica cómo detectar SSRF en APIs",
      "input": "Tengo una API que permite URLs en parámetros",
      "output": "Para detectar SSRF en APIs...",
      "category": "SSRF",
      "quality_score": 0.85,
      "source_document": "ssrf_report.pdf"
    }
    // ... más ejemplos
  ]
}
```

---

# Tab 2: Dataset Review

## 📂 Load Dataset

### **Select Dataset**
- **Tipo:** Dropdown
- **Valores:** Todos los datasets en `storage/datasets/*.json`
- **Actualización:** Click en "🔄 Refresh List"
- **Uso:** Selecciona dataset a revisar

**Ejemplo:**
```
Datasets disponibles:
- ssrf_v1.json
- ssrf_raw_v2.json
- xss_writeups.json
- sqli_merged.json
```

---

### **📂 Load Dataset Button**
- **Acción:** Carga el dataset seleccionado
- **Proceso:**
  1. Lee archivo JSON
  2. Valida estructura
  3. Carga primer ejemplo
  4. Actualiza contador (1/50)

**Output:**
```
Status: Example 1/50 | Category: SSRF | Quality: 0.85 | Status: ✅ Good
```

---

## 🔍 Navigate Examples

### **⬅️ Previous / ➡️ Next**
- **Tipo:** Botones
- **Acción:** Navega al ejemplo anterior/siguiente
- **Límites:** Se detiene en primer/último ejemplo

---

### **Position Indicator**
- **Tipo:** Text (read-only)
- **Formato:** `N/TOTAL` (ej: `5/50`)
- **Muestra:** Posición actual en el dataset

---

### **Jump to Example Slider**
- **Tipo:** Slider
- **Rango:** 0 - (total_examples - 1)
- **Uso:** Salta directamente a cualquier ejemplo
- **Actualización:** Al mover slider, carga ese ejemplo

---

## ✏️ Edit Example

### **Instruction**
- **Tipo:** Text area (3 líneas)
- **Contenido:** La tarea o pregunta del ejemplo
- **Editable:** Sí
- **Uso:** Modifica la instrucción si está mal redactada

**Ejemplo:**
```
Antes: "dime como hacer ssrf"
Después: "Explica cómo identificar vulnerabilidades SSRF en AWS Lambda"
```

---

### **Input**
- **Tipo:** Text area (4 líneas)
- **Contenido:** Contexto de entrada para la tarea
- **Editable:** Sí
- **Uso:** Modifica el contexto de entrada

**Ejemplo:**
```
Antes: "tengo una función lambda"
Después: "Tengo una función AWS Lambda que hace peticiones HTTP a URLs proporcionadas por usuarios"
```

---

### **Output**
- **Tipo:** Text area (8 líneas)
- **Contenido:** Respuesta esperada del modelo
- **Editable:** Sí
- **Uso:** Corrige o mejora la respuesta esperada

**Ejemplo:**
```
Antes: "SSRF es malo"
Después: "SSRF (Server-Side Request Forgery) permite a un atacante...
[explicación técnica detallada de 200+ palabras]"
```

---

### **Quality Score**
- **Tipo:** Slider
- **Rango:** 0.0 - 1.0
- **Paso:** 0.01
- **Default:** Score automático
- **Uso:** Ajusta manualmente el score de calidad

**Cuándo ajustar:**
- Mejoraste mucho el output → sube a 0.9-1.0
- Output sigue mediocre → baja a 0.4-0.6
- Output es excelente → 1.0

---

## 🎯 Action Buttons (Review)

### **💾 Save Changes**
- **Acción:** Guarda ediciones al ejemplo actual
- **Marca:** `edited: true` en metadata del ejemplo
- **No guarda:** Archivo (solo en memoria hasta "Save Dataset")

---

### **🚩 Flag as Bad**
- **Acción:** Marca ejemplo como mala calidad
- **Marca:** `flagged: true`
- **Visual:** Status cambia a "🚩 Flagged as bad"
- **Uso:** Marca para eliminar después

---

### **✅ Mark as Good**
- **Acción:** Quita flag de ejemplo
- **Marca:** `flagged: false`
- **Visual:** Status cambia a "✅ Good"

---

### **🗑️ Delete**
- **Acción:** Elimina ejemplo actual del dataset
- **Permanente:** Sí (en memoria, hasta guardar)
- **Navegación:** Salta al siguiente ejemplo automáticamente

---

### **🗑️ Remove All Flagged**
- **Acción:** Elimina TODOS los ejemplos con `flagged: true`
- **Batch operation:** Sí
- **Confirmación:** No (cuidado!)

**Ejemplo:**
```
Dataset original: 50 ejemplos
Flagged: 8 ejemplos (malos)
→ Click "Remove All Flagged"
→ Dataset nuevo: 42 ejemplos
Status: ✅ Removed 8 flagged examples (42 remaining)
```

---

### **Save As (Dataset Name)**
- **Tipo:** Text input
- **Default:** `reviewed_dataset`
- **Uso:** Nombre para guardar dataset modificado

---

### **💾 Save Dataset**
- **Acción:** Guarda dataset modificado a archivo
- **Metadata adicional:**
  ```json
  {
    "reviewed": true,
    "total_examples": 42,
    "edited_examples": 5
  }
  ```

---

# Tab 3: Training Manager

## 💻 Hardware Info

### **GPU Info Display**
- **Tipo:** Markdown (read-only)
- **Contenido:**
  - Nombre de GPU (ej: NVIDIA GeForce RTX 4060 Ti)
  - Memoria total (GB)
  - Memoria allocated (GB)
  - Memoria free (GB)
  - Recomendaciones específicas para tu GPU

**Ejemplo:**
```
✅ GPU Available: NVIDIA GeForce RTX 4060 Ti

Memory:
- Total: 8.0 GB
- Allocated: 1.5 GB
- Free: 6.5 GB

Recommendation for RTX 4060 Ti (8GB):
- Batch size: 2-4
- Gradient accumulation: 4-8
- Use QLoRA (4-bit quantization)
```

**Si NO hay GPU:**
```
❌ No GPU detected - Training will use CPU (very slow)
```

---

## ⚙️ Training Configuration

### **Training Dataset**
- **Tipo:** Dropdown
- **Valores:** Todos los datasets en `storage/datasets/`
- **Uso:** Selecciona dataset para entrenar

**Recomendación:**
- Usa datasets "final" o "reviewed"
- Mínimo 30-50 ejemplos para entrenamiento efectivo
- Idealmente 100-200+ ejemplos

---

### **Model Name**
- **Tipo:** Text input
- **Default:** `ki_agent_v1`
- **Uso:** Nombre del modelo a entrenar

**Convenciones:**
```
ssrf_agent_v1       → Primer modelo SSRF
ssrf_agent_v2       → Segunda versión (más entrenamiento)
xss_specialist      → Especialista en XSS
general_bounty_v1   → Modelo general de bug bounty
```

**Guardado en:**
```
storage/models/agents/{model_name}/
  ├── adapter_config.json
  ├── adapter_model.bin
  ├── training_config.json
  └── training_log.txt
```

---

### **Epochs**
- **Tipo:** Slider
- **Rango:** 1 - 10
- **Default:** 3
- **Paso:** 1

**Qué es:**
- Una "epoch" = pasada completa por todo el dataset
- Más epochs = más entrenamiento

**Recomendaciones:**
- **Datasets pequeños (< 50 ejemplos):** 5-7 epochs
- **Datasets medianos (50-150 ejemplos):** 3-5 epochs
- **Datasets grandes (> 150 ejemplos):** 2-3 epochs

**Riesgos:**
- **Muy pocos epochs:** Modelo no aprende bien (underfitting)
- **Demasiados epochs:** Modelo memoriza (overfitting)

**Ejemplo:**
```
Dataset: 100 ejemplos
Epochs: 3
→ Modelo verá cada ejemplo 3 veces
→ Total de pasos de entrenamiento: 300
```

---

### **Batch Size**
- **Tipo:** Slider
- **Rango:** 1 - 8
- **Default:** 2
- **Paso:** 1

**Qué es:**
- Número de ejemplos procesados juntos en cada paso
- Más grande = más rápido, pero más memoria GPU

**Recomendaciones por GPU:**
```
RTX 4060 Ti (8GB):   batch_size = 2-4
RTX 3090 (24GB):     batch_size = 8-16
RTX 4090 (24GB):     batch_size = 8-16
CPU:                 batch_size = 1
```

**Trade-offs:**
- **Batch pequeño (1-2):**
  - ✅ Menos memoria
  - ✅ Más actualizaciones de gradiente
  - ❌ Entrenamiento más lento
- **Batch grande (4-8):**
  - ✅ Entrenamiento más rápido
  - ❌ Más memoria GPU
  - ❌ Menos actualizaciones de gradiente

**Ejemplo:**
```
Batch size: 2
GPU memory: ~4 GB usados
→ Cada paso procesa 2 ejemplos simultáneos
```

---

### **Learning Rate**
- **Tipo:** Number input
- **Default:** `2e-4` (0.0002)
- **Rango típico:** 1e-5 a 5e-4

**Qué es:**
- Qué tan rápido el modelo aprende
- Valor muy sensible

**Recomendaciones:**
```
LoRA/QLoRA fine-tuning:  1e-4 a 3e-4
Full fine-tuning:        1e-5 a 5e-5
Experimentos:            5e-4 (puede ser inestable)
```

**Riesgos:**
- **Learning rate muy alto (> 5e-4):**
  - Loss diverge (se va a infinito)
  - Entrenamiento falla
- **Learning rate muy bajo (< 1e-5):**
  - Entrenamiento extremadamente lento
  - Puede no converger en epochs razonables

**Formato de notación científica:**
```
2e-4 = 0.0002
1e-4 = 0.0001
5e-5 = 0.00005
```

---

### **LoRA r**
- **Tipo:** Slider
- **Rango:** 4 - 64
- **Default:** 16
- **Paso:** 4

**Qué es:**
- Rank de las matrices LoRA
- Controla cuántos parámetros se entrenan
- Más alto = más capacidad de aprendizaje

**Recomendaciones:**
```
Tareas simples:          r = 8
Tareas estándar:         r = 16
Tareas complejas:        r = 32
Máxima capacidad:        r = 64
```

**Trade-offs:**
- **r bajo (4-8):**
  - ✅ Muy rápido
  - ✅ Poca memoria
  - ❌ Capacidad limitada
- **r alto (32-64):**
  - ✅ Mayor capacidad
  - ❌ Más lento
  - ❌ Más memoria

**Ejemplo:**
```
LoRA r = 16
→ ~1M parámetros entrenables
→ Modelo base: 8B parámetros (frozen)
→ Ratio: 0.0125% del modelo original
```

---

### **LoRA alpha**
- **Tipo:** Slider
- **Rango:** 8 - 128
- **Default:** 32
- **Paso:** 8

**Qué es:**
- Factor de escala para LoRA
- Controla qué tan fuerte es la adaptación

**Regla general:**
```
LoRA alpha = 2 × LoRA r
```

**Ejemplos:**
```
r = 8   →  alpha = 16
r = 16  →  alpha = 32
r = 32  →  alpha = 64
```

**No te preocupes demasiado:**
- Este parámetro es menos crítico
- El default (2x de r) funciona bien en la mayoría de casos

---

## 📊 Training Estimates

### **🔍 Estimate Training Time Button**
- **Acción:** Calcula tiempo estimado de entrenamiento
- **Basado en:**
  - Número de ejemplos en dataset
  - Epochs configurados
  - Batch size configurado
  - GPU disponible (o CPU)

**Output ejemplo:**
```
📊 Training Estimates:

- Dataset: ssrf_final.json
- Examples: 100
- Epochs: 3
- Batch size: 2
- Total batches: 150

⏱️ Estimated Time:
- 75.0 minutes
- 1.25 hours

Note: Actual time may vary based on GPU load and model size.
```

**Fórmulas:**
```python
batches_per_epoch = num_examples // batch_size
total_batches = batches_per_epoch * epochs

# RTX 4060 Ti estimates:
seconds_per_batch = 2.0  # GPU
# or
seconds_per_batch = 10.0  # CPU

total_seconds = total_batches * seconds_per_batch
estimated_hours = total_seconds / 3600
```

---

## 🚀 Training Controls

### **🚀 Start Training**
- **Acción:** Inicia entrenamiento
- **Requiere:**
  - Dataset seleccionado
  - Model name proporcionado
- **Proceso:**
  1. Prepara dataset (convierte a formato Alpaca)
  2. Configura LoRA
  3. Detecta GPU
  4. Inicia entrenamiento
  5. Muestra progress en tiempo real
  6. Guarda modelo al completar

**Training Output:**
```
✅ Training Completed!

Model saved to: `storage/models/agents/ssrf_agent_v1`

Configuration:
- Base model: meta-llama/Llama-3.1-8B
- Epochs: 3
- Batch size: 2
- Learning rate: 0.0002
- LoRA r: 16
- LoRA alpha: 32

GPU: NVIDIA GeForce RTX 4060 Ti

Note: This is a simulation. Install transformers + peft for real training.
```

---

### **⏹️ Stop Training**
- **Acción:** Detiene entrenamiento en progreso
- **Guardado:** Último checkpoint guardado
- **Uso:** Si necesitas detener entrenamiento urgentemente

---

## 📦 Trained Models

### **🔄 Refresh List**
- **Acción:** Actualiza lista de modelos entrenados
- **Muestra:** Todos los modelos en `storage/models/agents/`

**Output ejemplo:**
```
🤖 Trained Models

📦 ssrf_agent_v1
- Base model: meta-llama/Llama-3.1-8B
- Created: 2025-10-02T20:30:00
- Path: `storage/models/agents/ssrf_agent_v1`

📦 xss_specialist
- Base model: meta-llama/Llama-3.1-8B
- Created: 2025-10-02T21:15:00
- Path: `storage/models/agents/xss_specialist`
```

---

# Tab 4: Testing System

## 📝 Generate Test Cases

### **Category**
- **Tipo:** Dropdown
- **Valores:**
  - `SSRF`
  - `XSS`
  - `SQLi`
  - `IDOR`
  - `RCE`
  - `XXE`
  - `CSRF`
- **Default:** `SSRF`
- **Uso:** Tipo de vulnerabilidad para test cases

**Qué hace:**
- Selecciona templates predefinidos de test cases
- Genera prompts específicos para esa vulnerabilidad

---

### **Number of Test Cases**
- **Tipo:** Slider
- **Rango:** 1 - 20
- **Default:** 5
- **Paso:** 1
- **Uso:** Cuántos test cases generar

**Recomendaciones:**
- **Quick test:** 3-5 casos
- **Evaluación estándar:** 10 casos
- **Evaluación completa:** 15-20 casos

---

### **🎲 Generate Cases Button**
- **Acción:** Genera test cases para evaluación
- **Output:** Tabla con test cases generados

**Ejemplo:**
```
Test Cases:
┌──────────────┬────────────────────────────────────────┬─────────────────────────────────┐
│ ID           │ Instruction                            │ Input                           │
├──────────────┼────────────────────────────────────────┼─────────────────────────────────┤
│ test_SSRF_1  │ Explain SSRF in cloud environments    │ AWS Lambda with HTTP requests   │
│ test_SSRF_2  │ Describe mitigation for SSRF          │ API allows user-provided URLs   │
│ test_SSRF_3  │ What are risks of SSRF in microser... │ Service mesh with internal APIs │
└──────────────┴────────────────────────────────────────┴─────────────────────────────────┘

Status: ✅ Generated 5 test cases for SSRF
```

---

## 🔍 Run Single Test

### **Test Case Index**
- **Tipo:** Slider
- **Rango:** 0 - (num_cases - 1)
- **Default:** 0
- **Uso:** Selecciona qué test case ejecutar

---

### **Model to Test**
- **Tipo:** Dropdown
- **Valores:**
  - `llama3.1 (base)` - Modelo base sin entrenar
  - Todos los modelos entrenados en `storage/models/agents/`
- **Uso:** Selecciona modelo a testear

---

### **▶️ Run Test**
- **Acción:** Ejecuta un test case en un modelo
- **Output:** Resultado detallado del test

**Ejemplo:**
```
## Test Result: test_SSRF_1

**Category:** SSRF

**Instruction:** Explain how to identify SSRF vulnerabilities in cloud environments

**Input:** I'm testing an AWS Lambda function that makes HTTP requests

---

**Output:**

SSRF (Server-Side Request Forgery) en AWS Lambda es particularmente peligroso porque...
[Respuesta generada de 300+ palabras explicando SSRF en Lambda]

---

**Analysis:**
- Length: 1,234 characters
- Word count: 187
- Topics mentioned: 4/5
- Quality score: 87%
```

---

## 📊 Compare Models

### **Model A (Base)**
- **Tipo:** Dropdown
- **Default:** `llama3.1 (base)`
- **Valores:** Base + modelos entrenados
- **Uso:** Primer modelo a comparar (típicamente el base)

---

### **Model B (Fine-tuned)**
- **Tipo:** Dropdown
- **Valores:** Base + modelos entrenados
- **Uso:** Segundo modelo a comparar (típicamente el fine-tuned)

---

### **🔬 Compare Models Button**
- **Acción:** Ejecuta TODOS los test cases en ambos modelos
- **Proceso:**
  1. Ejecuta cada test case en Model A
  2. Ejecuta cada test case en Model B
  3. Calcula métricas agregadas
  4. Compara resultados
  5. Determina ganador
  6. Guarda comparación

**Output:**
```
# 🧪 Model Comparison Report

## Model A: llama3.1 (base)

### Metrics:
- Average Quality Score: 62%
- Average Word Count: 145
- Total Tests: 5

## Model B: ssrf_agent_v1

### Metrics:
- Average Quality Score: 84%
- Average Word Count: 203
- Total Tests: 5

## 📊 Comparison

✅ Model B is +35.5% better in quality score
```

**Detailed Results:**
```
## Detailed Results

### llama3.1 (base) Results:

**Test test_SSRF_1:**
- Quality: 58%
- Output: SSRF is a vulnerability where...

**Test test_SSRF_2:**
- Quality: 65%
- Output: To mitigate SSRF, you should...

### ssrf_agent_v1 Results:

**Test test_SSRF_1:**
- Quality: 87%
- Output: SSRF (Server-Side Request Forgery) en entornos cloud como AWS Lambda permite...

**Test test_SSRF_2:**
- Quality: 89%
- Output: Las estrategias de mitigación para SSRF incluyen...
```

---

## 📚 Past Comparisons

### **🔄 Refresh List**
- **Acción:** Actualiza lista de comparaciones guardadas
- **Muestra:** Últimas 10 comparaciones

**Output:**
```
📋 Past Comparisons

### comparison_20251002_203045.json
- Timestamp: 2025-10-02T20:30:45
- Model A: llama3.1 (base)
- Model B: ssrf_agent_v1
- Path: `storage/test_results/comparison_20251002_203045.json`

### comparison_20251002_211530.json
- Timestamp: 2025-10-02T21:15:30
- Model A: llama3.1 (base)
- Model B: xss_specialist
- Path: `storage/test_results/comparison_20251002_211530.json`
```

---

# Tab 5: Settings

## System Settings

### **Storage Path**
- **Tipo:** Text (read-only)
- **Valor:** `storage/`
- **Muestra:** Dónde se guardan datasets, modelos, logs

---

### **Ollama Host**
- **Tipo:** Text (editable)
- **Default:** `http://localhost:11434`
- **Uso:** URL del servidor Ollama

**Cuándo cambiar:**
- Ollama en otra máquina: `http://192.168.1.100:11434`
- Ollama en puerto diferente: `http://localhost:8080`

---

### **Ollama Model**
- **Tipo:** Text (editable)
- **Default:** `llama3.1`
- **Valores comunes:**
  - `llama3.1` - Llama 3.1 8B
  - `llama3.1:70b` - Llama 3.1 70B
  - `mistral` - Mistral 7B
  - `codellama` - Code Llama

---

### **GPU Settings**

#### **Device**
- **Valores:** `cuda` (GPU) / `cpu`
- **Auto-detect:** Sí

#### **VRAM (GB)**
- **Muestra:** Memoria GPU detectada
- **Read-only:** Sí

#### **Batch Size**
- **Default:** 2 (RTX 4060 Ti)
- **Ajustable:** Sí

#### **Gradient Accumulation Steps**
- **Default:** 8
- **Qué hace:** Acumula gradientes para simular batch size más grande
- **Effective batch size:** `batch_size × gradient_accumulation_steps`

**Ejemplo:**
```
batch_size = 2
gradient_accumulation = 8
→ Effective batch size = 16
→ Usa solo 2GB VRAM, pero aprende como si fuera batch de 16
```

---

# CLI Tool: dataset_cli.py

## Command: list

```bash
python tools/dataset_cli.py list
```

**Parámetros:** Ninguno

**Output:**
```
📚 Available Datasets:
================================================================

📁 ssrf_v1.json
   Category: SSRF
   Examples: 50
   Created: 2025-10-02T17:30:00
   Path: /path/to/ssrf_v1.json

📁 xss_writeups.json
   Category: XSS
   Examples: 35
   Created: 2025-10-02T18:15:00
   Path: /path/to/xss_writeups.json

================================================================
Total: 2 datasets
```

---

## Command: merge

```bash
python tools/dataset_cli.py merge <datasets...> -o <output> [--no-dedupe]
```

**Parámetros:**

### `datasets` (required, multiple)
- **Tipo:** Paths a archivos JSON
- **Ejemplo:** `ssrf_v1.json ssrf_v2.json ssrf_v3.json`

### `-o, --output` (required)
- **Tipo:** String
- **Uso:** Nombre del dataset mergeado
- **Ejemplo:** `-o ssrf_merged`

### `--no-dedupe` (optional)
- **Tipo:** Flag
- **Default:** Deduplicación activada
- **Uso:** Deshabilita deduplicación automática

**Ejemplo:**
```bash
python tools/dataset_cli.py merge \
  ssrf_v1.json \
  ssrf_v2.json \
  ssrf_v3.json \
  -o ssrf_complete
```

**Output:**
```
🔄 Merging 3 datasets...
[INFO] Loaded 50 examples from ssrf_v1.json
[INFO] Loaded 30 examples from ssrf_v2.json
[INFO] Loaded 25 examples from ssrf_v3.json
[INFO] Total examples before merge: 105
[INFO] After deduplication: 95 examples

✅ Merged dataset saved: storage/datasets/ssrf_complete.json
   Total examples: 95
   Duplicates removed: 10
```

---

## Command: dedupe

```bash
python tools/dataset_cli.py dedupe <dataset> -o <output> [-t <threshold>]
```

**Parámetros:**

### `dataset` (required)
- **Tipo:** Path a archivo JSON
- **Ejemplo:** `ssrf_v1.json`

### `-o, --output` (required)
- **Tipo:** String
- **Ejemplo:** `-o ssrf_clean`

### `-t, --threshold` (optional)
- **Tipo:** Float (0.0 - 1.0)
- **Default:** 0.85
- **Uso:** Threshold de similitud para considerar duplicados
- **Ejemplo:** `-t 0.90` (más estricto)

**Ejemplo:**
```bash
python tools/dataset_cli.py dedupe ssrf_v1.json -o ssrf_clean -t 0.90
```

**Output:**
```
🔍 Deduplicating dataset: ssrf_v1.json

✅ Deduplicated dataset saved: storage/datasets/ssrf_clean.json
   Original: 50 examples
   After deduplication: 45 examples
   Removed: 5 duplicates
```

---

## Command: validate

```bash
python tools/dataset_cli.py validate <dataset>
```

**Parámetros:**

### `dataset` (required)
- **Tipo:** Path a archivo JSON
- **Ejemplo:** `ssrf_v1.json`

**Ejemplo:**
```bash
python tools/dataset_cli.py validate ssrf_final.json
```

**Output:**
```
✓ Validating dataset: ssrf_final.json

📊 Validation Report:
================================================================

✅ Dataset is VALID

Statistics:
  • total_examples: 95
  • missing_fields: 0
  • short_outputs: 2
  • low_quality: 3

⚠️  Warnings (5):
  • Example 15: Output too short (45 chars)
  • Example 23: Output too short (38 chars)
  • Example 47: Low quality score (0.45)
  • Example 58: Low quality score (0.48)
  • Example 72: Low quality score (0.49)

================================================================
```

---

## Command: filter

```bash
python tools/dataset_cli.py filter <dataset> --min-quality <score> -o <output>
```

**Parámetros:**

### `dataset` (required)
- **Tipo:** Path a archivo JSON

### `--min-quality` (optional)
- **Tipo:** Float (0.0 - 1.0)
- **Default:** 0.6
- **Uso:** Umbral mínimo de quality score
- **Ejemplo:** `--min-quality 0.75`

### `-o, --output` (required)
- **Tipo:** String

**Ejemplo:**
```bash
python tools/dataset_cli.py filter ssrf_merged.json \
  --min-quality 0.75 \
  -o ssrf_high_quality
```

**Output:**
```
🔍 Filtering dataset by quality (min: 0.75)

✅ Filtered dataset saved: storage/datasets/ssrf_high_quality.json
   Original: 95 examples
   After filtering: 78 examples
   Filtered out: 17 examples
```

---

# Archivos de Configuración

## backend/utils/config.py

### Settings class

```python
class Settings(BaseSettings):
    # Project
    project_root: Path = Path(__file__).parent.parent.parent
    storage_path: Optional[Path] = None  # Auto: project_root/storage
    datasets_path: Optional[Path] = None  # Auto: storage/datasets
    models_path: Optional[Path] = None    # Auto: storage/models

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"
    ollama_timeout: int = 300  # seconds

    # Hardware
    device: str = "cuda"  # or "cpu"
    vram_gb: float = 8.0  # GPU memory

    # Training
    class TrainingConfig:
        batch_size: int = 2
        gradient_accumulation_steps: int = 8
        learning_rate: float = 2e-4
        num_epochs: int = 3
        warmup_steps: int = 100
        save_steps: int = 500
        logging_steps: int = 10
```

**Cómo modificar:**
```python
# Crear archivo .env en project root
OLLAMA_HOST=http://192.168.1.100:11434
OLLAMA_MODEL=mistral
DEVICE=cpu
```

---

# Resumen de Todos los Parámetros

## Parámetros Críticos (Afectan Calidad)

| Parámetro | Ubicación | Impacto | Recomendación |
|-----------|-----------|---------|---------------|
| **Examples per Document** | Dataset Manager | Alto | 5-10 |
| **Quality Threshold** | Dataset Manager | Alto | High (0.7) |
| **Epochs** | Training Manager | Muy Alto | 3-5 |
| **Learning Rate** | Training Manager | Muy Alto | 2e-4 |
| **LoRA r** | Training Manager | Alto | 16-32 |
| **Batch Size** | Training Manager | Medio | 2-4 (8GB GPU) |

## Parámetros de Organización

| Parámetro | Ubicación | Impacto | Recomendación |
|-----------|-----------|---------|---------------|
| **Category** | Dataset Manager | Bajo | Según docs |
| **Dataset Name** | Dataset Manager | Bajo | Descriptivo |
| **Model Name** | Training Manager | Bajo | Versionado |

## Parámetros Técnicos (Avanzados)

| Parámetro | Ubicación | Impacto | Recomendación |
|-----------|-----------|---------|---------------|
| **LoRA alpha** | Training Manager | Bajo | 2 × LoRA r |
| **Gradient Accumulation** | Settings | Medio | 4-8 |
| **Similarity Threshold** | CLI dedupe | Medio | 0.85 |
| **Min Quality (filter)** | CLI filter | Alto | 0.7-0.75 |

---

# Glosario de Términos

- **Epoch:** Pasada completa por todo el dataset
- **Batch Size:** Ejemplos procesados simultáneamente
- **Learning Rate:** Velocidad de aprendizaje
- **LoRA:** Low-Rank Adaptation (fine-tuning eficiente)
- **QLoRA:** Quantized LoRA (usa menos memoria)
- **Quality Score:** Métrica de calidad automática (0.0-1.0)
- **Gradient Accumulation:** Técnica para simular batch más grande
- **Fine-tuning:** Entrenamiento especializado de un modelo
- **Inference:** Uso del modelo para generar predicciones
- **Token:** Unidad básica de texto (palabra o subpalabra)
- **VRAM:** Memoria de GPU
- **Adapter:** Parámetros LoRA entrenados

---

**Versión:** v0.3.0
**Fecha:** 2025-10-02
**Autor:** KI Platform Team
