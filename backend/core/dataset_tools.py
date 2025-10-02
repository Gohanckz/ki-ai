"""
Dataset Tools - Merge, deduplicate, and validate datasets
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Optional
from datetime import datetime
from difflib import SequenceMatcher

from backend.utils.logger import setup_logger
from backend.utils.config import settings

logger = setup_logger("ki.core.dataset_tools")


class DatasetTools:
    """Tools for managing and improving datasets"""

    def __init__(self):
        self.datasets_path = settings.datasets_path

    def merge_datasets(
        self,
        dataset_paths: List[Path],
        output_name: str,
        deduplicate: bool = True
    ) -> Dict:
        """
        Merge multiple datasets into one

        Args:
            dataset_paths: List of paths to dataset JSON files
            output_name: Name for the merged dataset
            deduplicate: Whether to remove duplicates

        Returns:
            Merged dataset dictionary
        """
        logger.info(f"Merging {len(dataset_paths)} datasets")

        all_examples = []
        source_datasets = []
        total_examples_before = 0

        # Load all datasets
        for path in dataset_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    dataset = json.load(f)

                examples = dataset.get('examples', [])
                all_examples.extend(examples)
                total_examples_before += len(examples)

                source_datasets.append({
                    'name': path.name,
                    'examples': len(examples),
                    'metadata': dataset.get('metadata', {})
                })

                logger.info(f"Loaded {len(examples)} examples from {path.name}")

            except Exception as e:
                logger.error(f"Error loading {path.name}: {str(e)}")
                continue

        logger.info(f"Total examples before merge: {total_examples_before}")

        # Deduplicate if requested
        if deduplicate:
            all_examples = self.deduplicate_examples(all_examples)
            logger.info(f"After deduplication: {len(all_examples)} examples")

        # Create merged dataset
        merged_dataset = {
            "metadata": {
                "name": output_name,
                "created_at": datetime.now().isoformat(),
                "total_examples": len(all_examples),
                "source_datasets": source_datasets,
                "total_examples_before_merge": total_examples_before,
                "duplicates_removed": total_examples_before - len(all_examples),
                "merge_info": {
                    "deduplicated": deduplicate,
                    "merged_from": len(dataset_paths)
                }
            },
            "examples": all_examples
        }

        logger.info(f"✅ Merged dataset created: {len(all_examples)} examples")

        return merged_dataset

    def deduplicate_examples(
        self,
        examples: List[Dict],
        similarity_threshold: float = 0.85
    ) -> List[Dict]:
        """
        Remove duplicate examples based on similarity

        Args:
            examples: List of example dictionaries
            similarity_threshold: Similarity threshold (0-1) for considering duplicates

        Returns:
            Deduplicated list of examples
        """
        logger.info(f"Deduplicating {len(examples)} examples (threshold: {similarity_threshold})")

        if not examples:
            return []

        # Track seen content hashes
        seen_hashes: Set[str] = set()
        seen_contents: List[Dict] = []
        unique_examples: List[Dict] = []
        duplicates_removed = 0

        for example in examples:
            # Create content hash
            content_str = f"{example.get('instruction', '')}{example.get('input', '')}{example.get('output', '')}"
            content_hash = hashlib.md5(content_str.encode()).hexdigest()

            # Check exact duplicates first
            if content_hash in seen_hashes:
                duplicates_removed += 1
                logger.debug(f"Removed exact duplicate (hash: {content_hash[:8]}...)")
                continue

            # Check similarity with existing examples
            is_duplicate = False

            for seen in seen_contents:
                similarity = self._calculate_similarity(example, seen)

                if similarity >= similarity_threshold:
                    duplicates_removed += 1
                    logger.debug(f"Removed similar duplicate (similarity: {similarity:.2f})")
                    is_duplicate = True
                    break

            if not is_duplicate:
                seen_hashes.add(content_hash)
                seen_contents.append(example)
                unique_examples.append(example)

        logger.info(f"✅ Removed {duplicates_removed} duplicates ({len(unique_examples)} unique examples remaining)")

        return unique_examples

    def _calculate_similarity(self, example1: Dict, example2: Dict) -> float:
        """Calculate similarity between two examples"""

        # Compare instruction, input, and output
        inst_sim = SequenceMatcher(
            None,
            example1.get('instruction', ''),
            example2.get('instruction', '')
        ).ratio()

        input_sim = SequenceMatcher(
            None,
            example1.get('input', ''),
            example2.get('input', '')
        ).ratio()

        output_sim = SequenceMatcher(
            None,
            example1.get('output', ''),
            example2.get('output', '')
        ).ratio()

        # Weighted average (output is most important)
        similarity = (inst_sim * 0.2 + input_sim * 0.3 + output_sim * 0.5)

        return similarity

    def validate_dataset(self, dataset: Dict) -> Dict:
        """
        Validate dataset structure and quality

        Args:
            dataset: Dataset dictionary

        Returns:
            Validation report
        """
        logger.info("Validating dataset")

        report = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "stats": {}
        }

        # Check structure
        if 'examples' not in dataset:
            report['valid'] = False
            report['errors'].append("Missing 'examples' key in dataset")
            return report

        examples = dataset['examples']

        # Stats
        report['stats'] = {
            "total_examples": len(examples),
            "missing_fields": 0,
            "short_outputs": 0,
            "low_quality": 0
        }

        # Validate each example
        required_fields = ['instruction', 'input', 'output']

        for i, example in enumerate(examples):
            # Check required fields
            missing = [field for field in required_fields if field not in example]
            if missing:
                report['stats']['missing_fields'] += 1
                report['warnings'].append(f"Example {i}: Missing fields {missing}")

            # Check output length
            output = example.get('output', '')
            if len(output) < 50:
                report['stats']['short_outputs'] += 1
                report['warnings'].append(f"Example {i}: Output too short ({len(output)} chars)")

            # Check quality score if available
            quality = example.get('quality_score', 1.0)
            if quality < 0.5:
                report['stats']['low_quality'] += 1
                report['warnings'].append(f"Example {i}: Low quality score ({quality:.2f})")

        # Overall validation
        if report['stats']['missing_fields'] > len(examples) * 0.1:
            report['errors'].append(f"Too many examples with missing fields ({report['stats']['missing_fields']})")
            report['valid'] = False

        if report['valid']:
            logger.info(f"✅ Dataset is valid ({len(examples)} examples)")
        else:
            logger.warning(f"⚠️ Dataset has validation errors")

        return report

    def save_dataset(self, dataset: Dict, name: str, validate: bool = True) -> Path:
        """
        Save dataset to JSON file

        Args:
            dataset: Dataset dictionary
            name: Name for the dataset file
            validate: Whether to validate before saving

        Returns:
            Path to saved file
        """
        # Validate if requested
        if validate:
            report = self.validate_dataset(dataset)
            if not report['valid']:
                logger.warning("Dataset has validation errors but saving anyway")
                logger.warning(f"Errors: {report['errors']}")

        # Clean filename
        clean_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
        if not clean_name:
            clean_name = f"dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Save to file
        output_path = self.datasets_path / f"{clean_name}.json"

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)

        logger.info(f"✅ Dataset saved to: {output_path}")

        return output_path

    def load_dataset(self, path: Path) -> Dict:
        """Load dataset from JSON file"""

        try:
            with open(path, 'r', encoding='utf-8') as f:
                dataset = json.load(f)

            logger.info(f"Loaded dataset: {path.name} ({len(dataset.get('examples', []))} examples)")

            return dataset

        except Exception as e:
            logger.error(f"Error loading dataset {path.name}: {str(e)}")
            raise

    def list_datasets(self) -> List[Dict]:
        """List all available datasets"""

        datasets = []

        for json_file in self.datasets_path.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    dataset = json.load(f)

                metadata = dataset.get('metadata', {})

                datasets.append({
                    'name': json_file.name,
                    'path': str(json_file),
                    'examples': len(dataset.get('examples', [])),
                    'category': metadata.get('category', 'Unknown'),
                    'created_at': metadata.get('created_at', 'Unknown')
                })

            except Exception as e:
                logger.warning(f"Could not read {json_file.name}: {str(e)}")
                continue

        logger.info(f"Found {len(datasets)} datasets")

        return datasets

    def filter_examples_by_quality(
        self,
        examples: List[Dict],
        min_quality: float = 0.6
    ) -> List[Dict]:
        """Filter examples by minimum quality score"""

        filtered = [
            ex for ex in examples
            if ex.get('quality_score', 0.0) >= min_quality
        ]

        logger.info(f"Filtered {len(examples)} → {len(filtered)} examples (min quality: {min_quality})")

        return filtered

    def balance_dataset(
        self,
        dataset: Dict,
        max_per_category: Optional[int] = None
    ) -> Dict:
        """Balance dataset by limiting examples per category"""

        examples = dataset.get('examples', [])

        # Group by category
        by_category = {}
        for ex in examples:
            category = ex.get('category', 'unknown')
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(ex)

        # Balance
        balanced = []

        for category, cat_examples in by_category.items():
            if max_per_category and len(cat_examples) > max_per_category:
                # Sort by quality and take top N
                sorted_examples = sorted(
                    cat_examples,
                    key=lambda x: x.get('quality_score', 0.0),
                    reverse=True
                )
                balanced.extend(sorted_examples[:max_per_category])
                logger.info(f"Balanced {category}: {len(cat_examples)} → {max_per_category}")
            else:
                balanced.extend(cat_examples)

        # Create balanced dataset
        balanced_dataset = dataset.copy()
        balanced_dataset['examples'] = balanced
        balanced_dataset['metadata']['balanced'] = True
        balanced_dataset['metadata']['max_per_category'] = max_per_category

        logger.info(f"✅ Dataset balanced: {len(examples)} → {len(balanced)} examples")

        return balanced_dataset
