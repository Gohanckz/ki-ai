# 📖 KI Platform - Guía Completa de Uso

## 🎯 Explicación de Parámetros de la Interfaz

### Tab 1: 📁 Dataset Manager

#### Sección: "Upload Documents"
**Drag & Drop Documents or Click to Browse**
- **Qué hace:** Área para arrastrar/soltar archivos o seleccionarlos
- **Formatos aceptados:** PDF, DOCX, TXT, Markdown (.md)
- **Dónde se guardan:** Los archivos NO se copian automáticamente
  - Gradio lee desde su ubicación original temporalmente
  - Si quieres mantenerlos, guárdalos manualmente en: `/mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki/storage/documents/[categoría]/`

**Uploaded Files (tabla)**
- **Name:** Nombre del archivo subido
- **Size:** Tamaño en KB
- **Type:** Extensión del archivo (PDF, DOCX, etc.)
- **Status:** ✅ Supported o ❌ Unsupported

---

#### Sección: "Dataset Configuration"

**1. Vulnerability Category**
```
Opciones: SSRF, XSS, SQLi, IDOR, RCE, XXE, CSRF, LFI/RFI, Authentication Bypass, Custom
```
- **Qué hace:** Define la categoría de vulnerabilidad para el dataset
- **Por qué importa:** Los ejemplos generados se etiquetan con esta categoría
- **Dónde se usa:** En metadata del dataset y para organizar ejemplos
- **Valor por defecto:** SSRF

**2. Examples per Document**
```
Rango: 1-20
Valor por defecto: 5
```
- **Qué hace:** Número de ejemplos de entrenamiento a generar POR CADA documento
- **Ejemplo:** Si subes 10 documentos y pones 5 ejemplos → 50 ejemplos totales
- **Recomendaciones:**
  - 3-5 para documentos largos (>5000 palabras)
  - 5-10 para documentos medianos (1000-5000 palabras)
  - 10-15 para documentos cortos (<1000 palabras)

**3. Quality Threshold**
```
Opciones: High, Medium, Low
```
- **High:** Solo acepta ejemplos de alta calidad (filtrado estricto)
  - Más lento, menos ejemplos, mejor calidad
- **Medium:** Balance entre calidad y cantidad
  - Velocidad media, calidad aceptable
- **Low:** Acepta todos los ejemplos
  - Rápido, mayor cantidad, calidad variable

**4. Dataset Name**
```
Valor por defecto: "my_dataset"
```
- **Qué hace:** Nombre del archivo JSON que se guardará
- **Dónde se guarda:** `/storage/datasets/[nombre].json`
- **Formato:** Se limpia automáticamente (solo alfanuméricos, -, _)

---

#### Sección: "Processing Results"

**Parsing Results (tabla)**
- **File:** Nombre del documento parseado
- **Type:** Tipo de archivo (PDF, DOCX, TEXT, MARKDOWN)
- **Words:** Cantidad de palabras extraídas
- **Status:** ✅ Success o ❌ Error con mensaje

**Generation Log**
- **Qué muestra:** Log en tiempo real de la generación
- **Información incluida:**
  - [INFO] Archivos procesados
  - [SUCCESS] Ejemplos generados
  - [WARNING] Problemas de calidad
  - [ERROR] Errores durante generación

**Status**
- Mensaje final con resumen: "✅ Generated X examples from Y documents"

---

### Tab 2: 🎓 Training Studio (Preparado para Sesión 4)

**Select Dataset**
- Dropdown con datasets guardados en `/storage/datasets/`

**Base Model**
```
Opciones: llama-3.1-8b, mistral-7b, phi-3-mini
```
- Modelo base de HuggingFace para fine-tuning

**Hardware Preset**
```
Opciones: RTX 4060 Ti (8GB), RTX 3080 (10GB), RTX 4090 (24GB), Custom
```
- **RTX 4060 Ti (8GB):** Configuración actual optimizada
  - batch_size: 2
  - gradient_accumulation: 8
  - 4-bit quantization: Enabled
  - max_vram_usage: 7.5GB

