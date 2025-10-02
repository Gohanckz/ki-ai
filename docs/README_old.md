# 🤖 KI - AI Training Platform for Bug Bounty

**KI** (Knowledge Intelligence) es una plataforma de entrenamiento de IA especializada en bug bounty y ciberseguridad.

## 🎯 Objetivo

Crear agentes de IA especializados en vulnerabilidades web mediante:
1. Generación automática de datasets desde documentos
2. Entrenamiento de modelos con LoRA/QLoRA
3. Evaluación y comparación de agentes
4. Interfaz visual completa

## 🏗️ Arquitectura

```
KI/
├── frontend/          # Interfaz Gradio
├── backend/           # Lógica de negocio (FastAPI)
├── storage/           # Datos y modelos
├── configs/           # Configuraciones
├── scripts/           # Scripts auxiliares
├── tests/            # Tests
└── docs/             # Documentación
```

## 🚀 Quick Start

### 1. Setup

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Setup Ollama
./scripts/setup_ollama.sh
```

### 2. Configuración

```bash
# Copiar configuración de ejemplo
cp .env.example .env

# Editar configuración
nano .env
```

### 3. Ejecutar

```bash
# Iniciar plataforma
python frontend/app.py

# O usar script
./scripts/start_platform.sh
```

## 📚 Documentación

- [Arquitectura Completa](docs/ARCHITECTURE.md)
- [Guía de Usuario](docs/USER_GUIDE.md)
- [Guía de Desarrollo](docs/DEVELOPER_GUIDE.md)
- [API Reference](docs/API_REFERENCE.md)

## 🛠️ Stack Tecnológico

- **Frontend:** Gradio 4.x
- **Backend:** FastAPI + Python 3.10+
- **LLM:** Ollama (Llama 3.1, Mixtral)
- **Training:** HuggingFace Transformers + PEFT
- **Vector DB:** ChromaDB
- **Monitoring:** TensorBoard + W&B

## 📦 Estructura de Directorios

Ver [STRUCTURE.md](docs/STRUCTURE.md) para detalles completos.

## 🎓 Uso Básico

### Generar Dataset

1. Ir a tab "Dataset Manager"
2. Upload PDFs/DOCX sobre vulnerabilidad
3. Seleccionar categoría (SSRF, XSS, SQLi, etc.)
4. Click "Generate"
5. Revisar y validar ejemplos generados

### Entrenar Agente

1. Ir a tab "Training Studio"
2. Seleccionar dataset
3. Configurar hyperparámetros (o usar preset)
4. Click "Start Training"
5. Monitorear progreso en tiempo real

### Probar Agente

1. Ir a tab "Testing Lab"
2. Seleccionar agente entrenado
3. Escribir prompts de prueba
4. Evaluar calidad de respuestas

## 🤝 Contribuir

Ver [CONTRIBUTING.md](docs/CONTRIBUTING.md)

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE)

## 🙏 Agradecimientos

- HuggingFace por Transformers
- Ollama por LLMs locales
- Gradio por UI framework

---

**Desarrollado con ❤️ para la comunidad de bug bounty**
