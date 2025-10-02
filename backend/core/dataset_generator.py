"""
Dataset Generator - Generate training examples from documents using Ollama
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from backend.ml.ollama_client import get_ollama_client
from backend.utils.logger import setup_logger
from backend.utils.config import settings

logger = setup_logger("ki.core.dataset_generator")


class DatasetGenerator:
    """Generate training datasets from parsed documents"""

    def __init__(self, ollama_client=None):
        """
        Initialize dataset generator

        Args:
            ollama_client: Optional Ollama client instance
        """
        self.ollama_client = ollama_client or get_ollama_client()
        self.quality_thresholds = {
            'High': 0.8,
            'Medium': 0.6,
            'Low': 0.4
        }

    def generate_examples_from_document(
        self,
        document_text: str,
        document_name: str,
        category: str,
        num_examples: int = 5,
        quality_level: str = "High",
        temperature: float = 0.7
    ) -> List[Dict]:
        """
        Generate training examples from a single document

        Args:
            document_text: Full text of the document
            document_name: Name of the source document
            category: Vulnerability category (SSRF, XSS, etc.)
            num_examples: Number of examples to generate
            quality_level: Quality threshold (High, Medium, Low)
            temperature: Sampling temperature for generation

        Returns:
            List of example dictionaries
        """
        logger.info(f"Generating {num_examples} examples from {document_name} (category: {category})")

        # Check if Ollama is available
        if not self.ollama_client.is_available():
            logger.warning("Ollama not available, using simulated generation")
            return self._generate_simulated_examples(
                document_name, category, num_examples
            )

        # Create prompt for example generation
        prompt = self._create_generation_prompt(
            document_text, category, num_examples
        )

        try:
            # Generate examples using Ollama
            response = self.ollama_client.generate(
                prompt=prompt,
                temperature=temperature,
                max_tokens=4096
            )

            # Parse JSON response
            examples = self._parse_ollama_response(response, document_name, category)

            # Validate quality
            validated_examples = self._validate_examples(examples, quality_level)

            logger.info(f"✅ Generated {len(validated_examples)} validated examples from {document_name}")

            return validated_examples

        except Exception as e:
            logger.error(f"❌ Error generating examples: {str(e)}")
            # Fallback to simulated generation
            return self._generate_simulated_examples(
                document_name, category, num_examples
            )

    def _create_generation_prompt(
        self,
        document_text: str,
        category: str,
        num_examples: int
    ) -> str:
        """Create prompt for Ollama to generate examples"""

        # Truncate document if too long
        max_text_length = 3000
        if len(document_text) > max_text_length:
            document_text = document_text[:max_text_length] + "..."

        prompt = f"""You are an expert in cybersecurity and bug bounty hunting, specializing in {category} vulnerabilities.

Your task is to generate {num_examples} high-quality training examples for teaching AI agents about {category} vulnerabilities based on the following document.

Document content:
---
{document_text}
---

Generate exactly {num_examples} diverse training examples in JSON format. Each example should follow this structure:

{{
  "instruction": "A clear task instruction or question about {category}",
  "input": "Specific context, scenario, or code snippet related to {category}",
  "output": "Detailed, educational explanation or analysis of the {category} vulnerability"
}}

Requirements:
1. Each example should be unique and cover different aspects of {category}
2. Instructions should be clear and actionable
3. Inputs should provide realistic scenarios or code examples
4. Outputs should be detailed, educational, and technically accurate
5. Focus on practical bug bounty and security testing scenarios
6. Include detection methods, exploitation techniques, and mitigation strategies

Output ONLY a valid JSON array of {num_examples} examples. Do not include any other text.

Example format:
[
  {{
    "instruction": "Identify the SSRF vulnerability in this code",
    "input": "Code snippet showing vulnerable implementation",
    "output": "Detailed explanation of the SSRF vulnerability, how to exploit it, and how to fix it"
  }}
]

