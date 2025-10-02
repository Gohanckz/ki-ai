"""
Agent Testing Module - Test and compare trained agents
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from backend.training.lora_trainer import LoRATrainer
from backend.clients.ollama_client import OllamaClient
from backend.utils.logger import setup_logger
from backend.utils.config import settings

logger = setup_logger("ki.testing.agent_tester")


class AgentTester:
    """Test and compare trained agents"""

    def __init__(self):
        self.trainer = LoRATrainer()
        self.ollama = OllamaClient()
        self.test_results_path = settings.storage_path / "test_results"
        self.test_results_path.mkdir(parents=True, exist_ok=True)

        logger.info("Initialized AgentTester")

    def generate_test_cases(self, category: str, num_cases: int = 5) -> List[Dict]:
        """
        Generate test cases for a specific category

        Args:
            category: Vulnerability category
            num_cases: Number of test cases to generate

        Returns:
            List of test case dictionaries
        """
        logger.info(f"Generating {num_cases} test cases for {category}")

        # Predefined test cases for common categories
        test_cases_templates = {
            "SSRF": [
                {
                    "instruction": "Explain how to identify SSRF vulnerabilities in cloud environments",
                    "input": "I'm testing an AWS Lambda function that makes HTTP requests",
                    "expected_topics": ["SSRF", "AWS", "Lambda", "metadata", "IMDSv2"]
                },
                {
                    "instruction": "Describe mitigation strategies for SSRF attacks",
                    "input": "Our API allows users to provide URLs for image processing",
                    "expected_topics": ["whitelist", "validation", "network segmentation"]
                },
                {
                    "instruction": "What are the risks of SSRF in microservices?",
                    "input": "We have a service mesh with internal APIs",
                    "expected_topics": ["internal network", "service discovery", "lateral movement"]
                }
            ],
            "XSS": [
                {
                    "instruction": "Explain DOM-based XSS vulnerabilities",
                    "input": "Our JavaScript app uses window.location.hash",
                    "expected_topics": ["DOM", "XSS", "client-side", "sanitization"]
                },
                {
                    "instruction": "How to prevent XSS in React applications?",
                    "input": "We're building a dashboard with user-generated content",
                    "expected_topics": ["React", "JSX", "escaping", "Content Security Policy"]
                }
            ],
            "SQLi": [
                {
                    "instruction": "Identify SQL injection attack vectors",
                    "input": "Our login form uses string concatenation for queries",
                    "expected_topics": ["SQL injection", "prepared statements", "parameterized queries"]
                },
                {
                    "instruction": "Explain blind SQL injection techniques",
                    "input": "The application doesn't show error messages",
                    "expected_topics": ["blind SQLi", "boolean-based", "time-based"]
                }
            ]
        }

        # Get test cases for category
        templates = test_cases_templates.get(category, [])

        if not templates:
            logger.warning(f"No templates for {category}, generating generic tests")
            templates = [
                {
                    "instruction": f"Explain {category} vulnerabilities",
                    "input": "Provide a technical overview",
                    "expected_topics": [category.lower(), "security", "vulnerability"]
                }
            ]

        # Cycle through templates if we need more cases
        test_cases = []
        for i in range(num_cases):
            template = templates[i % len(templates)]
            test_case = {
                "id": f"test_{category}_{i+1}",
                "category": category,
                "instruction": template['instruction'],
                "input": template['input'],
                "expected_topics": template.get('expected_topics', [])
            }
            test_cases.append(test_case)

        logger.info(f"Generated {len(test_cases)} test cases")

        return test_cases

    def run_test_case(self, test_case: Dict, model: str = "llama3.1") -> Dict:
        """
        Run a single test case

        Args:
            test_case: Test case dictionary
            model: Model to test (Ollama model name or path to trained model)

        Returns:
            Test result dictionary
        """
        logger.info(f"Running test case: {test_case['id']}")

        # Construct prompt
        prompt = f"""Instruction: {test_case['instruction']}

Input: {test_case['input']}

