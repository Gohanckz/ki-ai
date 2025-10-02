# 🚀 KI Platform - Nuevas Funcionalidades Implementadas

## ✅ Implementado en Esta Sesión

### 1. 🤖 Generación Real con Ollama

**¿Qué es?**
Ya no es simulación - ahora KI usa Ollama para generar ejemplos reales de entrenamiento usando IA.

**Cómo funciona:**
1. Subes documentos sobre vulnerabilidades
2. KI analiza el contenido con Llama 3.1
3. Genera ejemplos educativos de alta calidad
4. Filtra por calidad automáticamente

**Beneficios:**
- ✅ Ejemplos basados en contenido real de documentos
- ✅ Explicaciones técnicas detalladas
- ✅ Diversidad en escenarios y contextos
- ✅ Quality scoring automático

**Estado:**
- 🟢 **Ollama corriendo:** Genera ejemplos reales con IA
- 🟡 **Ollama no disponible:** Usa generación simulada (fallback)

---

### 2. 🔄 Merge de Datasets

**¿Qué es?**
Combina múltiples datasets en uno solo, eliminando duplicados automáticamente.

**Casos de uso:**
```
Dataset 1: ssrf_v1.json (50 ejemplos de docs iniciales)
Dataset 2: ssrf_v2.json (30 ejemplos de nuevos docs)
Dataset 3: ssrf_v3.json (25 ejemplos corregidos)

→ Merge → ssrf_final.json (95 ejemplos únicos)
```

**Cómo usarlo:**

#### Opción 1: CLI Tool
```bash
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki
source ../venv/bin/activate

# Merge múltiples datasets
python tools/dataset_cli.py merge ssrf_v1.json ssrf_v2.json ssrf_v3.json -o ssrf_final

# Ver resultado
python tools/dataset_cli.py list
```

#### Opción 2: Python
```python
from backend.core.dataset_tools import DatasetTools

tools = DatasetTools()

# Merge
merged = tools.merge_datasets(
    dataset_paths=[
        Path("storage/datasets/ssrf_v1.json"),
        Path("storage/datasets/ssrf_v2.json")
    ],
    output_name="ssrf_merged",
    deduplicate=True
)

# Save
tools.save_dataset(merged, "ssrf_final")
```

---

### 3. 🧹 Deduplicación Inteligente

**¿Qué es?**
Elimina ejemplos duplicados o muy similares usando análisis de similitud.

**Cómo funciona:**
- Calcula hash de contenido (duplicados exactos)
- Mide similitud semántica (duplicados parciales)
- Umbral configurable (default: 85% similitud)

**Ejemplo:**
```
Ejemplo 1: "Explica SSRF en AWS Lambda"
Ejemplo 2: "Describe SSRF en AWS Lambda"
→ Similitud: 92% → DUPLICADO (se elimina uno)

Ejemplo 3: "SSRF en API Gateway"
→ Similitud: 45% → ÚNICO (se mantiene)
```

**Cómo usarlo:**
```bash
# Deduplicar dataset
python tools/dataset_cli.py dedupe ssrf_v1.json -o ssrf_v1_clean

# Threshold personalizado
python tools/dataset_cli.py dedupe ssrf_v1.json -o ssrf_clean -t 0.90
```

---

### 4. ✅ Validador de Calidad

**¿Qué valida?**
- ✓ Estructura correcta del JSON
- ✓ Campos requeridos presentes
- ✓ Longitud mínima de outputs
- ✓ Scores de calidad
- ✓ Campos faltantes
- ✓ Ejemplos mal formados

**Reporte incluye:**
- Total de ejemplos
- Ejemplos con errores
- Advertencias de calidad
- Recomendaciones

**Cómo usarlo:**
```bash
# Validar dataset
python tools/dataset_cli.py validate ssrf_v1.json

# Output:
# ✅ Dataset is VALID
# Statistics:
#   • total_examples: 50
#   • missing_fields: 0
#   • short_outputs: 2
#   • low_quality: 1
```

---

### 5. 🎯 Filtrado por Calidad

**¿Qué es?**
Filtra ejemplos basándose en quality score automático.

**Quality Score (0.0 - 1.0):**
- **0.8-1.0:** Excelente calidad
- **0.6-0.8:** Buena calidad
- **0.4-0.6:** Calidad media
- **<0.4:** Baja calidad

**Factores que afectan el score:**
- Longitud y detalle del output
- Claridad de la instruction
- Contexto en el input
- Estructura completa