Generate {num_examples} examples now:"""

        return prompt

    def _parse_ollama_response(
        self,
        response: str,
        document_name: str,
        category: str
    ) -> List[Dict]:
        """Parse Ollama response into structured examples"""

        try:
            # Try to parse as JSON
            examples = json.loads(response)

            if not isinstance(examples, list):
                logger.warning("Response is not a list, wrapping in array")
                examples = [examples]

            # Add metadata to each example
            for i, example in enumerate(examples):
                example['source'] = document_name
                example['category'] = category
                example['timestamp'] = datetime.now().isoformat()
                example['generated_by'] = 'ollama'
                example['quality_score'] = self._estimate_quality(example)

            return examples

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            logger.debug(f"Response was: {response[:500]}...")

            # Try to extract JSON from response
            return self._extract_json_from_text(response, document_name, category)

    def _extract_json_from_text(
        self,
        text: str,
        document_name: str,
        category: str
    ) -> List[Dict]:
        """Try to extract JSON array from text that may contain extra content"""

        # Look for JSON array
        import re

        # Find content between [ and ]
        json_match = re.search(r'\[.*\]', text, re.DOTALL)

        if json_match:
            try:
                json_str = json_match.group(0)
                examples = json.loads(json_str)

                # Add metadata
                for example in examples:
                    example['source'] = document_name
                    example['category'] = category
                    example['timestamp'] = datetime.now().isoformat()
                    example['generated_by'] = 'ollama'
                    example['quality_score'] = self._estimate_quality(example)

                return examples

            except json.JSONDecodeError:
                logger.error("Could not parse extracted JSON")

        # If all else fails, return empty list
        logger.warning("Could not extract valid JSON from response")
        return []

    def _estimate_quality(self, example: Dict) -> float:
        """Estimate quality score of an example"""

        score = 0.0

        # Check required fields
        required_fields = ['instruction', 'input', 'output']
        if all(field in example for field in required_fields):
            score += 0.3
        else:
            return 0.0  # Missing required fields

        # Check length of output (should be detailed)
        output_length = len(example.get('output', ''))
        if output_length > 200:
            score += 0.3
        elif output_length > 100:
            score += 0.2
        elif output_length > 50:
            score += 0.1

        # Check instruction clarity
        instruction = example.get('instruction', '')
        if len(instruction) > 20 and len(instruction) < 200:
            score += 0.2

        # Check input has context
        input_text = example.get('input', '')
        if len(input_text) > 20:
            score += 0.2

        return min(score, 1.0)

    def _validate_examples(
        self,
        examples: List[Dict],
        quality_level: str
    ) -> List[Dict]:
        """Filter examples based on quality threshold"""

        threshold = self.quality_thresholds.get(quality_level, 0.6)

        validated = []
        rejected = 0

        for example in examples:
            quality_score = example.get('quality_score', 0.0)

            if quality_score >= threshold:
                validated.append(example)
            else:
                rejected += 1
                logger.debug(f"Rejected example (score: {quality_score:.2f} < {threshold})")

        if rejected > 0:
            logger.info(f"⚠️ Rejected {rejected} examples below quality threshold ({quality_level})")

        return validated

    def _generate_simulated_examples(
        self,
        document_name: str,
        category: str,
        num_examples: int
    ) -> List[Dict]:
        """Generate simulated examples when Ollama is not available"""

        logger.info(f"Generating {num_examples} simulated examples (Ollama not available)")

        examples = []

        for i in range(num_examples):
            example = {
                "instruction": f"Analyze this {category} vulnerability scenario (Example {i+1})",
                "input": f"Sample scenario from {document_name} demonstrating {category} vulnerability patterns",
                "output": f"This is a simulated example for {category}. In a real scenario with Ollama running, "
                         f"this would contain detailed analysis of the vulnerability, exploitation techniques, "
                         f"detection methods, and mitigation strategies based on the actual document content.",
                "source": document_name,
                "category": category,
                "timestamp": datetime.now().isoformat(),
                "generated_by": "simulated",
                "quality_score": 0.5
            }
            examples.append(example)

        return examples

    def generate_dataset(
        self,
        parsed_documents: Dict[str, Dict],
        category: str,
        examples_per_doc: int = 5,
        quality_level: str = "High",
        temperature: float = 0.7
    ) -> Dict:
        """
        Generate complete dataset from multiple documents

        Args:
            parsed_documents: Dict of {file_path: parsed_data}
            category: Vulnerability category
            examples_per_doc: Examples to generate per document
            quality_level: Quality threshold
            temperature: Sampling temperature

        Returns:
            Complete dataset dictionary
        """
        logger.info(f"Generating dataset for {len(parsed_documents)} documents")

        all_examples = []
        stats = {
            'total_documents': len(parsed_documents),
            'total_generated': 0,
            'total_validated': 0,
            'total_rejected': 0
        }

        for file_path, doc_data in parsed_documents.items():
            document_name = Path(file_path).name
            document_text = doc_data.get('full_text', '')

            # Generate examples for this document
            examples = self.generate_examples_from_document(
                document_text=document_text,
                document_name=document_name,
                category=category,
                num_examples=examples_per_doc,
                quality_level=quality_level,
                temperature=temperature
            )

            stats['total_generated'] += examples_per_doc
            stats['total_validated'] += len(examples)
            stats['total_rejected'] += (examples_per_doc - len(examples))

            all_examples.extend(examples)

        # Create dataset
        dataset = {
            "metadata": {
                "category": category,
                "created_at": datetime.now().isoformat(),
                "total_examples": len(all_examples),
                "source_documents": stats['total_documents'],
                "examples_per_doc": examples_per_doc,
                "quality_level": quality_level,
                "temperature": temperature,
                "stats": stats,
                "ollama_available": self.ollama_client.is_available()
            },
            "examples": all_examples
        }

        logger.info(f"✅ Dataset generation complete: {len(all_examples)} examples")

        return dataset
