"""
Dataset Review Tab - View, edit, and improve dataset examples
"""

import gradio as gr
from pathlib import Path
from typing import List, Dict, Optional
import json

from backend.core.dataset_tools import DatasetTools
from backend.utils.logger import setup_logger

logger = setup_logger("ki.frontend.dataset_review")

# Initialize tools
dataset_tools = DatasetTools()

# Global state for current dataset
current_dataset: Optional[Dict] = None
current_index: int = 0


def load_dataset_for_review(dataset_name: str) -> tuple:
    """Load a dataset for review"""
    global current_dataset, current_index

    if not dataset_name:
        return "No dataset selected", "", "", "", 0.0, "0/0", None, None

    try:
        dataset_path = dataset_tools.datasets_path / dataset_name
        current_dataset = dataset_tools.load_dataset(dataset_path)
        current_index = 0

        if not current_dataset or 'examples' not in current_dataset:
            return "❌ Invalid dataset format", "", "", "", 0.0, "0/0", None, None

        total = len(current_dataset['examples'])

        if total == 0:
            return "❌ Dataset is empty", "", "", "", 0.0, "0/0", None, None

        # Load first example
        return load_example_at_index(0)

    except Exception as e:
        logger.error(f"Error loading dataset: {str(e)}")
        return f"❌ Error: {str(e)}", "", "", "", 0.0, "0/0", None, None


def load_example_at_index(index: int) -> tuple:
    """Load example at specific index"""
    global current_dataset, current_index

    if not current_dataset or 'examples' not in current_dataset:
        return "No dataset loaded", "", "", "", 0.0, "0/0", None, None

    examples = current_dataset['examples']

    if not examples:
        return "No examples in dataset", "", "", "", 0.0, "0/0", None, None

    # Clamp index
    index = max(0, min(index, len(examples) - 1))
    current_index = index

    example = examples[index]

    # Extract fields
    instruction = example.get('instruction', '')
    input_text = example.get('input', '')
    output = example.get('output', '')
    quality = example.get('quality_score', 0.0)
    category = example.get('category', 'Unknown')
    flagged = example.get('flagged', False)

    # Position indicator
    position = f"{index + 1}/{len(examples)}"

    # Status message
    flag_status = "🚩 Flagged as bad" if flagged else "✅ Good"
    status = f"Example {position} | Category: {category} | Quality: {quality:.2f} | Status: {flag_status}"

    return status, instruction, input_text, output, quality, position, gr.update(value=index), current_dataset


def navigate_previous() -> tuple:
    """Navigate to previous example"""
    global current_index
    return load_example_at_index(current_index - 1)


def navigate_next() -> tuple:
    """Navigate to next example"""
    global current_index
    return load_example_at_index(current_index + 1)


def save_current_example(instruction: str, input_text: str, output: str, quality: float) -> str:
    """Save changes to current example"""
    global current_dataset, current_index

    if not current_dataset or 'examples' not in current_dataset:
        return "❌ No dataset loaded"

    examples = current_dataset['examples']

    if current_index >= len(examples):
        return "❌ Invalid index"

    # Update example
    examples[current_index]['instruction'] = instruction
    examples[current_index]['input'] = input_text
    examples[current_index]['output'] = output
    examples[current_index]['quality_score'] = quality
    examples[current_index]['edited'] = True

    logger.info(f"Updated example {current_index + 1}")

    return f"✅ Saved changes to example {current_index + 1}"


def flag_as_bad() -> tuple:
    """Flag current example as bad"""
    global current_dataset, current_index

    if not current_dataset or 'examples' not in current_dataset:
        return "❌ No dataset loaded", "", "", "", 0.0, "0/0", None, None

    examples = current_dataset['examples']
    examples[current_index]['flagged'] = True

    logger.info(f"Flagged example {current_index + 1} as bad")

    # Reload to show updated status
    return load_example_at_index(current_index)


