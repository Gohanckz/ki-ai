"""
Document Parsers for KI platform

Supports: PDF, DOCX, TXT, Markdown
"""

from pathlib import Path
from typing import Dict, Optional
from .pdf_parser import PDFParser, parse_pdf
from .docx_parser import DOCXParser, parse_docx
from .text_parser import TextParser, parse_text
from .markdown_parser import MarkdownParser, parse_markdown
from ...utils.logger import setup_logger

logger = setup_logger("ki.parsers")


class UniversalParser:
    """
    Universal document parser that automatically detects
    and uses the appropriate parser based on file extension
    """

    def __init__(self):
        self.parsers = {
            "pdf": PDFParser(),
            "docx": DOCXParser(),
            "text": TextParser(),
            "markdown": MarkdownParser()
        }

        # Build extension to parser mapping
        self.extension_map = {}
        for parser_name, parser in self.parsers.items():
            for ext in parser.supported_extensions:
                self.extension_map[ext] = parser_name

    def parse(self, file_path: Path) -> Dict[str, any]:
        """
        Parse document using appropriate parser

        Args:
            file_path: Path to document

        Returns:
            Parsed content dictionary
        """
        file_path = Path(file_path)

        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return {
                "file_name": file_path.name,
                "success": False,
                "error": "File not found",
                "full_text": ""
            }

        ext = file_path.suffix.lower()

        if ext not in self.extension_map:
            logger.error(f"Unsupported file type: {ext}")
            return {
                "file_name": file_path.name,
                "success": False,
                "error": f"Unsupported file type: {ext}",
                "full_text": ""
            }

        parser_name = self.extension_map[ext]
        parser = self.parsers[parser_name]

        logger.info(f"Using {parser_name} parser for {file_path.name}")

        return parser.parse(file_path)

    def is_supported(self, file_path: Path) -> bool:
        """Check if file type is supported"""
        ext = Path(file_path).suffix.lower()
        return ext in self.extension_map

    def get_supported_extensions(self) -> list:
        """Get list of all supported extensions"""
        return list(self.extension_map.keys())


# Global parser instance
universal_parser = UniversalParser()


def parse_document(file_path: Path) -> Dict[str, any]:
    """
    Convenience function to parse any supported document

    Args:
        file_path: Path to document

    Returns:
        Parsed content dictionary
    """
    return universal_parser.parse(file_path)


def is_supported_document(file_path: Path) -> bool:
    """Check if document type is supported"""
    return universal_parser.is_supported(file_path)


def get_supported_extensions() -> list:
    """Get list of supported file extensions"""
    return universal_parser.get_supported_extensions()


__all__ = [
    # Individual parsers
    "PDFParser",
    "DOCXParser",
    "TextParser",
    "MarkdownParser",
    # Convenience functions
    "parse_pdf",
    "parse_docx",
    "parse_text",
    "parse_markdown",
    # Universal parser
    "UniversalParser",
    "universal_parser",
    "parse_document",
    "is_supported_document",
    "get_supported_extensions",
]