**Cómo usarlo:**
```bash
# Filtrar solo alta calidad (>=0.7)
python tools/dataset_cli.py filter ssrf_v1.json --min-quality 0.7 -o ssrf_high_quality

# Resultado:
# Original: 50 ejemplos
# Después: 42 ejemplos
# Filtrados: 8 ejemplos de baja calidad
```

---

## 🛠️ Herramienta CLI Completa

### Instalación:
```bash
cd /mnt/c/Users/Gohanckz/Desktop/IA-Proyect/ki
source ../venv/bin/activate
chmod +x tools/dataset_cli.py
```

### Comandos Disponibles:

#### 1. Listar Datasets
```bash
python tools/dataset_cli.py list

# Output:
# 📚 Available Datasets:
# ================================================================
#
# 📁 ssrf_v1.json
#    Category: SSRF
#    Examples: 50
#    Created: 2025-10-02T17:30:00
#    Path: /path/to/ssrf_v1.json
```

#### 2. Merge Datasets
```bash
# Merge 2+ datasets
python tools/dataset_cli.py merge ssrf_v1.json ssrf_v2.json -o ssrf_merged

# Merge sin deduplicar
python tools/dataset_cli.py merge dataset1.json dataset2.json -o merged --no-dedupe
```

#### 3. Deduplicar
```bash
# Deduplicar con threshold default (0.85)
python tools/dataset_cli.py dedupe ssrf_v1.json -o ssrf_clean

# Threshold personalizado (más estricto)
python tools/dataset_cli.py dedupe ssrf_v1.json -o ssrf_clean -t 0.95
```

#### 4. Validar
```bash
python tools/dataset_cli.py validate ssrf_v1.json
```

#### 5. Filtrar por Calidad
```bash
# Solo ejemplos con quality >= 0.7
python tools/dataset_cli.py filter ssrf_v1.json --min-quality 0.7 -o ssrf_hq

# Solo excelente calidad (>= 0.9)
python tools/dataset_cli.py filter ssrf_v1.json --min-quality 0.9 -o ssrf_excellent
```

---

## 📊 Workflow Completo Actualizado

### Paso 1: Generar Dataset Inicial
```
1. Abrir UI: http://localhost:7860
2. Upload documentos sobre SSRF
3. Parse Documents
4. Generate Dataset (Ollama generará ejemplos reales)
5. Save: "ssrf_v1"
```

### Paso 2: Generar Datasets Adicionales
```
1. Upload más documentos SSRF
2. Generate Dataset
3. Save: "ssrf_v2"

Repetir con diferentes docs → ssrf_v3, ssrf_v4...
```

### Paso 3: Merge y Limpieza (CLI)
```bash
# Activar venv
source ../venv/bin/activate

# Merge todos
python tools/dataset_cli.py merge \
  ssrf_v1.json \
  ssrf_v2.json \
  ssrf_v3.json \
  -o ssrf_merged

# Resultado: ssrf_merged.json con ejemplos únicos
```

### Paso 4: Validar Calidad
```bash
# Validar
python tools/dataset_cli.py validate ssrf_merged.json

# Si hay ejemplos de baja calidad, filtrar
python tools/dataset_cli.py filter ssrf_merged.json --min-quality 0.7 -o ssrf_final
```

### Paso 5: Dataset Final
```
✅ ssrf_final.json
   • Ejemplos únicos (sin duplicados)
   • Alta calidad (score >= 0.7)
   • Listo para entrenamiento
```

---

## 🎯 Mejoras en la UI

### Dataset Manager - Cambios:

**Antes (v0.1.0):**
- ❌ Generación simulada
- ❌ No mostraba estadísticas reales

**Ahora (v0.2.0):**
- ✅ Generación real con Ollama
- ✅ Estadísticas detalladas:
  - Documentos procesados
  - Ejemplos generados
  - Ejemplos validados
  - Ejemplos rechazados por calidad
  - Tasa de rechazo
- ✅ Detección automática de Ollama
- ✅ Fallback a simulación si Ollama no disponible

**Log de Generación Mejorado:**
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

---

## 🔧 API de Programación

### DatasetGenerator
```python
from backend.core.dataset_generator import DatasetGenerator

generator = DatasetGenerator()

# Generar ejemplos de un documento
examples = generator.generate_examples_from_document(
    document_text="Contenido del documento...",
    document_name="ssrf_guide.pdf",
    category="SSRF",
    num_examples=5,
    quality_level="High",
    temperature=0.7
)

# Generar dataset completo
dataset = generator.generate_dataset(
    parsed_documents={
        "doc1.pdf": {"full_text": "...", "word_count": 1000},
        "doc2.pdf": {"full_text": "...", "word_count": 1500}
    },
    category="SSRF",
    examples_per_doc=5,
    quality_level="High"
)
```