def flag_as_good() -> tuple:
    """Flag current example as good"""
    global current_dataset, current_index

    if not current_dataset or 'examples' not in current_dataset:
        return "❌ No dataset loaded", "", "", "", 0.0, "0/0", None, None

    examples = current_dataset['examples']
    examples[current_index]['flagged'] = False

    logger.info(f"Flagged example {current_index + 1} as good")

    # Reload to show updated status
    return load_example_at_index(current_index)


def delete_current_example() -> tuple:
    """Delete current example"""
    global current_dataset, current_index

    if not current_dataset or 'examples' not in current_dataset:
        return "❌ No dataset loaded", "", "", "", 0.0, "0/0", None, None

    examples = current_dataset['examples']

    if len(examples) == 0:
        return "❌ No examples to delete", "", "", "", 0.0, "0/0", None, None

    # Delete example
    deleted = examples.pop(current_index)
    logger.info(f"Deleted example {current_index + 1}: {deleted.get('instruction', '')[:50]}...")

    # Adjust index if needed
    if current_index >= len(examples) and current_index > 0:
        current_index -= 1

    # Load next example
    if len(examples) > 0:
        return load_example_at_index(current_index)
    else:
        return "✅ All examples deleted", "", "", "", 0.0, "0/0", None, None


def remove_flagged_examples() -> str:
    """Remove all flagged examples from dataset"""
    global current_dataset, current_index

    if not current_dataset or 'examples' not in current_dataset:
        return "❌ No dataset loaded"

    examples = current_dataset['examples']
    original_count = len(examples)

    # Remove flagged
    current_dataset['examples'] = [ex for ex in examples if not ex.get('flagged', False)]

    removed_count = original_count - len(current_dataset['examples'])

    # Reset index
    current_index = 0

    logger.info(f"Removed {removed_count} flagged examples")

    return f"✅ Removed {removed_count} flagged examples ({len(current_dataset['examples'])} remaining)"


def save_reviewed_dataset(dataset_name: str) -> str:
    """Save the reviewed dataset"""
    global current_dataset

    if not current_dataset:
        return "❌ No dataset loaded"

    if not dataset_name:
        return "❌ Please provide a dataset name"

    try:
        # Update metadata
        if 'metadata' not in current_dataset:
            current_dataset['metadata'] = {}

        current_dataset['metadata']['reviewed'] = True
        current_dataset['metadata']['total_examples'] = len(current_dataset['examples'])

        # Save
        output_path = dataset_tools.save_dataset(current_dataset, dataset_name, validate=True)

        logger.info(f"Saved reviewed dataset: {output_path}")

        return f"✅ Saved reviewed dataset to: {output_path.name}"

    except Exception as e:
        logger.error(f"Error saving dataset: {str(e)}")
        return f"❌ Error: {str(e)}"


def get_available_datasets() -> List[str]:
    """Get list of available datasets"""
    datasets = dataset_tools.list_datasets()
    return [ds['name'] for ds in datasets]


