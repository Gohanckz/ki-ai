#!/usr/bin/env python3
"""
Dataset Management CLI Tool
"""

import sys
from pathlib import Path
import argparse

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.core.dataset_tools import DatasetTools
from backend.utils.logger import setup_logger

logger = setup_logger("ki.tools.dataset_cli")


def main():
    parser = argparse.ArgumentParser(
        description="KI Dataset Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all datasets
  python tools/dataset_cli.py list

  # Merge datasets
  python tools/dataset_cli.py merge ssrf_v1.json ssrf_v2.json -o ssrf_final

  # Deduplicate a dataset
  python tools/dataset_cli.py dedupe ssrf_v1.json -o ssrf_v1_clean

  # Validate a dataset
  python tools/dataset_cli.py validate ssrf_v1.json

  # Filter by quality
  python tools/dataset_cli.py filter ssrf_v1.json --min-quality 0.7 -o ssrf_high_quality
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # List command
    list_parser = subparsers.add_parser('list', help='List all datasets')

    # Merge command
    merge_parser = subparsers.add_parser('merge', help='Merge multiple datasets')
    merge_parser.add_argument('datasets', nargs='+', help='Dataset files to merge')
    merge_parser.add_argument('-o', '--output', required=True, help='Output dataset name')
    merge_parser.add_argument('--no-dedupe', action='store_true', help='Skip deduplication')

    # Deduplicate command
    dedupe_parser = subparsers.add_parser('dedupe', help='Remove duplicates from dataset')
    dedupe_parser.add_argument('dataset', help='Dataset file')
    dedupe_parser.add_argument('-o', '--output', required=True, help='Output dataset name')
    dedupe_parser.add_argument('-t', '--threshold', type=float, default=0.85,
                              help='Similarity threshold (0-1)')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate dataset')
    validate_parser.add_argument('dataset', help='Dataset file')

    # Filter command
    filter_parser = subparsers.add_parser('filter', help='Filter examples by quality')
    filter_parser.add_argument('dataset', help='Dataset file')
    filter_parser.add_argument('--min-quality', type=float, default=0.6,
                              help='Minimum quality score')
    filter_parser.add_argument('-o', '--output', required=True, help='Output dataset name')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize tools
    tools = DatasetTools()

    # Execute command
    if args.command == 'list':
        cmd_list(tools)

    elif args.command == 'merge':
        cmd_merge(tools, args)

    elif args.command == 'dedupe':
        cmd_dedupe(tools, args)

    elif args.command == 'validate':
        cmd_validate(tools, args)

    elif args.command == 'filter':
        cmd_filter(tools, args)


def cmd_list(tools: DatasetTools):
    """List all datasets"""
    print("\n📚 Available Datasets:")
    print("=" * 80)

    datasets = tools.list_datasets()

    if not datasets:
        print("No datasets found.")
        return

    for ds in datasets:
        print(f"\n📁 {ds['name']}")
        print(f"   Category: {ds['category']}")
        print(f"   Examples: {ds['examples']}")
        print(f"   Created: {ds['created_at']}")
        print(f"   Path: {ds['path']}")

    print("\n" + "=" * 80)
    print(f"Total: {len(datasets)} datasets\n")


def cmd_merge(tools: DatasetTools, args):
    """Merge multiple datasets"""
    print(f"\n🔄 Merging {len(args.datasets)} datasets...")

    # Resolve paths
    dataset_paths = []
    for ds_name in args.datasets:
        path = tools.datasets_path / ds_name
        if not path.exists():
            print(f"❌ Dataset not found: {ds_name}")
            return
        dataset_paths.append(path)

    # Merge
    merged = tools.merge_datasets(
        dataset_paths=dataset_paths,
        output_name=args.output,
        deduplicate=not args.no_dedupe
    )

    # Save
    output_path = tools.save_dataset(merged, args.output)

    print(f"\n✅ Merged dataset saved: {output_path}")
    print(f"   Total examples: {len(merged['examples'])}")
    print(f"   Duplicates removed: {merged['metadata']['duplicates_removed']}")


def cmd_dedupe(tools: DatasetTools, args):
    """Deduplicate dataset"""
    print(f"\n🔍 Deduplicating dataset: {args.dataset}")

    # Load dataset
    dataset_path = tools.datasets_path / args.dataset
    if not dataset_path.exists():
        print(f"❌ Dataset not found: {args.dataset}")
        return

    dataset = tools.load_dataset(dataset_path)

    # Deduplicate
    original_count = len(dataset['examples'])
    dataset['examples'] = tools.deduplicate_examples(
        dataset['examples'],
        similarity_threshold=args.threshold
    )

    duplicates_removed = original_count - len(dataset['examples'])

    # Update metadata
    dataset['metadata']['deduplicated'] = True
    dataset['metadata']['duplicates_removed'] = duplicates_removed

    # Save
    output_path = tools.save_dataset(dataset, args.output)

    print(f"\n✅ Deduplicated dataset saved: {output_path}")
    print(f"   Original: {original_count} examples")
    print(f"   After deduplication: {len(dataset['examples'])} examples")
    print(f"   Removed: {duplicates_removed} duplicates")


def cmd_validate(tools: DatasetTools, args):
    """Validate dataset"""
    print(f"\n✓ Validating dataset: {args.dataset}")

    # Load dataset
    dataset_path = tools.datasets_path / args.dataset
    if not dataset_path.exists():
        print(f"❌ Dataset not found: {args.dataset}")
        return

    dataset = tools.load_dataset(dataset_path)

    # Validate
    report = tools.validate_dataset(dataset)

    print("\n📊 Validation Report:")
    print("=" * 80)

    if report['valid']:
        print("✅ Dataset is VALID")
    else:
        print("❌ Dataset has ERRORS")

    print(f"\nStatistics:")
    for key, value in report['stats'].items():
        print(f"  • {key}: {value}")

    if report['errors']:
        print(f"\n❌ Errors ({len(report['errors'])}):")
        for error in report['errors']:
            print(f"  • {error}")

    if report['warnings']:
        print(f"\n⚠️  Warnings ({len(report['warnings'])}):")
        for i, warning in enumerate(report['warnings'][:10]):  # Show first 10
            print(f"  • {warning}")
        if len(report['warnings']) > 10:
            print(f"  ... and {len(report['warnings']) - 10} more warnings")

    print("=" * 80 + "\n")


def cmd_filter(tools: DatasetTools, args):
    """Filter examples by quality"""
    print(f"\n🔍 Filtering dataset by quality (min: {args.min_quality})")

    # Load dataset
    dataset_path = tools.datasets_path / args.dataset
    if not dataset_path.exists():
        print(f"❌ Dataset not found: {args.dataset}")
        return

    dataset = tools.load_dataset(dataset_path)

    # Filter
    original_count = len(dataset['examples'])
    dataset['examples'] = tools.filter_examples_by_quality(
        dataset['examples'],
        min_quality=args.min_quality
    )

    # Update metadata
    dataset['metadata']['filtered'] = True
    dataset['metadata']['min_quality'] = args.min_quality
    dataset['metadata']['filtered_out'] = original_count - len(dataset['examples'])

    # Save
    output_path = tools.save_dataset(dataset, args.output)

    print(f"\n✅ Filtered dataset saved: {output_path}")
    print(f"   Original: {original_count} examples")
    print(f"   After filtering: {len(dataset['examples'])} examples")
    print(f"   Filtered out: {original_count - len(dataset['examples'])} examples")


if __name__ == '__main__':
    main()
