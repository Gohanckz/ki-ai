"""
Testing System Tab - Test and compare trained agents
"""

import gradio as gr
from typing import List

from backend.testing.agent_tester import AgentTester
from backend.training.lora_trainer import LoRATrainer
from backend.utils.logger import setup_logger

logger = setup_logger("ki.frontend.testing_system")

# Initialize tools
tester = AgentTester()
trainer = LoRATrainer()

# Global state
current_test_cases: List = []
current_comparison: dict = {}


def get_available_models():
    """Get list of trained models"""
    models = trainer.list_trained_models()
    model_names = [m['name'] for m in models]

    # Add base model option
    return ["llama3.1 (base)"] + model_names


def generate_test_cases_ui(category: str, num_cases: int) -> tuple:
    """Generate test cases"""
    global current_test_cases

    if not category:
        return "❌ Select a category", []

    try:
        current_test_cases = tester.generate_test_cases(category, num_cases)

        # Format for display
        display_data = []
        for tc in current_test_cases:
            display_data.append({
                "ID": tc['id'],
                "Instruction": tc['instruction'][:50] + "...",
                "Input": tc['input'][:50] + "..."
            })

        status = f"✅ Generated {len(current_test_cases)} test cases for {category}"

        return status, display_data

    except Exception as e:
        logger.error(f"Error generating test cases: {str(e)}")
        return f"❌ Error: {str(e)}", []


def run_single_test(test_index: int, model_name: str, progress=gr.Progress()) -> str:
    """Run a single test case"""
    global current_test_cases

    if not current_test_cases:
        return "❌ Generate test cases first"

    if test_index >= len(current_test_cases):
        return "❌ Invalid test index"

    test_case = current_test_cases[test_index]

    # Get model identifier
    model = "llama3.1" if "base" in model_name.lower() else model_name

    progress(0.5, desc="Running test...")

    result = tester.run_test_case(test_case, model)

    progress(1.0, desc="Complete!")

    # Format result
    output = f"""
## Test Result: {result['test_case_id']}

**Category:** {result['category']}

**Instruction:** {result['instruction']}

**Input:** {result['input']}

---

**Output:**

{result['output']}

---

**Analysis:**
- Length: {result['analysis']['length']} characters
- Word count: {result['analysis']['word_count']}
- Topics mentioned: {result['analysis']['mentions_expected_topics']}
- Quality score: {result['analysis']['quality_score']:.2%}
"""

    return output


def compare_models_ui(
    model_a_name: str,
    model_b_name: str,
    progress=gr.Progress()
) -> tuple:
    """Compare two models"""
    global current_test_cases, current_comparison

    if not current_test_cases:
        return "❌ Generate test cases first", ""

    if not model_a_name or not model_b_name:
        return "❌ Select both models", ""

    try:
        # Get model identifiers
        model_a = "llama3.1" if "base" in model_a_name.lower() else model_a_name
        model_b = "llama3.1" if "base" in model_b_name.lower() else model_b_name

        progress(0.1, desc="Starting comparison...")

        # Run comparison
        current_comparison = tester.compare_models(
            test_cases=current_test_cases,
            model_a=model_a,
            model_b=model_b,
            model_a_name=model_a_name,
            model_b_name=model_b_name
        )

        progress(1.0, desc="Complete!")

        # Generate report
        report = tester.generate_comparison_report(current_comparison)

        # Format detailed results
        details = "## Detailed Results\n\n"

        # Model A results
        details += f"### {model_a_name} Results:\n\n"
        for result in current_comparison['model_a']['results'][:3]:  # Show first 3
            details += f"**Test {result['test_case_id']}:**\n"
            details += f"- Quality: {result['analysis']['quality_score']:.2%}\n"
            details += f"- Output: {result['output'][:200]}...\n\n"

        # Model B results
        if 'model_b' in current_comparison:
            details += f"### {model_b_name} Results:\n\n"
            for result in current_comparison['model_b']['results'][:3]:
                details += f"**Test {result['test_case_id']}:**\n"
                details += f"- Quality: {result['analysis']['quality_score']:.2%}\n"
                details += f"- Output: {result['output'][:200]}...\n\n"

        return report, details

    except Exception as e:
        logger.error(f"Comparison error: {str(e)}")
        return f"❌ Error: {str(e)}", ""