**Training Epochs**
```
Rango: 1-10
Valor por defecto: 3
```
- Número de veces que el modelo verá el dataset completo

**Advanced Settings:**
- **Learning Rate:** 2e-4 (tasa de aprendizaje)
- **Batch Size:** 2 (muestras por paso)
- **Gradient Accumulation Steps:** 8 (acumular gradientes antes de actualizar)

---

### Tab 3: 🧪 Testing Lab (Preparado para Sesión 4)

**Select Trained Model**
- Lista de modelos entrenados guardados en `/storage/models/agents/`

**Temperature**
```
Rango: 0.1 - 2.0
Valor por defecto: 0.7
```
- **0.1-0.5:** Respuestas más determinísticas y conservadoras
- **0.7-0.9:** Balance creatividad/precisión (recomendado)
- **1.0-2.0:** Respuestas más creativas y variadas

**Test Input**
- Campo de texto para ingresar escenario de prueba

**Model Response**
- Salida del modelo entrenado

---

### Tab 4: ⚙️ Settings

**Ollama Host**
```
Valor por defecto: http://localhost:11434
```
- URL del servidor Ollama (local)

**Default Ollama Model**
```
Opciones: llama3.1, llama3.1:70b, mistral, mixtral, phi3
```
- Modelo LLM para generar datasets

**Max VRAM Usage (GB)**
```
Rango: 1.0 - 8.0
Valor por defecto: 7.5
```
- Límite de memoria GPU para entrenamiento
- Dejar 0.5GB libre para el sistema

**Use 4-bit Quantization**
```
Valor por defecto: True
```
- Reduce uso de VRAM en ~50%
- Permite entrenar modelos más grandes en GPUs pequeñas

---

## 📂 Dónde se Almacenan los Archivos

### Estructura Completa de Storage:

```
/mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki/storage/
│
├── documents/                    ← DOCUMENTOS FUENTE
│   ├── ssrf/                     ← Docs de SSRF
│   ├── xss/                      ← Docs de XSS
│   ├── sqli/                     ← Docs de SQLi
│   └── general/                  ← Docs generales
│
├── datasets/                     ← DATASETS GENERADOS
│   ├── raw/                      ← Datasets sin procesar
│   ├── processed/                ← Datasets validados
│   └── final/                    ← Datasets listos para entrenar
│   └── [nombre].json             ← Datasets guardados manualmente
│
├── models/                       ← MODELOS ENTRENADOS
│   ├── base/                     ← Modelos base descargados
│   └── agents/                   ← Agentes entrenados (LoRA adapters)
│       └── ssrf_agent_v1/
│       └── xss_agent_v2/
│
├── logs/                         ← LOGS DEL SISTEMA
│   ├── training/                 ← Logs de entrenamiento
│   ├── generation/               ← Logs de generación de datasets
│   └── system/                   ← Logs generales
│
└── databases/                    ← BASES DE DATOS
    ├── metadata.db               ← SQLite con metadata
    └── chromadb/                 ← Vector DB para embeddings
```

### Detalles de Ubicaciones:

#### 1. **Documentos Cargados:**
**TEMPORAL:** Cuando subes archivos con drag & drop:
- Gradio crea copias temporales en `/tmp/gradio/`
- Estos archivos se borran al cerrar la aplicación

**PERMANENTE (Recomendado):** Para mantener documentos:
```bash
# Copiar manualmente a:
/mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki/storage/documents/[categoria]/

# Ejemplo:
cp mi_documento.pdf /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki/storage/documents/ssrf/
```

#### 2. **Datasets Generados:**
Cuando haces click en "Save Dataset", se guardan en:
```
/mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki/storage/datasets/

Archivo: [nombre_del_dataset].json
```

