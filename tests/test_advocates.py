"""
Tests for advocate modules.
"""

import pytest
from contractai.advocates import (
    ContractorAdvocate,
    CompanyAdvocate,
    DualAdvocateAssessor,
)


class TestAdvocates:
    """Tests for advocate classes."""

    def test_contractor_advocate_init(self):
        """Test ContractorAdvocate initialization."""
        advocate = ContractorAdvocate()
        assert advocate is not None
        assert hasattr(advocate, "assess")

    def test_company_advocate_init(self):
        """Test CompanyAdvocate initialization."""
        advocate = CompanyAdvocate()
        assert advocate is not None
        assert hasattr(advocate, "assess")

    def test_dual_assessor_init(self):
        """Test DualAdvocateAssessor initialization."""
        assessor = DualAdvocateAssessor()
        assert assessor is not None
        assert hasattr(assessor, "contractor_advocate")
        assert hasattr(assessor, "company_advocate")
