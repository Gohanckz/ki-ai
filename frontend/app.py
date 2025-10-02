"""
KI Platform - Main Application Entry Point
Desktop application with Gradio Blocks UI
"""

import gradio as gr
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.utils.config import settings
from backend.utils.logger import setup_logger
from frontend.components.dataset_manager import create_dataset_manager_tab
from frontend.components.training_studio import create_training_studio_tab
from frontend.components.testing_lab import create_testing_lab_tab
from frontend.components.settings_tab import create_settings_tab

logger = setup_logger("ki.frontend")


def create_app():
    """Create main Gradio application"""

    # Custom CSS for better visual appeal
    custom_css = """
    .gradio-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .tab-nav button {
        font-size: 16px;
        font-weight: 500;
    }

    .upload-container {
        border: 2px dashed #4A90E2;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        background-color: #f8f9fa;
    }

    .progress-bar {
        background-color: #4A90E2;
    }

    .status-success {
        color: #28a745;
    }

    .status-error {
        color: #dc3545;
    }

    .status-warning {
        color: #ffc107;
    }
    """

    with gr.Blocks(
        title="KI - AI Training Platform",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="slate",
            neutral_hue="slate"
        ),
        css=custom_css
    ) as app:

        # Header
        with gr.Row():
            gr.Markdown(
                """
                # 🎯 KI - AI Training Platform
                **Knowledge Intelligence for Bug Bounty Training**

                Transform documents into high-quality training datasets • Train specialized AI agents • Test and deploy
                """
            )

        # Main tabs
        with gr.Tabs() as tabs:

            # Tab 1: Dataset Manager
            with gr.Tab("📁 Dataset Manager", id="dataset_manager"):
                create_dataset_manager_tab()

            # Tab 2: Training Studio
            with gr.Tab("🎓 Training Studio", id="training"):
                create_training_studio_tab()

            # Tab 3: Testing Lab
            with gr.Tab("🧪 Testing Lab", id="testing"):
                create_testing_lab_tab()

            # Tab 4: Settings
            with gr.Tab("⚙️ Settings", id="settings"):
                create_settings_tab()

        # Footer
        with gr.Row():
            gr.Markdown(
                """
                ---
                **KI Platform v0.1.0** | Running locally on `localhost:7860` |
                Storage: `{storage_path}` | Ollama: `{ollama_host}`
                """.format(
                    storage_path=settings.storage_path,
                    ollama_host=settings.ollama_host
                )
            )

    return app


def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("KI Platform - AI Training Platform")
    logger.info("=" * 60)
    logger.info(f"Storage path: {settings.storage_path}")
    logger.info(f"Ollama host: {settings.ollama_host}")
    logger.info(f"Ollama model: {settings.ollama_model}")
    logger.info("=" * 60)

    # Create and launch app
    app = create_app()

    logger.info("Launching UI on http://localhost:7860")

    app.launch(
        server_name="127.0.0.1",  # Only local access
        server_port=7860,
        share=False,              # Do not share online
        inbrowser=True,           # Open browser automatically
        show_error=True,
        quiet=False
    )


if __name__ == "__main__":
    main()
