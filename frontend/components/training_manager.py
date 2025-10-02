"""
Training Manager Tab - Train models with LoRA/QLoRA
"""

import gradio as gr
from pathlib import Path
from typing import Optional

from backend.training.lora_trainer import LoRATrainer
from backend.core.dataset_tools import DatasetTools
from backend.utils.logger import setup_logger

logger = setup_logger("ki.frontend.training_manager")

# Initialize tools
trainer = LoRATrainer()
dataset_tools = DatasetTools()


def get_available_datasets():
    """Get list of available datasets"""
    datasets = dataset_tools.list_datasets()
    return [ds['name'] for ds in datasets]


def get_gpu_info() -> str:
    """Get GPU information"""
    info = trainer.check_gpu_available()

    if not info['available']:
        return "❌ No GPU detected - Training will use CPU (very slow)"

    output = f"""
✅ GPU Available: {info['device_name']}

**Memory:**
- Total: {info['total_memory_gb']:.1f} GB
- Allocated: {info['allocated_memory_gb']:.1f} GB
- Free: {info['free_memory_gb']:.1f} GB

**Recommendation for RTX 4060 Ti (8GB):**
- Batch size: 2-4
- Gradient accumulation: 4-8
- Use QLoRA (4-bit quantization)
"""

    return output


def estimate_training(dataset_name: str, epochs: int, batch_size: int) -> str:
    """Estimate training time"""

    if not dataset_name:
        return "Select a dataset first"

    try:
        dataset_path = dataset_tools.datasets_path / dataset_name
        dataset = dataset_tools.load_dataset(dataset_path)
        num_examples = len(dataset.get('examples', []))

        estimates = trainer.estimate_training_time(num_examples, epochs, batch_size)

        output = f"""
📊 **Training Estimates:**

- Dataset: {dataset_name}
- Examples: {num_examples}
- Epochs: {epochs}
- Batch size: {batch_size}
- Total batches: {estimates['total_batches']}

⏱️ **Estimated Time:**
- {estimates['estimated_minutes']:.1f} minutes
- {estimates['estimated_hours']:.2f} hours

Note: Actual time may vary based on GPU load and model size.
"""

        return output

    except Exception as e:
        logger.error(f"Error estimating training: {str(e)}")
        return f"❌ Error: {str(e)}"


def start_training_job(
    dataset_name: str,
    model_name: str,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    lora_r: int,
    lora_alpha: int,
    progress=gr.Progress()
) -> str:
    """Start training"""

    if not dataset_name:
        return "❌ Please select a dataset"

    if not model_name:
        return "❌ Please provide a model name"

    try:
        dataset_path = dataset_tools.datasets_path / dataset_name

        logger.info(f"Starting training: {model_name}")

        # Progress callback
        def update_progress(prog, desc):
            progress(prog, desc=desc)

        # Start training
        result = trainer.start_training(
            dataset_path=dataset_path,
            output_name=model_name,
            epochs=epochs,
            batch_size=batch_size,
            learning_rate=learning_rate,
            lora_r=lora_r,
            lora_alpha=lora_alpha,
            progress_callback=update_progress
        )

        if result['status'] == 'completed':
            return f"""
✅ **Training Completed!**

Model saved to: `{result['output_dir']}`

**Configuration:**
- Base model: {result['config']['base_model']}
- Epochs: {result['config']['num_epochs']}
- Batch size: {result['config']['batch_size']}
- Learning rate: {result['config']['learning_rate']}
- LoRA r: {result['config']['lora_r']}
- LoRA alpha: {result['config']['lora_alpha']}

GPU: {result['gpu_info']['device_name'] if result['gpu_info']['available'] else 'CPU'}

Note: This is a simulation. Install transformers + peft for real training.
"""
        else:
            return f"❌ Training failed: {result.get('error', 'Unknown error')}"

    except Exception as e:
        logger.error(f"Training error: {str(e)}")
        return f"❌ Error: {str(e)}"


def list_trained_models() -> str:
    """List all trained models"""

    models = trainer.list_trained_models()

    if not models:
        return "No trained models found."

    output = ["## 🤖 Trained Models", ""]

    for model in models:
        output.append(f"### 📦 {model['name']}")
        output.append(f"- **Base model:** {model['base_model']}")
        output.append(f"- **Created:** {model['created']}")
        output.append(f"- **Path:** `{model['path']}`")
        output.append("")

    return "\n".join(output)


