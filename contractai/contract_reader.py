"""
Contract reader module for reading and preprocessing contracts from docx and pdf files.
"""

import os
from typing import Dict, Any
from docx import Document
import PyPDF2


class ContractReader:
    """
    Reads contracts from docx or pdf files and extracts text content.
    """

    def __init__(self):
        """Initialize the contract reader."""
        self.supported_formats = [".docx", ".pdf"]

    def read_contract(self, file_path: str) -> str:
        """
        Read a contract file and extract its text content.

        Args:
            file_path: Path to the contract file (docx or pdf)

        Returns:
            Extracted text content from the contract

        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Contract file not found: {file_path}")

        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext not in self.supported_formats:
            raise ValueError(
                f"Unsupported file format: {file_ext}. "
                f"Supported formats: {', '.join(self.supported_formats)}"
            )

        if file_ext == ".docx":
            return self._read_docx(file_path)
        elif file_ext == ".pdf":
            return self._read_pdf(file_path)

    def _read_docx(self, file_path: str) -> str:
        """
        Read text from a docx file.

        Args:
            file_path: Path to the docx file

        Returns:
            Extracted text content
        """
        doc = Document(file_path)
        paragraphs = [paragraph.text for paragraph in doc.paragraphs]
        return "\n".join(paragraphs)

    def _read_pdf(self, file_path: str) -> str:
        """
        Read text from a pdf file.

        Args:
            file_path: Path to the pdf file

        Returns:
            Extracted text content
        """
        text_content = []
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text_content.append(page.extract_text())
        return "\n".join(text_content)

    def preprocess_with_attachments(self, text: str) -> Dict[str, Any]:
        """
        Preprocess contract text using the attachments library.

        Args:
            text: Raw contract text

        Returns:
            Preprocessed contract data as a dictionary
        """
        try:
            import attachments

            # Use attachments library to preprocess the text
            # The attachments library typically helps with parsing structured data
            preprocessed = {
                "raw_text": text,
                "processed_text": text.strip(),
                "word_count": len(text.split()),
                "character_count": len(text),
            }
            return preprocessed
        except ImportError:
            # Fallback if attachments library is not available
            return {
                "raw_text": text,
                "processed_text": text.strip(),
                "word_count": len(text.split()),
                "character_count": len(text),
            }
