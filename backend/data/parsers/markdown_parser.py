"""
Markdown Parser for extracting text from Markdown files
"""

from pathlib import Path
from typing import Dict
import markdown
from bs4 import BeautifulSoup
from ...utils.logger import setup_logger

logger = setup_logger("ki.parsers.markdown")


class MarkdownParser:
    """Parser for Markdown documents"""

    def __init__(self):
        self.supported_extensions = [".md", ".markdown"]

    def parse(self, file_path: Path) -> Dict[str, any]:
        """
        Parse Markdown file

        Args:
            file_path: Path to Markdown file

        Returns:
            Dictionary with parsed content
        """
        try:
            logger.info(f"Parsing Markdown: {file_path.name}")

            with open(file_path, 'r', encoding='utf-8') as f:
                markdown_text = f.read()

            # Convert Markdown to HTML
            html = markdown.markdown(markdown_text, extensions=['extra', 'codehilite'])

            # Extract plain text from HTML
            soup = BeautifulSoup(html, 'html.parser')
            plain_text = soup.get_text()

            # Extract headers
            headers = self._extract_headers(markdown_text)

            # Extract code blocks
            code_blocks = self._extract_code_blocks(markdown_text)

            result = {
                "file_name": file_path.name,
                "file_path": str(file_path),
                "file_type": "markdown",
                "markdown_text": markdown_text,
                "html": html,
                "plain_text": plain_text,
                "headers": headers,
                "code_blocks": code_blocks,
                "full_text": plain_text,  # For consistency with other parsers
                "char_count": len(plain_text),
                "word_count": len(plain_text.split()),
                "success": True,
                "error": None
            }

            logger.info(f"✅ Parsed {len(headers)} headers, {len(code_blocks)} code blocks, {result['word_count']} words")

            return result

        except Exception as e:
            logger.error(f"❌ Error parsing Markdown {file_path.name}: {str(e)}")
            return {
                "file_name": file_path.name,
                "file_path": str(file_path),
                "file_type": "markdown",
                "success": False,
                "error": str(e),
                "full_text": ""
            }

    def _extract_headers(self, markdown_text: str) -> list:
        """Extract headers from markdown"""
        headers = []
        for line in markdown_text.split('\n'):
            stripped = line.strip()
            if stripped.startswith('#'):
                level = len(stripped) - len(stripped.lstrip('#'))
                text = stripped.lstrip('#').strip()
                headers.append({
                    "level": level,
                    "text": text
                })
        return headers

    def _extract_code_blocks(self, markdown_text: str) -> list:
        """Extract code blocks from markdown"""
        code_blocks = []
        in_code_block = False
        current_block = []
        current_language = None

        for line in markdown_text.split('\n'):
            if line.strip().startswith('```'):
                if in_code_block:
                    # End of code block
                    code_blocks.append({
                        "language": current_language,
                        "code": '\n'.join(current_block)
                    })
                    current_block = []
                    current_language = None
                    in_code_block = False
                else:
                    # Start of code block
                    current_language = line.strip()[3:].strip() or "plain"
                    in_code_block = True
            elif in_code_block:
                current_block.append(line)

        return code_blocks

    def is_supported(self, file_path: Path) -> bool:
        """Check if file is supported"""
        return file_path.suffix.lower() in self.supported_extensions


def parse_markdown(file_path: Path) -> Dict[str, any]:
    """
    Convenience function to parse Markdown

    Args:
        file_path: Path to Markdown file

    Returns:
        Parsed content dictionary
    """
    parser = MarkdownParser()
    return parser.parse(file_path)