### DatasetTools
```python
from backend.core.dataset_tools import DatasetTools

tools = DatasetTools()

# Merge
merged = tools.merge_datasets([path1, path2], "merged", deduplicate=True)

# Deduplicate
unique = tools.deduplicate_examples(examples, similarity_threshold=0.85)

# Validate
report = tools.validate_dataset(dataset)

# Filter
high_quality = tools.filter_examples_by_quality(examples, min_quality=0.7)

# Balance (limitar por categoría)
balanced = tools.balance_dataset(dataset, max_per_category=100)

# List
datasets = tools.list_datasets()

# Save
path = tools.save_dataset(dataset, "my_dataset")
```

---

## 📈 Comparación: Antes vs Ahora

| Funcionalidad | v0.1.0 (Antes) | v0.2.0 (Ahora) |
|---------------|----------------|----------------|
| **Generación de datasets** | Simulada | ✅ Real con Ollama |
| **Quality scoring** | No | ✅ Automático |
| **Merge datasets** | Manual (editar JSON) | ✅ CLI tool |
| **Deduplicación** | No | ✅ Inteligente |
| **Validación** | No | ✅ Completa |
| **Filtrado por calidad** | No | ✅ CLI + API |
| **Estadísticas** | Básicas | ✅ Detalladas |
| **Logs** | Simples | ✅ Informativos |

---

## 🎓 Ejemplos de Uso Real

### Caso 1: Dataset de SSRF desde múltiples fuentes

```bash
# Día 1: Generar desde reportes de HackerOne
UI → Upload reportes H1 → Generate → Save "ssrf_h1"

# Día 2: Generar desde writeups de bug bounty
UI → Upload writeups → Generate → Save "ssrf_writeups"

# Día 3: Generar desde documentación técnica
UI → Upload docs AWS → Generate → Save "ssrf_aws_docs"

# Día 4: Merge y limpieza
python tools/dataset_cli.py merge \
  ssrf_h1.json \
  ssrf_writeups.json \
  ssrf_aws_docs.json \
  -o ssrf_complete

python tools/dataset_cli.py filter ssrf_complete.json \
  --min-quality 0.75 \
  -o ssrf_final

# Resultado: 150+ ejemplos únicos de alta calidad
```

### Caso 2: Mejorar dataset existente

```bash
# Tienes ssrf_old.json (100 ejemplos, algunos duplicados)

# 1. Deduplicar
python tools/dataset_cli.py dedupe ssrf_old.json -o ssrf_clean

# 2. Validar
python tools/dataset_cli.py validate ssrf_clean.json

# 3. Filtrar baja calidad
python tools/dataset_cli.py filter ssrf_clean.json \
  --min-quality 0.6 \
  -o ssrf_improved

# 4. Generar nuevos ejemplos en UI
UI → Upload nuevos docs → Generate → Save "ssrf_new"

# 5. Merge
python tools/dataset_cli.py merge \
  ssrf_improved.json \
  ssrf_new.json \
  -o ssrf_v2_final
```

---

## 🚀 Próximos Pasos (Sesión 5)

Con estas herramientas ya puedes:
1. ✅ Generar datasets reales con IA
2. ✅ Mergear múltiples versiones
3. ✅ Eliminar duplicados
4. ✅ Validar calidad
5. ✅ Filtrar por calidad

**Siguiente fase:**
- 🔜 UI para review/edición de ejemplos
- 🔜 Feedback loop en interfaz
- 🔜 Entrenamiento de modelos
- 🔜 Testing de agentes entrenados

---

## 📚 Documentación Adicional

**Guías:**
- `GUIA_COMPLETA_USO.md` - Guía general de la plataforma
- `RESUMEN_RAPIDO.txt` - Resumen visual rápido
- `NUEVAS_FEATURES.md` - Este archivo

**Archivos de código:**
- `backend/core/dataset_generator.py` - Generación con Ollama
- `backend/core/dataset_tools.py` - Herramientas de gestión
- `tools/dataset_cli.py` - CLI tool
- `frontend/components/dataset_manager.py` - UI actualizada

---

**Versión:** v0.2.0
**Fecha:** 2025-10-02
**Estado:** ✅ Todas las features funcionando