def create_dataset_review_tab():
    """Create the Dataset Review tab UI"""

    with gr.Column():
        gr.Markdown(
            """
            ## 📝 Dataset Review & Edit

            Load a dataset to review, edit, and improve individual examples.
            """
        )

        # Load dataset section
        with gr.Group():
            gr.Markdown("### 📂 Load Dataset")

            with gr.Row():
                dataset_dropdown = gr.Dropdown(
                    choices=get_available_datasets(),
                    label="Select Dataset",
                    interactive=True
                )

                refresh_btn = gr.Button("🔄 Refresh List", size="sm")
                load_btn = gr.Button("📂 Load Dataset", variant="primary")

            status_text = gr.Textbox(
                label="Status",
                interactive=False,
                lines=1
            )

        # Navigation section
        with gr.Group():
            gr.Markdown("### 🔍 Navigate Examples")

            with gr.Row():
                prev_btn = gr.Button("⬅️ Previous", size="sm")
                position_text = gr.Textbox(
                    label="Position",
                    value="0/0",
                    interactive=False,
                    scale=1
                )
                next_btn = gr.Button("➡️ Next", size="sm")

            example_slider = gr.Slider(
                minimum=0,
                maximum=100,
                step=1,
                label="Jump to Example",
                interactive=True
            )

        # Example editing section
        with gr.Group():
            gr.Markdown("### ✏️ Edit Example")

            instruction_input = gr.Textbox(
                label="Instruction",
                lines=3,
                interactive=True,
                placeholder="The task instruction..."
            )

            input_input = gr.Textbox(
                label="Input",
                lines=4,
                interactive=True,
                placeholder="The input context..."
            )

            output_input = gr.Textbox(
                label="Output",
                lines=8,
                interactive=True,
                placeholder="The expected output..."
            )

            quality_slider = gr.Slider(
                minimum=0.0,
                maximum=1.0,
                step=0.01,
                label="Quality Score",
                interactive=True
            )

        # Action buttons
        with gr.Row():
            save_example_btn = gr.Button("💾 Save Changes", variant="secondary")
            flag_bad_btn = gr.Button("🚩 Flag as Bad", variant="stop")
            flag_good_btn = gr.Button("✅ Mark as Good", variant="secondary")
            delete_btn = gr.Button("🗑️ Delete", variant="stop")

        edit_status = gr.Textbox(
            label="Edit Status",
            interactive=False
        )

        # Batch operations
        with gr.Group():
            gr.Markdown("### 🧹 Batch Operations")

            with gr.Row():
                remove_flagged_btn = gr.Button("🗑️ Remove All Flagged", variant="stop")

                with gr.Column():
                    save_name_input = gr.Textbox(
                        label="Save As",
                        placeholder="reviewed_dataset",
                        interactive=True
                    )
                    save_dataset_btn = gr.Button("💾 Save Dataset", variant="primary")

            batch_status = gr.Textbox(
                label="Batch Status",
                interactive=False
            )

        # Hidden state
        dataset_state = gr.State(None)

        # Event handlers
        refresh_btn.click(
            fn=lambda: gr.update(choices=get_available_datasets()),
            outputs=[dataset_dropdown]
        )

        load_btn.click(
            fn=load_dataset_for_review,
            inputs=[dataset_dropdown],
            outputs=[status_text, instruction_input, input_input, output_input,
                    quality_slider, position_text, example_slider, dataset_state]
        )

        prev_btn.click(
            fn=navigate_previous,
            outputs=[status_text, instruction_input, input_input, output_input,
                    quality_slider, position_text, example_slider, dataset_state]
        )

        next_btn.click(
            fn=navigate_next,
            outputs=[status_text, instruction_input, input_input, output_input,
                    quality_slider, position_text, example_slider, dataset_state]
        )

        example_slider.change(
            fn=load_example_at_index,
            inputs=[example_slider],
            outputs=[status_text, instruction_input, input_input, output_input,
                    quality_slider, position_text, example_slider, dataset_state]
        )

        save_example_btn.click(
            fn=save_current_example,
            inputs=[instruction_input, input_input, output_input, quality_slider],
            outputs=[edit_status]
        )

        flag_bad_btn.click(
            fn=flag_as_bad,
            outputs=[status_text, instruction_input, input_input, output_input,
                    quality_slider, position_text, example_slider, dataset_state]
        )

        flag_good_btn.click(
            fn=flag_as_good,
            outputs=[status_text, instruction_input, input_input, output_input,
                    quality_slider, position_text, example_slider, dataset_state]
        )

        delete_btn.click(
            fn=delete_current_example,
            outputs=[status_text, instruction_input, input_input, output_input,
                    quality_slider, position_text, example_slider, dataset_state]
        )

        remove_flagged_btn.click(
            fn=remove_flagged_examples,
            outputs=[batch_status]
        )

        save_dataset_btn.click(
            fn=save_reviewed_dataset,
            inputs=[save_name_input],
            outputs=[batch_status]
        )
