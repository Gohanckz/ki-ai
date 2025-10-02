"""
Training Studio Tab - Model Training Interface
"""

import gradio as gr
from pathlib import Path
from backend.utils.logger import setup_logger

logger = setup_logger("ki.frontend.training_studio")


def create_training_studio_tab():
    """Create the Training Studio tab UI"""

    with gr.Column():
        gr.Markdown(
            """
            ## 🎓 Training Studio

            Train specialized AI agents using your generated datasets.
            Optimized for RTX 4060 Ti (8GB VRAM) with 4-bit quantization.
            """
        )

        with gr.Group():
            gr.Markdown("### 🔧 Training Configuration")

            with gr.Row():
                dataset_selector = gr.Dropdown(
                    choices=[],
                    label="Select Dataset",
                    interactive=True,
                    info="Choose a dataset to train on"
                )

                model_selector = gr.Dropdown(
                    choices=["llama-3.1-8b", "mistral-7b", "phi-3-mini"],
                    value="llama-3.1-8b",
                    label="Base Model",
                    interactive=True
                )

            with gr.Row():
                preset_selector = gr.Dropdown(
                    choices=["RTX 4060 Ti (8GB)", "RTX 3080 (10GB)", "RTX 4090 (24GB)", "Custom"],
                    value="RTX 4060 Ti (8GB)",
                    label="Hardware Preset",
                    interactive=True
                )

                epochs = gr.Slider(
                    minimum=1,
                    maximum=10,
                    value=3,
                    step=1,
                    label="Training Epochs",
                    interactive=True
                )

        with gr.Accordion("Advanced Settings", open=False):
            with gr.Row():
                learning_rate = gr.Number(
                    value=2e-4,
                    label="Learning Rate",
                    interactive=True
                )

                batch_size = gr.Number(
                    value=2,
                    label="Batch Size",
                    interactive=True
                )

                gradient_accumulation = gr.Number(
                    value=8,
                    label="Gradient Accumulation Steps",
                    interactive=True
                )

        with gr.Row():
            start_training_btn = gr.Button("▶️ Start Training", variant="primary", size="lg")
            stop_training_btn = gr.Button("⏹️ Stop Training", variant="stop", size="lg")

        with gr.Group():
            gr.Markdown("### 📊 Training Progress")

            training_progress = gr.Textbox(
                label="Status",
                value="Ready to train",
                interactive=False
            )

            training_log = gr.Textbox(
                label="Training Log",
                lines=15,
                max_lines=30,
                interactive=False,
                show_copy_button=True
            )

        with gr.Group():
            gr.Markdown("### 💾 Saved Models")

            models_list = gr.Markdown(
                "No trained models yet. Start a training session to create your first model."
            )

        gr.Markdown(
            """
            ---
            **Note:** Training will be implemented in the next session with full Ollama integration
            """
        )