Output:"""

        # Generate response
        if self.ollama.is_available():
            try:
                response = self.ollama.generate(
                    prompt=prompt,
                    model=model,
                    temperature=0.7,
                    max_tokens=512
                )

                output = response.strip()

            except Exception as e:
                logger.error(f"Error generating response: {str(e)}")
                output = f"[ERROR: {str(e)}]"
        else:
            output = "[Ollama not available - simulation mode]"

        # Analyze response
        analysis = self._analyze_response(output, test_case)

        result = {
            "test_case_id": test_case['id'],
            "category": test_case['category'],
            "instruction": test_case['instruction'],
            "input": test_case['input'],
            "output": output,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }

        return result

    def _analyze_response(self, output: str, test_case: Dict) -> Dict:
        """Analyze test response quality"""

        analysis = {
            "length": len(output),
            "word_count": len(output.split()),
            "mentions_expected_topics": 0,
            "quality_score": 0.0
        }

        # Check for expected topics
        expected = test_case.get('expected_topics', [])
        output_lower = output.lower()

        for topic in expected:
            if topic.lower() in output_lower:
                analysis['mentions_expected_topics'] += 1

        # Calculate quality score
        score = 0.0

        # Length score (30%)
        if analysis['word_count'] > 100:
            score += 0.3
        elif analysis['word_count'] > 50:
            score += 0.15

        # Topic coverage (50%)
        if expected:
            topic_coverage = analysis['mentions_expected_topics'] / len(expected)
            score += topic_coverage * 0.5

        # No error (20%)
        if "[ERROR" not in output:
            score += 0.2

        analysis['quality_score'] = min(score, 1.0)

        return analysis

    def compare_models(
        self,
        test_cases: List[Dict],
        model_a: str = "llama3.1",
        model_b: Optional[str] = None,
        model_a_name: str = "Base Model",
        model_b_name: str = "Fine-tuned Model"
    ) -> Dict:
        """
        Compare two models on test cases

        Args:
            test_cases: List of test cases
            model_a: First model identifier
            model_b: Second model identifier (optional)
            model_a_name: Display name for model A
            model_b_name: Display name for model B

        Returns:
            Comparison results
        """
        logger.info(f"Comparing models: {model_a_name} vs {model_b_name}")

        results_a = []
        results_b = []

        # Run tests on model A
        for test_case in test_cases:
            result = self.run_test_case(test_case, model_a)
            results_a.append(result)

        # Run tests on model B (if provided)
        if model_b:
            for test_case in test_cases:
                result = self.run_test_case(test_case, model_b)
                results_b.append(result)

        # Calculate metrics
        metrics_a = self._calculate_metrics(results_a)
        metrics_b = self._calculate_metrics(results_b) if model_b else None

        comparison = {
            "timestamp": datetime.now().isoformat(),
            "model_a": {
                "name": model_a_name,
                "identifier": model_a,
                "results": results_a,
                "metrics": metrics_a
            }
        }

        if model_b:
            comparison["model_b"] = {
                "name": model_b_name,
                "identifier": model_b,
                "results": results_b,
                "metrics": metrics_b
            }

        # Save comparison
        self._save_comparison(comparison)

        logger.info(f"✅ Comparison completed: {len(test_cases)} test cases")

        return comparison

    def _calculate_metrics(self, results: List[Dict]) -> Dict:
        """Calculate aggregate metrics from results"""

        if not results:
            return {}

        total_score = sum(r['analysis']['quality_score'] for r in results)
        avg_score = total_score / len(results)

        total_length = sum(r['analysis']['length'] for r in results)
        avg_length = total_length / len(results)

        total_words = sum(r['analysis']['word_count'] for r in results)
        avg_words = total_words / len(results)

        total_topics = sum(r['analysis']['mentions_expected_topics'] for r in results)

        return {
            "total_tests": len(results),
            "average_quality_score": avg_score,
            "average_length": avg_length,
            "average_word_count": avg_words,
            "total_topics_mentioned": total_topics
        }

    def _save_comparison(self, comparison: Dict):
        """Save comparison results to file"""

        filename = f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_path = self.test_results_path / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(comparison, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved comparison to: {output_path}")

    def list_test_results(self) -> List[Dict]:
        """List all saved test results"""

        results = []

        for result_file in self.test_results_path.glob("comparison_*.json"):
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                results.append({
                    "filename": result_file.name,
                    "path": str(result_file),
                    "timestamp": data.get('timestamp', 'Unknown'),
                    "model_a": data.get('model_a', {}).get('name', 'Unknown'),
                    "model_b": data.get('model_b', {}).get('name', 'N/A')
                })

            except Exception as e:
                logger.warning(f"Could not read {result_file.name}: {str(e)}")

        return sorted(results, key=lambda x: x['timestamp'], reverse=True)

    def generate_comparison_report(self, comparison: Dict) -> str:
        """Generate a markdown report from comparison"""

        report = ["# 🧪 Model Comparison Report", ""]

        # Model A
        model_a = comparison['model_a']
        report.append(f"## Model A: {model_a['name']}")
        report.append("")
        report.append("### Metrics:")
        metrics_a = model_a['metrics']
        report.append(f"- **Average Quality Score:** {metrics_a['average_quality_score']:.2%}")
        report.append(f"- **Average Word Count:** {metrics_a['average_word_count']:.0f}")
        report.append(f"- **Total Tests:** {metrics_a['total_tests']}")
        report.append("")

        # Model B (if exists)
        if 'model_b' in comparison:
            model_b = comparison['model_b']
            report.append(f"## Model B: {model_b['name']}")
            report.append("")
            report.append("### Metrics:")
            metrics_b = model_b['metrics']
            report.append(f"- **Average Quality Score:** {metrics_b['average_quality_score']:.2%}")
            report.append(f"- **Average Word Count:** {metrics_b['average_word_count']:.0f}")
            report.append(f"- **Total Tests:** {metrics_b['total_tests']}")
            report.append("")

            # Comparison
            report.append("## 📊 Comparison")
            report.append("")

            score_diff = metrics_b['average_quality_score'] - metrics_a['average_quality_score']
            score_pct = (score_diff / metrics_a['average_quality_score']) * 100 if metrics_a['average_quality_score'] > 0 else 0

            if score_diff > 0:
                report.append(f"✅ Model B is **{score_pct:+.1f}%** better in quality score")
            elif score_diff < 0:
                report.append(f"❌ Model B is **{score_pct:.1f}%** worse in quality score")
            else:
                report.append("➖ Both models have equal quality scores")

            report.append("")

        return "\n".join(report)
