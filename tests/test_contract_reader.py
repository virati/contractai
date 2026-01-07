"""
Tests for ContractReader module.
"""

import pytest
import os
from contractai.contract_reader import ContractReader


class TestContractReader:
    """Tests for ContractReader class."""

    def test_init(self):
        """Test ContractReader initialization."""
        reader = ContractReader()
        assert reader.supported_formats == [".docx", ".pdf"]

    def test_unsupported_format(self):
        """Test error handling for unsupported file format."""
        reader = ContractReader()
        with pytest.raises(ValueError, match="Unsupported file format"):
            reader.read_contract("test.txt")

    def test_file_not_found(self):
        """Test error handling for missing file."""
        reader = ContractReader()
        with pytest.raises(FileNotFoundError):
            reader.read_contract("nonexistent.docx")

    def test_preprocess_with_attachments(self):
        """Test preprocessing functionality."""
        reader = ContractReader()
        text = "This is a test contract with multiple words."
        result = reader.preprocess_with_attachments(text)

        assert "raw_text" in result
        assert "processed_text" in result
        assert "word_count" in result
        assert "character_count" in result
        assert result["raw_text"] == text
        assert result["word_count"] == 8
        assert result["character_count"] == len(text)
