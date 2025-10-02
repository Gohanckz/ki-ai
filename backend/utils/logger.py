"""
Logging configuration for KI platform
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime
from rich.logging import RichHandler
from rich.console import Console

from .config import settings


console = Console()


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors"""

    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'
    }

    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        return super().format(record)


def setup_logger(
    name: str,
    log_file: Optional[Path] = None,
    level: Optional[str] = None
) -> logging.Logger:
    """
    Setup logger with file and console handlers

    Args:
        name: Logger name
        log_file: Optional log file path
        level: Optional log level (overrides settings)

    Returns:
        Configured logger
    """

    logger = logging.getLogger(name)
    logger.setLevel(level or settings.log_level)

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler with Rich
    if settings.log_to_console:
        console_handler = RichHandler(
            console=console,
            show_time=True,
            show_path=False,
            rich_tracebacks=True
        )
        console_handler.setLevel(level or settings.log_level)
        logger.addHandler(console_handler)

    # File handler
    if settings.log_to_file:
        if log_file is None:
            # Default log file
            timestamp = datetime.now().strftime("%Y%m%d")
            log_file = settings.logs_path / "system" / f"{name}_{timestamp}.log"

        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level or settings.log_level)

        formatter = logging.Formatter(settings.log_format)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger


# Default loggers
main_logger = setup_logger("ki.main")
api_logger = setup_logger("ki.api")
training_logger = setup_logger("ki.training", settings.logs_path / "training" / f"training_{datetime.now().strftime('%Y%m%d')}.log")
generation_logger = setup_logger("ki.generation", settings.logs_path / "generation" / f"generation_{datetime.now().strftime('%Y%m%d')}.log")


def log_system_info():
    """Log system information"""
    import torch
    import platform

    main_logger.info("=" * 60)
    main_logger.info(f"🤖 KI - AI Training Platform v{settings.app_version}")
    main_logger.info("=" * 60)
    main_logger.info(f"Platform: {platform.system()} {platform.release()}")
    main_logger.info(f"Python: {platform.python_version()}")
    main_logger.info(f"PyTorch: {torch.__version__}")
    main_logger.info(f"CUDA Available: {torch.cuda.is_available()}")

    if torch.cuda.is_available():
        main_logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
        main_logger.info(f"CUDA Version: {torch.version.cuda}")
        vram_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
        main_logger.info(f"VRAM: {vram_gb:.2f} GB")

    main_logger.info(f"Project Root: {settings.project_root}")
    main_logger.info(f"Storage Path: {settings.storage_path}")
    main_logger.info("=" * 60)


def log_training_start(config: dict):
    """Log training start"""
    training_logger.info("=" * 60)
    training_logger.info("🎓 TRAINING STARTED")
    training_logger.info("=" * 60)

    for key, value in config.items():
        training_logger.info(f"{key}: {value}")

    training_logger.info("=" * 60)


def log_training_end(results: dict):
    """Log training end"""
    training_logger.info("=" * 60)
    training_logger.info("✅ TRAINING COMPLETED")
    training_logger.info("=" * 60)

    for key, value in results.items():
        training_logger.info(f"{key}: {value}")

    training_logger.info("=" * 60)


def log_generation_start(doc_count: int):
    """Log dataset generation start"""
    generation_logger.info("=" * 60)
    generation_logger.info(f"📝 DATASET GENERATION STARTED - {doc_count} documents")
    generation_logger.info("=" * 60)


def log_generation_progress(current: int, total: int, examples: int):
    """Log generation progress"""
    generation_logger.info(f"Progress: {current}/{total} documents | {examples} examples generated")


def log_generation_end(results: dict):
    """Log generation end"""
    generation_logger.info("=" * 60)
    generation_logger.info("✅ GENERATION COMPLETED")
    generation_logger.info("=" * 60)

    for key, value in results.items():
        generation_logger.info(f"{key}: {value}")

    generation_logger.info("=" * 60)
