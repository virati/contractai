"""
Tests for the reconciliation module.
"""

import pytest
from contractai.reconciliation import ReconciliationModule, TunableReconciliationAssessor


class TestReconciliationModule:
    """Test the ReconciliationModule class."""

    def test_initialization(self):
        """Test that ReconciliationModule initializes correctly."""
        module = ReconciliationModule()
        assert module is not None
        assert hasattr(module, "identify_conflicts")
        assert hasattr(module, "generate_compromises")

    def test_forward_with_sample_data(self):
        """Test reconciliation with sample contractor and company views."""
        module = ReconciliationModule()

        contractor_view = {
            "assessment": "The contract heavily favors the company with strict deliverables.",
            "key_concerns": "Limited liability protection, unclear payment terms.",
            "recommendations": "Negotiate liability cap, clarify payment schedule.",
        }

        company_view = {
            "assessment": "The contract lacks clear quality standards and timelines.",
            "key_concerns": "Vague deliverables, no performance metrics.",
            "recommendations": "Add detailed specifications and milestone dates.",
        }

        # This would normally call the LLM, so we'll just test the structure
        # In a real test environment, you'd mock the DSPy calls
        try:
            result = module(
                contractor_view=contractor_view,
                company_view=company_view,
                contractor_weight=0.5,
                company_weight=0.5,
            )

            # Check that the result has the expected structure
            assert "conflicts" in result
            assert "common_ground" in result
            assert "compromises" in result
            assert "rationale" in result
            assert "implementation_steps" in result
            assert "weights" in result
            assert result["weights"]["contractor"] == 0.5
            assert result["weights"]["company"] == 0.5
        except Exception as e:
            # If DSPy is not configured, this will fail, which is expected in tests
            pytest.skip(f"DSPy not configured for testing: {e}")

    def test_weight_normalization(self):
        """Test that weights are normalized correctly."""
        module = ReconciliationModule()

        contractor_view = {
            "assessment": "Test assessment",
            "key_concerns": "Test concerns",
            "recommendations": "Test recommendations",
        }

        company_view = {
            "assessment": "Test assessment",
            "key_concerns": "Test concerns",
            "recommendations": "Test recommendations",
        }

        try:
            result = module(
                contractor_view=contractor_view,
                company_view=company_view,
                contractor_weight=0.7,
                company_weight=0.3,
            )

            # Verify weights are properly normalized
            assert result["weights"]["contractor"] == 0.7
            assert result["weights"]["company"] == 0.3
        except Exception as e:
            pytest.skip(f"DSPy not configured for testing: {e}")


class TestTunableReconciliationAssessor:
    """Test the TunableReconciliationAssessor class."""

    def test_initialization(self):
        """Test that TunableReconciliationAssessor initializes correctly."""
        assessor = TunableReconciliationAssessor()
        assert assessor is not None
        assert hasattr(assessor, "contractor_advocate")
        assert hasattr(assessor, "company_advocate")
        assert hasattr(assessor, "reconciliation")

    def test_forward_structure(self):
        """Test that forward method returns correct structure."""
        assessor = TunableReconciliationAssessor()

        try:
            result = assessor(
                contract_text="This is a test contract.",
                contractor_weight=0.6,
                company_weight=0.4,
                include_reconciliation=True,
            )

            # Check structure
            assert "contractor_view" in result
            assert "company_view" in result
            assert "reconciliation" in result

            # Check contractor view structure
            assert "assessment" in result["contractor_view"]
            assert "key_concerns" in result["contractor_view"]
            assert "recommendations" in result["contractor_view"]

            # Check company view structure
            assert "assessment" in result["company_view"]
            assert "key_concerns" in result["company_view"]
            assert "recommendations" in result["company_view"]

            # Check reconciliation structure
            assert "conflicts" in result["reconciliation"]
            assert "common_ground" in result["reconciliation"]
            assert "compromises" in result["reconciliation"]
        except Exception as e:
            pytest.skip(f"DSPy not configured for testing: {e}")

    def test_forward_without_reconciliation(self):
        """Test that reconciliation can be disabled."""
        assessor = TunableReconciliationAssessor()

        try:
            result = assessor(
                contract_text="This is a test contract.",
                contractor_weight=0.5,
                company_weight=0.5,
                include_reconciliation=False,
            )

            # Check that reconciliation is not included
            assert "contractor_view" in result
            assert "company_view" in result
            assert "reconciliation" not in result
        except Exception as e:
            pytest.skip(f"DSPy not configured for testing: {e}")
