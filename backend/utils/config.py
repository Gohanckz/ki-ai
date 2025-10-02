"""
Configuration management for KI platform
"""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""

    # Application
    app_name: str = "KI"
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = True

    # Paths
    project_root: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    storage_path: Optional[Path] = None
    datasets_path: Optional[Path] = None
    models_path: Optional[Path] = None
    documents_path: Optional[Path] = None
    logs_path: Optional[Path] = None

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # Gradio UI
    gradio_host: str = "0.0.0.0"
    gradio_port: int = 7860
    gradio_share: bool = False
    gradio_theme: str = "default"

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"
    ollama_timeout: int = 300
    ollama_num_gpu: int = 1
    ollama_num_thread: int = 8

    # Training
    default_base_model: str = "codellama/CodeLlama-7b-hf"
    batch_size: int = 2
    gradient_accumulation_steps: int = 8
    learning_rate: float = 2e-4
    num_epochs: int = 3
    max_length: int = 512
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    use_4bit_quantization: bool = True
    use_fp16: bool = True
    use_gradient_checkpointing: bool = True

    # GPU
    cuda_visible_devices: str = "0"
    max_vram_usage_gb: float = 7.5
    enable_cpu_offload: bool = True

    # Dataset Generation
    examples_per_document: int = 5
    min_example_length: int = 50
    max_example_length: int = 500
    quality_threshold: float = 0.7
    enable_deduplication: bool = True

    # Database
    db_path: Optional[Path] = None
    vector_db_path: Optional[Path] = None

    # Monitoring
    enable_tensorboard: bool = True
    tensorboard_port: int = 6006
    enable_wandb: bool = False
    wandb_project: str = "ki-training"
    wandb_entity: Optional[str] = None
    wandb_api_key: Optional[str] = None

    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_to_file: bool = True
    log_to_console: bool = True

    # Security
    secret_key: str = "change-this-to-a-secure-random-key"
    allowed_origins: str = "*"
    allowed_hosts: str = "*"

    # Features
    enable_auto_save: bool = True
    enable_gpu_monitoring: bool = True
    enable_quality_validation: bool = True
    enable_checkpoint_resume: bool = True

    # Advanced
    max_workers: int = 4
    cache_size_mb: int = 1024
    cleanup_on_exit: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Auto-configure paths
        if self.storage_path is None:
            self.storage_path = self.project_root / "storage"

        if self.datasets_path is None:
            self.datasets_path = self.storage_path / "datasets"

        if self.models_path is None:
            self.models_path = self.storage_path / "models"

        if self.documents_path is None:
            self.documents_path = self.storage_path / "documents"

        if self.logs_path is None:
            self.logs_path = self.storage_path / "logs"

        if self.db_path is None:
            self.db_path = self.storage_path / "databases" / "metadata.db"

        if self.vector_db_path is None:
            self.vector_db_path = self.storage_path / "databases" / "chromadb"

        # Create directories
        self._create_directories()

    def _create_directories(self):
        """Create necessary directories"""
        dirs = [
            self.storage_path,
            self.datasets_path,
            self.datasets_path / "raw",
            self.datasets_path / "processed",
            self.datasets_path / "final",
            self.models_path,
            self.models_path / "base",
            self.models_path / "agents",
            self.documents_path,
            self.documents_path / "ssrf",
            self.documents_path / "xss",
            self.documents_path / "sqli",
            self.documents_path / "general",
            self.logs_path,
            self.logs_path / "training",
            self.logs_path / "generation",
            self.logs_path / "system",
            self.storage_path / "databases",
        ]

        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
