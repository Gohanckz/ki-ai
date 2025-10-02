"""
Dataset Manager Tab - Drag & Drop Document Upload and Dataset Generation
"""

import gradio as gr
from pathlib import Path
from typing import List, Dict, Optional
import json
from datetime import datetime

from backend.data.parsers import parse_document, is_supported_document, get_supported_extensions
from backend.core.dataset_generator import DatasetGenerator
from backend.core.dataset_tools import DatasetTools
from backend.utils.logger import setup_logger
from backend.utils.config import settings

logger = setup_logger("ki.frontend.dataset_manager")

# Initialize tools
dataset_generator = DatasetGenerator()
dataset_tools = DatasetTools()


def handle_file_upload(files: List) -> tuple:
    """
    Handle uploaded files and display them in a table

    Args:
        files: List of uploaded file objects

    Returns:
        Tuple of (file_display_data, file_paths, status_message)
    """
    if not files:
        return [], [], "No files uploaded"

    file_display = []
    file_paths = []

    for file in files:
        file_path = Path(file.name)
        file_size_kb = file_path.stat().st_size / 1024 if file_path.exists() else 0

        # Check if supported
        supported = is_supported_document(file_path)

        file_display.append({
            "Name": file_path.name,
            "Size": f"{file_size_kb:.2f} KB",
            "Type": file_path.suffix.upper().replace(".", ""),
            "Status": "✅ Supported" if supported else "❌ Unsupported"
        })

        if supported:
            file_paths.append(str(file_path))

    status_msg = f"✅ Uploaded {len(file_paths)} supported files (Total: {len(files)} files)"

    return file_display, file_paths, status_msg


def parse_uploaded_documents(file_paths: List[str], progress=gr.Progress()) -> tuple:
    """
    Parse uploaded documents and extract text

    Args:
        file_paths: List of file paths to parse
        progress: Gradio progress tracker

    Returns:
        Tuple of (parsing_results, parsed_data, status_message)
    """
    if not file_paths:
        return [], {}, "No files to parse"

    parsed_results = []
    parsed_data = {}
    total_words = 0

    for i, file_path in enumerate(file_paths):
        # Update progress
        progress(i / len(file_paths), desc=f"Parsing {Path(file_path).name}...")

        # Parse document
        result = parse_document(Path(file_path))

        if result['success']:
            parsed_results.append({
                "File": result['file_name'],
                "Type": result['file_type'].upper(),
                "Words": result['word_count'],
                "Status": "✅ Success"
            })

            parsed_data[file_path] = result
            total_words += result['word_count']
        else:
            parsed_results.append({
                "File": result['file_name'],
                "Type": "ERROR",
                "Words": 0,
                "Status": f"❌ {result['error']}"
            })

    progress(1.0, desc="✅ Parsing complete!")

    status_msg = f"✅ Parsed {len(parsed_data)} documents ({total_words:,} total words)"

    return parsed_results, parsed_data, status_msg


def generate_dataset_examples(
    parsed_data: Dict,
    category: str,
    examples_per_doc: int,
    quality_level: str,
    progress=gr.Progress()
) -> tuple:
    """
    Generate training examples from parsed documents using Ollama

    Args:
        parsed_data: Dictionary of parsed document data
        category: Vulnerability category (SSRF, XSS, etc.)
        examples_per_doc: Number of examples to generate per document
        quality_level: Quality threshold (High, Medium, Low)
        progress: Gradio progress tracker

    Returns:
        Tuple of (generation_log, examples_data, status_message)
    """
    if not parsed_data:
        return "❌ No parsed documents available", {}, "No documents to process"

    log_lines = []
    log_lines.append(f"[INFO] Starting dataset generation with Ollama")
    log_lines.append(f"[INFO] Category: {category}")
    log_lines.append(f"[INFO] Target: {examples_per_doc} examples per document")
    log_lines.append(f"[INFO] Quality level: {quality_level}")
    log_lines.append(f"[INFO] Total documents: {len(parsed_data)}")
    log_lines.append("")

    # Check Ollama availability
    if dataset_generator.ollama_client.is_available():
        log_lines.append("[✓] Ollama is running - using real AI generation")
    else:
        log_lines.append("[!] Ollama not available - using simulated generation")
        log_lines.append("[!] Install Ollama and run 'ollama serve' for real generation")

    log_lines.append("")

    # Use real dataset generator
    try:
        dataset = dataset_generator.generate_dataset(
            parsed_documents=parsed_data,
            category=category,
            examples_per_doc=examples_per_doc,
            quality_level=quality_level
        )

        # Create detailed log
        stats = dataset['metadata'].get('stats', {})

        log_lines.append(f"[SUCCESS] Dataset generation complete!")
        log_lines.append("")
        log_lines.append("📊 Statistics:")
        log_lines.append(f"  • Documents processed: {stats.get('total_documents', 0)}")
        log_lines.append(f"  • Examples generated: {stats.get('total_generated', 0)}")
        log_lines.append(f"  • Examples validated: {stats.get('total_validated', 0)}")
        log_lines.append(f"  • Examples rejected: {stats.get('total_rejected', 0)}")
        log_lines.append("")

        if stats.get('total_rejected', 0) > 0:
            rejection_rate = (stats['total_rejected'] / stats['total_generated']) * 100
            log_lines.append(f"[INFO] Quality rejection rate: {rejection_rate:.1f}%")

        status_msg = f"✅ Generated {len(dataset['examples'])} high-quality examples from {len(parsed_data)} documents"

    except Exception as e:
        logger.error(f"Error in dataset generation: {str(e)}")
        log_lines.append(f"[ERROR] Generation failed: {str(e)}")
        dataset = {"examples": [], "metadata": {}}
        status_msg = f"❌ Error: {str(e)}"

    return "\n".join(log_lines), dataset, status_msg