**Estructura del JSON:**
```json
{
  "metadata": {
    "category": "SSRF",
    "created_at": "2025-10-02T17:30:00",
    "total_examples": 50,
    "source_documents": 10,
    "examples_per_doc": 5,
    "quality_level": "High"
  },
  "examples": [
    {
      "instruction": "Explain SSRF vulnerability",
      "input": "What is SSRF in AWS?",
      "output": "SSRF (Server-Side Request Forgery)...",
      "source": "aws_ssrf_guide.pdf",
      "category": "SSRF",
      "timestamp": "2025-10-02T17:30:15"
    }
  ]
}
```

#### 3. **Modelos Entrenados:**
Después de entrenar (Sesión 4+), se guardan en:
```
/mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki/storage/models/agents/

Estructura:
ssrf_agent_v1/
├── adapter_config.json
├── adapter_model.bin
├── training_args.bin
└── tokenizer files
```

---

## 🔄 Sistema de Datasets: ¿Nuevo o Mejorar Existente?

### **Comportamiento Actual (v0.1.0):**

#### ❌ NO Hace (Por Ahora):
- No puede **mejorar/actualizar** un dataset existente automáticamente
- No tiene funcionalidad de "merge" automático
- No detecta duplicados entre datasets

#### ✅ SÍ Hace:
- **Genera datasets NUEVOS** cada vez
- Cada generación es independiente
- Puedes guardar múltiples versiones

### **Solución para Mejorar Datasets Existentes:**

#### Opción 1: Merge Manual (Próxima Sesión 4)
```python
# Implementaremos una función de merge:
1. Cargar dataset existente
2. Generar nuevos ejemplos
3. Combinar y deduplicar
4. Guardar dataset mejorado
```

#### Opción 2: Workflow Recomendado (Ahora)
```
1. Generar dataset inicial: "ssrf_v1.json" (50 ejemplos)
2. Generar dataset adicional: "ssrf_v2.json" (30 ejemplos nuevos)
3. En Sesión 4: Implementar merge → "ssrf_final.json" (80 ejemplos sin duplicados)
```

---

## 🔄 Sistema de Feedback para Mejora

### **Estado Actual (v0.1.0):**

#### ❌ NO Implementado (Aún):
- No hay sistema de feedback directo en la UI
- No puede marcar ejemplos como "buenos" o "malos"
- No hay re-entrenamiento automático con correcciones

### **Roadmap de Feedback (Sesiones Futuras):**

#### Fase 1: Review Manual (Sesión 4)
```
Dataset Manager → Nueva sección:
┌─────────────────────────────────┐
│ 📝 Review Generated Examples    │
│                                  │
│ Example 1/50                     │
│ Instruction: [...]               │
│ Input: [...]                     │
│ Output: [...]                    │
│                                  │
│ Quality: ⭐⭐⭐⭐⭐              │
│ [✓ Accept] [✗ Reject] [✏️ Edit] │
└─────────────────────────────────┘
```

#### Fase 2: Feedback Loop (Sesión 5-6)
```python
# Sistema de feedback propuesto:
1. Testing Lab → Usuario prueba modelo
2. Marca respuesta como "incorrecta"
3. Proporciona corrección esperada
4. Sistema genera ejemplo correcto
5. Se añade al dataset de fine-tuning
6. Re-entrena con ejemplos corregidos
```

#### Fase 3: Active Learning (Futuro)
```
1. Modelo identifica ejemplos difíciles
2. Pide feedback del usuario
3. Aprende de correcciones
4. Mejora iterativamente
```

---

## 💡 Cómo Implementar Feedback (Manual por Ahora)

### Método 1: Editar Dataset JSON

**Paso 1:** Generar y guardar dataset
```bash
Dataset guardado en:
/storage/datasets/ssrf_v1.json
```

**Paso 2:** Abrir con editor de texto
```bash
nano /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki/storage/datasets/ssrf_v1.json
```

