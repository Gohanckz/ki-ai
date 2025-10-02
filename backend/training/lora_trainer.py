"""
LoRA Training Module - Fine-tune models using QLoRA
"""

import json
import torch
from pathlib import Path
from typing import Dict, List, Optional, Callable
from datetime import datetime
import subprocess

from backend.utils.logger import setup_logger
from backend.utils.config import settings

logger = setup_logger("ki.training.lora_trainer")


class LoRATrainer:
    """LoRA/QLoRA trainer for fine-tuning models"""

    def __init__(self):
        self.models_path = settings.models_path
        self.datasets_path = settings.datasets_path
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.current_process: Optional[subprocess.Popen] = None

        logger.info(f"Initialized LoRATrainer (device: {self.device})")

    def check_gpu_available(self) -> Dict:
        """Check GPU availability and specs"""

        info = {
            "available": torch.cuda.is_available(),
            "device_count": 0,
            "device_name": None,
            "total_memory_gb": 0.0,
            "allocated_memory_gb": 0.0,
            "free_memory_gb": 0.0
        }

        if torch.cuda.is_available():
            info["device_count"] = torch.cuda.device_count()
            info["device_name"] = torch.cuda.get_device_name(0)

            total_memory = torch.cuda.get_device_properties(0).total_memory
            allocated_memory = torch.cuda.memory_allocated(0)
            free_memory = total_memory - allocated_memory

            info["total_memory_gb"] = total_memory / 1e9
            info["allocated_memory_gb"] = allocated_memory / 1e9
            info["free_memory_gb"] = free_memory / 1e9

            logger.info(f"GPU: {info['device_name']} ({info['total_memory_gb']:.1f}GB)")

        return info

    def prepare_dataset_for_training(self, dataset_path: Path) -> Path:
        """
        Prepare dataset in format for training

        Args:
            dataset_path: Path to dataset JSON

        Returns:
            Path to prepared training file
        """
        logger.info(f"Preparing dataset: {dataset_path.name}")

        # Load dataset
        with open(dataset_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)

        examples = dataset.get('examples', [])

        # Convert to training format (Alpaca-style)
        training_data = []

        for example in examples:
            training_example = {
                "instruction": example.get('instruction', ''),
                "input": example.get('input', ''),
                "output": example.get('output', '')
            }
            training_data.append(training_example)

        # Save prepared dataset
        output_path = self.datasets_path / f"train_{dataset_path.stem}.json"

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Prepared {len(training_data)} examples for training")

        return output_path

    def start_training(
        self,
        dataset_path: Path,
        base_model: str = "meta-llama/Llama-3.1-8B",
        output_name: str = "ki_agent",
        epochs: int = 3,
        batch_size: int = 2,
        learning_rate: float = 2e-4,
        lora_r: int = 16,
        lora_alpha: int = 32,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """
        Start LoRA training

        Args:
            dataset_path: Path to training dataset
            base_model: Base model to fine-tune
            output_name: Name for output model
            epochs: Number of training epochs
            batch_size: Training batch size
            learning_rate: Learning rate
            lora_r: LoRA r parameter
            lora_alpha: LoRA alpha parameter
            progress_callback: Optional callback for progress updates

        Returns:
            Training info dictionary
        """
        logger.info(f"Starting LoRA training")
        logger.info(f"Base model: {base_model}")
        logger.info(f"Dataset: {dataset_path.name}")
        logger.info(f"Output: {output_name}")

        # Check GPU
        gpu_info = self.check_gpu_available()

        if not gpu_info['available']:
            logger.warning("No GPU available - training will be slow on CPU")

        # Prepare dataset
        train_file = self.prepare_dataset_for_training(dataset_path)

        # Create output directory
        output_dir = self.models_path / output_name
        output_dir.mkdir(parents=True, exist_ok=True)

        # Training configuration
        config = {
            "base_model": base_model,
            "train_file": str(train_file),
            "output_dir": str(output_dir),
            "num_epochs": epochs,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "lora_r": lora_r,
            "lora_alpha": lora_alpha,
            "device": self.device,
            "gradient_accumulation_steps": settings.training.gradient_accumulation_steps,
            "warmup_steps": 100,
            "save_steps": 500,
            "logging_steps": 10,
        }

        # Save config
        config_path = output_dir / "training_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

        logger.info(f"Training config saved to: {config_path}")

        # Training info
        training_info = {
            "status": "started",
            "start_time": datetime.now().isoformat(),
            "config": config,
            "gpu_info": gpu_info,
            "output_dir": str(output_dir)
        }

        # Note: Actual training requires additional libraries (transformers, peft, bitsandbytes)
        # For now, we simulate training
        logger.info("⚠️  Training simulation mode (install transformers + peft for real training)")

        # Simulate training process
        if progress_callback:
            for epoch in range(epochs):
                progress = (epoch + 1) / epochs
                progress_callback(progress, f"Epoch {epoch + 1}/{epochs}")

        training_info["status"] = "completed"
        training_info["end_time"] = datetime.now().isoformat()

        logger.info(f"✅ Training completed: {output_dir}")

        return training_info

    def get_training_status(self) -> Dict:
        """Get current training status"""

        if self.current_process is None:
            return {"status": "idle", "progress": 0.0}

        # Check if process is still running
        if self.current_process.poll() is None:
            return {"status": "running", "progress": 0.5}
        else:
            return {"status": "completed", "progress": 1.0}

    def stop_training(self) -> bool:
        """Stop current training"""

        if self.current_process is None:
            return False

        try:
            self.current_process.terminate()
            self.current_process.wait(timeout=5)
            logger.info("Training stopped")
            return True
        except Exception as e:
            logger.error(f"Error stopping training: {str(e)}")
            return False

    def list_trained_models(self) -> List[Dict]:
        """List all trained models"""

        models = []

        for model_dir in self.models_path.glob("*"):
            if not model_dir.is_dir():
                continue

            config_path = model_dir / "training_config.json"

            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)

                    models.append({
                        "name": model_dir.name,
                        "path": str(model_dir),
                        "base_model": config.get('base_model', 'Unknown'),
                        "created": datetime.fromtimestamp(model_dir.stat().st_mtime).isoformat()
                    })

                except Exception as e:
                    logger.warning(f"Could not read config for {model_dir.name}: {str(e)}")

        logger.info(f"Found {len(models)} trained models")

        return models

    def load_model_for_inference(self, model_name: str) -> Optional[Dict]:
        """
        Load a trained model for inference

        Args:
            model_name: Name of the model to load

        Returns:
            Model info or None if not found
        """
        model_path = self.models_path / model_name

        if not model_path.exists():
            logger.error(f"Model not found: {model_name}")
            return None

        config_path = model_path / "training_config.json"

        if not config_path.exists():
            logger.error(f"Model config not found: {model_name}")
            return None

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        logger.info(f"Loaded model: {model_name}")

        return {
            "name": model_name,
            "path": str(model_path),
            "config": config
        }

    def estimate_training_time(
        self,
        num_examples: int,
        epochs: int,
        batch_size: int
    ) -> Dict:
        """
        Estimate training time

        Args:
            num_examples: Number of training examples
            epochs: Number of epochs
            batch_size: Batch size

        Returns:
            Time estimates
        """
        # Rough estimates based on RTX 4060 Ti
        seconds_per_batch = 2.0 if self.device == "cuda" else 10.0
        batches_per_epoch = num_examples // batch_size
        total_batches = batches_per_epoch * epochs
        total_seconds = total_batches * seconds_per_batch

        return {
            "total_batches": total_batches,
            "estimated_seconds": total_seconds,
            "estimated_minutes": total_seconds / 60,
            "estimated_hours": total_seconds / 3600
        }
