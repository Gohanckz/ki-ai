"""
PDF Parser for extracting text from PDF documents
"""

from pathlib import Path
from typing import List, Dict, Optional
import PyPDF2
from ...utils.logger import setup_logger

logger = setup_logger("ki.parsers.pdf")


class PDFParser:
    """Parser for PDF documents"""

    def __init__(self):
        self.supported_extensions = [".pdf"]

    def parse(self, file_path: Path) -> Dict[str, any]:
        """
        Parse PDF file and extract text

        Args:
            file_path: Path to PDF file

        Returns:
            Dictionary with parsed content
        """
        try:
            logger.info(f"Parsing PDF: {file_path.name}")

            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)

                # Extract metadata
                metadata = self._extract_metadata(reader)

                # Extract text from all pages
                pages = []
                full_text = []

                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text = page.extract_text()

                    pages.append({
                        "page_number": page_num + 1,
                        "text": text,
                        "char_count": len(text)
                    })

                    full_text.append(text)

                combined_text = "\n\n".join(full_text)

                result = {
                    "file_name": file_path.name,
                    "file_path": str(file_path),
                    "file_type": "pdf",
                    "total_pages": len(reader.pages),
                    "metadata": metadata,
                    "pages": pages,
                    "full_text": combined_text,
                    "char_count": len(combined_text),
                    "word_count": len(combined_text.split()),
                    "success": True,
                    "error": None
                }

                logger.info(f"✅ Parsed {len(reader.pages)} pages, {result['word_count']} words")

                return result

        except Exception as e:
            logger.error(f"❌ Error parsing PDF {file_path.name}: {str(e)}")
            return {
                "file_name": file_path.name,
                "file_path": str(file_path),
                "file_type": "pdf",
                "success": False,
                "error": str(e),
                "full_text": ""
            }

    def _extract_metadata(self, reader: PyPDF2.PdfReader) -> Dict[str, str]:
        """Extract PDF metadata"""
        metadata = {}

        try:
            if reader.metadata:
                metadata = {
                    "title": reader.metadata.get("/Title", ""),
                    "author": reader.metadata.get("/Author", ""),
                    "subject": reader.metadata.get("/Subject", ""),
                    "creator": reader.metadata.get("/Creator", ""),
                    "producer": reader.metadata.get("/Producer", ""),
                }
        except Exception as e:
            logger.warning(f"Could not extract metadata: {str(e)}")

        return metadata

    def is_supported(self, file_path: Path) -> bool:
        """Check if file is supported"""
        return file_path.suffix.lower() in self.supported_extensions


def parse_pdf(file_path: Path) -> Dict[str, any]:
    """
    Convenience function to parse PDF

    Args:
        file_path: Path to PDF file

    Returns:
        Parsed content dictionary
    """
    parser = PDFParser()
    return parser.parse(file_path)