def create_training_manager_tab():
    """Create the Training Manager tab UI"""

    with gr.Column():
        gr.Markdown(
            """
            ## 🎓 Training Manager

            Fine-tune models using LoRA/QLoRA on your custom datasets.
            """
        )

        # GPU Info
        with gr.Group():
            gr.Markdown("### 💻 Hardware Info")

            gpu_info_text = gr.Markdown(value=get_gpu_info())

            refresh_gpu_btn = gr.Button("🔄 Refresh GPU Info", size="sm")

        # Training Configuration
        with gr.Group():
            gr.Markdown("### ⚙️ Training Configuration")

            with gr.Row():
                dataset_dropdown = gr.Dropdown(
                    choices=get_available_datasets(),
                    label="Training Dataset",
                    interactive=True
                )

                model_name_input = gr.Textbox(
                    label="Model Name",
                    value="ki_agent_v1",
                    interactive=True
                )

            with gr.Row():
                epochs_slider = gr.Slider(
                    minimum=1,
                    maximum=10,
                    value=3,
                    step=1,
                    label="Epochs",
                    interactive=True
                )

                batch_size_slider = gr.Slider(
                    minimum=1,
                    maximum=8,
                    value=2,
                    step=1,
                    label="Batch Size",
                    interactive=True
                )

            with gr.Row():
                learning_rate_input = gr.Number(
                    label="Learning Rate",
                    value=2e-4,
                    interactive=True
                )

                lora_r_slider = gr.Slider(
                    minimum=4,
                    maximum=64,
                    value=16,
                    step=4,
                    label="LoRA r",
                    interactive=True
                )

                lora_alpha_slider = gr.Slider(
                    minimum=8,
                    maximum=128,
                    value=32,
                    step=8,
                    label="LoRA alpha",
                    interactive=True
                )

        # Training Estimates
        with gr.Group():
            gr.Markdown("### 📊 Training Estimates")

            estimate_btn = gr.Button("🔍 Estimate Training Time", size="sm")

            estimate_output = gr.Markdown(value="Click 'Estimate' to see time estimates")

        # Start Training
        with gr.Row():
            start_training_btn = gr.Button("🚀 Start Training", variant="primary", size="lg")
            stop_training_btn = gr.Button("⏹️ Stop Training", variant="stop", size="lg")

        training_output = gr.Markdown(
            label="Training Output",
            value="Configure training parameters and click 'Start Training'"
        )

        # Trained Models
        with gr.Group():
            gr.Markdown("### 📦 Trained Models")

            refresh_models_btn = gr.Button("🔄 Refresh List", size="sm")

            models_list = gr.Markdown(value=list_trained_models())

        # Help section
        with gr.Accordion("ℹ️ Training Parameters Help", open=False):
            gr.Markdown(
                """
                **Epochs:** Number of complete passes through the dataset
                - More epochs = better learning, but risk of overfitting
                - Recommended: 3-5 for most tasks

                **Batch Size:** Number of examples processed together
                - Larger = faster training, more GPU memory
                - For 8GB GPU: 2-4 recommended

                **Learning Rate:** How fast the model learns
                - Too high = unstable training
                - Too low = very slow learning
                - Recommended: 1e-4 to 3e-4

                **LoRA r:** Rank of LoRA matrices
                - Higher = more parameters, better quality
                - Lower = faster, less memory
                - Recommended: 8-32

                **LoRA alpha:** Scaling factor for LoRA
                - Usually 2x of LoRA r
                - Recommended: 16-64
                """
            )

        # Event handlers
        refresh_gpu_btn.click(
            fn=lambda: get_gpu_info(),
            outputs=[gpu_info_text]
        )

        estimate_btn.click(
            fn=estimate_training,
            inputs=[dataset_dropdown, epochs_slider, batch_size_slider],
            outputs=[estimate_output]
        )

        start_training_btn.click(
            fn=start_training_job,
            inputs=[
                dataset_dropdown,
                model_name_input,
                epochs_slider,
                batch_size_slider,
                learning_rate_input,
                lora_r_slider,
                lora_alpha_slider
            ],
            outputs=[training_output]
        )

        refresh_models_btn.click(
            fn=list_trained_models,
            outputs=[models_list]
        )

        gr.Markdown(
            """
            ---
            **Note:** Real training requires additional packages: `transformers`, `peft`, `bitsandbytes`

            Install with: `pip install transformers peft bitsandbytes accelerate`
            """
        )
