"""
Text Parser for plain text files
"""

from pathlib import Path
from typing import Dict
from ...utils.logger import setup_logger

logger = setup_logger("ki.parsers.text")


class TextParser:
    """Parser for plain text files"""

    def __init__(self):
        self.supported_extensions = [".txt", ".text", ".log"]

    def parse(self, file_path: Path) -> Dict[str, any]:
        """
        Parse text file

        Args:
            file_path: Path to text file

        Returns:
            Dictionary with parsed content
        """
        try:
            logger.info(f"Parsing text file: {file_path.name}")

            # Try multiple encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
            text = None
            used_encoding = None

            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        text = f.read()
                    used_encoding = encoding
                    break
                except UnicodeDecodeError:
                    continue

            if text is None:
                raise Exception("Could not decode file with any supported encoding")

            # Split into lines
            lines = text.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]

            result = {
                "file_name": file_path.name,
                "file_path": str(file_path),
                "file_type": "text",
                "encoding": used_encoding,
                "total_lines": len(lines),
                "non_empty_lines": len(non_empty_lines),
                "full_text": text,
                "char_count": len(text),
                "word_count": len(text.split()),
                "success": True,
                "error": None
            }

            logger.info(f"✅ Parsed {len(lines)} lines, {result['word_count']} words (encoding: {used_encoding})")

            return result

        except Exception as e:
            logger.error(f"❌ Error parsing text file {file_path.name}: {str(e)}")
            return {
                "file_name": file_path.name,
                "file_path": str(file_path),
                "file_type": "text",
                "success": False,
                "error": str(e),
                "full_text": ""
            }

    def is_supported(self, file_path: Path) -> bool:
        """Check if file is supported"""
        return file_path.suffix.lower() in self.supported_extensions


def parse_text(file_path: Path) -> Dict[str, any]:
    """
    Convenience function to parse text file

    Args:
        file_path: Path to text file

    Returns:
        Parsed content dictionary
    """
    parser = TextParser()
    return parser.parse(file_path)