def save_dataset(dataset: Dict, dataset_name: str) -> str:
    """
    Save dataset to JSON file

    Args:
        dataset: Dataset dictionary
        dataset_name: Name for the dataset file

    Returns:
        Status message
    """
    if not dataset or 'examples' not in dataset:
        return "❌ No dataset to save"

    # Create datasets directory
    datasets_dir = settings.storage_path / "datasets"
    datasets_dir.mkdir(parents=True, exist_ok=True)

    # Clean filename
    clean_name = "".join(c for c in dataset_name if c.isalnum() or c in (' ', '-', '_')).strip()
    if not clean_name:
        clean_name = f"dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Save dataset
    output_path = datasets_dir / f"{clean_name}.json"

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    logger.info(f"Saved dataset to: {output_path}")

    return f"✅ Dataset saved to: {output_path}"


def create_dataset_manager_tab():
    """Create the Dataset Manager tab UI"""

    with gr.Column():
        gr.Markdown(
            """
            ## 📁 Dataset Manager

            Upload documents to automatically generate high-quality training datasets.
            Supported formats: PDF, DOCX, TXT, Markdown
            """
        )

        # File upload section
        with gr.Group():
            gr.Markdown("### 📤 Upload Documents")

            file_upload = gr.File(
                file_count="multiple",
                file_types=[".pdf", ".docx", ".txt", ".text", ".md", ".markdown", ".log"],
                label="Drag & Drop Documents or Click to Browse",
                elem_classes=["upload-container"]
            )

            file_display = gr.DataFrame(
                headers=["Name", "Size", "Type", "Status"],
                label="Uploaded Files",
                interactive=False
            )

            upload_status = gr.Textbox(
                label="Upload Status",
                interactive=False,
                show_label=True
            )

        # Configuration section
        with gr.Group():
            gr.Markdown("### ⚙️ Dataset Configuration")

            with gr.Row():
                category_dropdown = gr.Dropdown(
                    choices=["SSRF", "XSS", "SQLi", "IDOR", "RCE", "XXE", "CSRF", "LFI/RFI", "Authentication Bypass", "Custom"],
                    value="SSRF",
                    label="Vulnerability Category",
                    interactive=True
                )

                examples_per_doc = gr.Slider(
                    minimum=1,
                    maximum=20,
                    value=5,
                    step=1,
                    label="Examples per Document",
                    interactive=True
                )

            with gr.Row():
                quality_dropdown = gr.Dropdown(
                    choices=["High", "Medium", "Low"],
                    value="High",
                    label="Quality Threshold",
                    interactive=True
                )

                dataset_name_input = gr.Textbox(
                    label="Dataset Name",
                    value="my_dataset",
                    interactive=True
                )

        # Action buttons
        with gr.Row():
            parse_btn = gr.Button("📄 Parse Documents", variant="secondary")
            generate_btn = gr.Button("🎯 Generate Dataset", variant="primary")
            save_btn = gr.Button("💾 Save Dataset", variant="secondary")

        # Results section
        with gr.Group():
            gr.Markdown("### 📊 Processing Results")

            parsing_results = gr.DataFrame(
                headers=["File", "Type", "Words", "Status"],
                label="Parsing Results",
                interactive=False
            )

            generation_log = gr.Textbox(
                label="Generation Log",
                lines=15,
                max_lines=30,
                interactive=False,
                show_copy_button=True
            )

            result_status = gr.Textbox(
                label="Status",
                interactive=False
            )

        # Saved datasets section
        with gr.Group():
            gr.Markdown("### 📚 Saved Datasets")

            datasets_list = gr.Markdown(
                "No datasets saved yet. Generate and save a dataset to see it here."
            )

        # Hidden state to store data
        file_paths_state = gr.State([])
        parsed_data_state = gr.State({})
        dataset_state = gr.State({})

        # Event handlers
        file_upload.change(
            fn=handle_file_upload,
            inputs=[file_upload],
            outputs=[file_display, file_paths_state, upload_status]
        )

        parse_btn.click(
            fn=parse_uploaded_documents,
            inputs=[file_paths_state],
            outputs=[parsing_results, parsed_data_state, result_status]
        )

        generate_btn.click(
            fn=generate_dataset_examples,
            inputs=[
                parsed_data_state,
                category_dropdown,
                examples_per_doc,
                quality_dropdown
            ],
            outputs=[generation_log, dataset_state, result_status]
        )

        save_btn.click(
            fn=save_dataset,
            inputs=[dataset_state, dataset_name_input],
            outputs=[result_status]
        )

        # Supported formats info
        gr.Markdown(
            f"""
            ---
            **Supported formats:** {', '.join(get_supported_extensions())}
            """
        )