def list_past_comparisons() -> str:
    """List past test results"""

    results = tester.list_test_results()

    if not results:
        return "No past comparisons found."

    output = ["## 📋 Past Comparisons", ""]

    for result in results[:10]:  # Show last 10
        output.append(f"### {result['filename']}")
        output.append(f"- **Timestamp:** {result['timestamp']}")
        output.append(f"- **Model A:** {result['model_a']}")
        output.append(f"- **Model B:** {result['model_b']}")
        output.append(f"- **Path:** `{result['path']}`")
        output.append("")

    return "\n".join(output)


def create_testing_system_tab():
    """Create the Testing System tab UI"""

    with gr.Column():
        gr.Markdown(
            """
            ## 🧪 Testing System

            Test and compare your trained models against base models.
            """
        )

        # Generate Test Cases
        with gr.Group():
            gr.Markdown("### 📝 Generate Test Cases")

            with gr.Row():
                category_dropdown = gr.Dropdown(
                    choices=["SSRF", "XSS", "SQLi", "IDOR", "RCE", "XXE", "CSRF"],
                    label="Category",
                    value="SSRF",
                    interactive=True
                )

                num_cases_slider = gr.Slider(
                    minimum=1,
                    maximum=20,
                    value=5,
                    step=1,
                    label="Number of Test Cases",
                    interactive=True
                )

                generate_cases_btn = gr.Button("🎲 Generate Cases", variant="primary")

            test_cases_status = gr.Textbox(
                label="Status",
                interactive=False
            )

            test_cases_table = gr.DataFrame(
                headers=["ID", "Instruction", "Input"],
                label="Test Cases",
                interactive=False
            )

        # Single Test
        with gr.Group():
            gr.Markdown("### 🔍 Run Single Test")

            with gr.Row():
                test_index_slider = gr.Slider(
                    minimum=0,
                    maximum=10,
                    value=0,
                    step=1,
                    label="Test Case Index",
                    interactive=True
                )

                single_model_dropdown = gr.Dropdown(
                    choices=get_available_models(),
                    label="Model to Test",
                    interactive=True
                )

                run_single_btn = gr.Button("▶️ Run Test", variant="secondary")

            single_test_output = gr.Markdown(
                label="Test Result",
                value="Configure and run a test"
            )

        # Model Comparison
        with gr.Group():
            gr.Markdown("### 📊 Compare Models")

            with gr.Row():
                model_a_dropdown = gr.Dropdown(
                    choices=get_available_models(),
                    label="Model A (Base)",
                    value="llama3.1 (base)",
                    interactive=True
                )

                model_b_dropdown = gr.Dropdown(
                    choices=get_available_models(),
                    label="Model B (Fine-tuned)",
                    interactive=True
                )

            compare_btn = gr.Button("🔬 Compare Models", variant="primary", size="lg")

            with gr.Row():
                with gr.Column(scale=1):
                    comparison_report = gr.Markdown(
                        label="Comparison Report",
                        value="Generate test cases and compare models"
                    )

                with gr.Column(scale=1):
                    comparison_details = gr.Markdown(
                        label="Detailed Results",
                        value=""
                    )

        # Past Comparisons
        with gr.Group():
            gr.Markdown("### 📚 Past Comparisons")

            refresh_comparisons_btn = gr.Button("🔄 Refresh List", size="sm")

            past_comparisons_list = gr.Markdown(
                value=list_past_comparisons()
            )

        # Help
        with gr.Accordion("ℹ️ Testing Help", open=False):
            gr.Markdown(
                """
                **How Testing Works:**

                1. **Generate Test Cases:** Create evaluation prompts for a category
                2. **Run Single Test:** Test one model on one test case
                3. **Compare Models:** Run all test cases on two models and compare

                **Quality Score:**
                - Based on response length, topic coverage, and format
                - Range: 0.0 to 1.0 (0% to 100%)
                - Higher is better

                **Interpretation:**
                - If fine-tuned model scores higher → training worked!
                - If base model scores higher → more training data needed
                - Similar scores → models are comparable
                """
            )

        # Event handlers
        generate_cases_btn.click(
            fn=generate_test_cases_ui,
            inputs=[category_dropdown, num_cases_slider],
            outputs=[test_cases_status, test_cases_table]
        )

        run_single_btn.click(
            fn=run_single_test,
            inputs=[test_index_slider, single_model_dropdown],
            outputs=[single_test_output]
        )

        compare_btn.click(
            fn=compare_models_ui,
            inputs=[model_a_dropdown, model_b_dropdown],
            outputs=[comparison_report, comparison_details]
        )

        refresh_comparisons_btn.click(
            fn=list_past_comparisons,
            outputs=[past_comparisons_list]
        )
