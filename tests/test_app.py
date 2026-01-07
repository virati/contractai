"""
Tests for ContractAssessmentApp.
"""

import pytest
from contractai.app import ContractAssessmentApp


class TestContractAssessmentApp:
    """Tests for ContractAssessmentApp class."""

    def test_init(self):
        """Test app initialization."""
        app = ContractAssessmentApp()
        assert app is not None
        assert hasattr(app, "reader")
        assert hasattr(app, "assessor")

    def test_init_with_model(self):
        """Test app initialization with language model."""
        # Note: This won't actually configure the model without proper setup
        # but tests the parameter handling
        app = ContractAssessmentApp(lm_model=None)
        assert app is not None

    def test_invalid_perspective(self):
        """Test error handling for invalid perspective."""
        app = ContractAssessmentApp()
        with pytest.raises(ValueError, match="Invalid perspective"):
            app.assess_contract("test.docx", perspective="invalid")

    def test_file_not_found(self):
        """Test error handling for missing file."""
        app = ContractAssessmentApp()
        with pytest.raises(FileNotFoundError):
            app.assess_contract("nonexistent.docx")
