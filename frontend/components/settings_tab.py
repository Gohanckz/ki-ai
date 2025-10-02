"""
Settings Tab - Platform Configuration Interface
"""

import gradio as gr
from backend.utils.config import settings
from backend.utils.logger import setup_logger

logger = setup_logger("ki.frontend.settings")


def create_settings_tab():
    """Create the Settings tab UI"""

    with gr.Column():
        gr.Markdown(
            """
            ## ⚙️ Settings

            Configure KI platform settings and preferences.
            """
        )

        with gr.Group():
            gr.Markdown("### 🔌 Ollama Configuration")

            ollama_host = gr.Textbox(
                label="Ollama Host",
                value=settings.ollama_host,
                interactive=True,
                info="Ollama server URL"
            )

            ollama_model = gr.Dropdown(
                choices=["llama3.1", "llama3.1:70b", "mistral", "mixtral", "phi3"],
                value=settings.ollama_model,
                label="Default Ollama Model",
                interactive=True
            )

            test_ollama_btn = gr.Button("🔍 Test Ollama Connection", variant="secondary")

            ollama_status = gr.Textbox(
                label="Connection Status",
                value="Not tested",
                interactive=False
            )

        with gr.Group():
            gr.Markdown("### 💾 Storage Configuration")

            storage_path = gr.Textbox(
                label="Storage Directory",
                value=str(settings.storage_path),
                interactive=False,
                info="Location for datasets, models, and logs"
            )

            with gr.Row():
                gr.Number(
                    label="Available Disk Space (GB)",
                    value=0,
                    interactive=False
                )

                gr.Number(
                    label="Used Space (GB)",
                    value=0,
                    interactive=False
                )

        with gr.Group():
            gr.Markdown("### 🎮 GPU Configuration")

            gpu_info = gr.Textbox(
                label="Detected GPU",
                value="RTX 4060 Ti (8GB VRAM)",
                interactive=False
            )

            with gr.Row():
                max_vram_usage = gr.Slider(
                    minimum=1.0,
                    maximum=8.0,
                    value=settings.max_vram_usage_gb,
                    step=0.5,
                    label="Max VRAM Usage (GB)",
                    interactive=True
                )

                use_4bit_quant = gr.Checkbox(
                    label="Use 4-bit Quantization",
                    value=settings.use_4bit_quantization,
                    interactive=True
                )

        with gr.Group():
            gr.Markdown("### 🎯 Dataset Generation Settings")

            with gr.Row():
                default_quality = gr.Dropdown(
                    choices=["High", "Medium", "Low"],
                    value="High",
                    label="Default Quality Level",
                    interactive=True
                )

                min_examples = gr.Number(
                    label="Min Examples per Category",
                    value=10,
                    interactive=True
                )

        with gr.Row():
            save_settings_btn = gr.Button("💾 Save Settings", variant="primary")
            reset_settings_btn = gr.Button("🔄 Reset to Defaults", variant="secondary")

        settings_status = gr.Textbox(
            label="Status",
            value="Ready",
            interactive=False
        )

        gr.Markdown(
            """
            ---
            **Current Configuration:**
            - Ollama Host: `{ollama_host}`
            - Storage Path: `{storage_path}`
            - Max VRAM: `{max_vram}GB`
            - 4-bit Quantization: `{use_4bit}`
            """.format(
                ollama_host=settings.ollama_host,
                storage_path=settings.storage_path,
                max_vram=settings.max_vram_usage_gb,
                use_4bit="Enabled" if settings.use_4bit_quantization else "Disabled"
            )
        )