**Paso 3:** Editar ejemplos incorrectos
```json
{
  "instruction": "Mal ejemplo - EDITAR",
  "output": "Respuesta incorrecta"
}

// Cambiar a:
{
  "instruction": "Ejemplo corregido",
  "output": "Respuesta correcta basada en feedback"
}
```

**Paso 4:** Guardar y usar en entrenamiento

### Método 2: Script de Corrección (Crear en Sesión 4)

```python
# feedback_tool.py (a implementar)

def add_corrected_example(dataset_path, bad_example_id, corrected_output):
    """
    Añade ejemplo corregido al dataset
    """
    dataset = load_dataset(dataset_path)

    # Marcar ejemplo malo
    dataset['examples'][bad_example_id]['quality'] = 'rejected'

    # Añadir corrección
    corrected_example = {
        "instruction": dataset['examples'][bad_example_id]['instruction'],
        "input": dataset['examples'][bad_example_id]['input'],
        "output": corrected_output,
        "source": "user_feedback",
        "quality": "verified"
    }

    dataset['examples'].append(corrected_example)
    save_dataset(dataset, dataset_path)
```

---

## 📊 Resumen de Capacidades Actuales vs Futuras

| Funcionalidad | Estado Actual (v0.1.0) | Próxima Implementación |
|---------------|------------------------|------------------------|
| **Upload documentos** | ✅ Funcional | - |
| **Parse documentos** | ✅ Funcional | - |
| **Generar datasets** | 🟡 Simulado | Sesión 4: Ollama real |
| **Guardar datasets** | ✅ Funcional | - |
| **Merge datasets** | ❌ No | Sesión 4 |
| **Deduplicar ejemplos** | ❌ No | Sesión 4 |
| **Review manual** | ❌ No | Sesión 4 |
| **Feedback en UI** | ❌ No | Sesión 5 |
| **Re-entrenamiento con feedback** | ❌ No | Sesión 6 |
| **Active Learning** | ❌ No | Futuro |

---

## 🎯 Workflow Recomendado (Ahora)

### Para Crear un Buen Dataset:

**1. Recopilar Documentos (Manual)**
```bash
# Crear carpeta por categoría
mkdir -p /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki/storage/documents/ssrf

# Copiar tus PDFs/docs
cp ~/mis_documentos_ssrf/*.pdf ./storage/documents/ssrf/
```

**2. Generar Dataset en UI**
```
1. Upload documentos (drag & drop)
2. Click "Parse Documents"
3. Configurar:
   - Category: SSRF
   - Examples per doc: 5
   - Quality: High
4. Click "Generate Dataset"
5. Revisar logs
6. Click "Save Dataset" con nombre: "ssrf_initial"
```

**3. Revisar y Editar Manualmente**
```bash
# Abrir dataset
nano storage/datasets/ssrf_initial.json

# Revisar cada ejemplo
# Editar outputs incorrectos
# Eliminar ejemplos malos
```

**4. Generar Datasets Adicionales**
```
Repetir proceso con nuevos documentos
Guardar como: ssrf_batch2.json, ssrf_batch3.json, etc.
```

**5. Preparar para Entrenamiento (Sesión 4)**
```
Implementaremos merge tool para combinar:
ssrf_initial.json + ssrf_batch2.json → ssrf_final.json
```

---

## 🔧 Configuraciones Importantes

### Archivos de Configuración:

**1. `/backend/utils/config.py`**
- Todas las rutas y parámetros del sistema
- Puedes editar valores por defecto aquí

**2. `.env` (crear si necesitas customizar)**
```bash
# Ejemplo .env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1
MAX_VRAM_USAGE_GB=7.5
EXAMPLES_PER_DOCUMENT=5
QUALITY_THRESHOLD=0.7
```

---

**¿Necesitas que implemente alguna de estas funcionalidades ahora? Por ejemplo:**
1. Script para merge de datasets
2. Tool de review manual de ejemplos
3. Deduplicador de ejemplos
4. Validador de calidad personalizado

