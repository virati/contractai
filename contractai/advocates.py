"""
DSPy-based advocates for contract assessment from different perspectives.
"""

import dspy
from typing import Dict, Any


class ContractAssessment(dspy.Signature):
    """Assess a contract from a specific perspective."""

    contract_text = dspy.InputField(desc="The contract text to assess")
    perspective = dspy.InputField(desc="The perspective to assess from (contractor or company)")
    assessment = dspy.OutputField(desc="Detailed assessment of the contract")
    key_concerns = dspy.OutputField(desc="Key concerns identified")
    recommendations = dspy.OutputField(desc="Recommendations for this party")


class ContractorAdvocate(dspy.Module):
    """
    A DSPy agent that assesses contracts from the contractor's perspective.
    Focuses on contractor rights, payment terms, liability, and obligations.
    """

    def __init__(self):
        super().__init__()
        self.assess = dspy.ChainOfThought(ContractAssessment)

    def forward(self, contract_text: str) -> dspy.Prediction:
        """
        Assess the contract from the contractor's perspective.

        Args:
            contract_text: The contract text to assess

        Returns:
            Assessment including concerns and recommendations
        """
        perspective = (
            "contractor - focusing on payment terms, contractor rights, "
            "liability limitations, scope clarity, termination clauses, "
            "and intellectual property rights"
        )
        return self.assess(contract_text=contract_text, perspective=perspective)


class CompanyAdvocate(dspy.Module):
    """
    A DSPy agent that assesses contracts from the company's perspective.
    Focuses on company protection, deliverables, quality standards, and compliance.
    """

    def __init__(self):
        super().__init__()
        self.assess = dspy.ChainOfThought(ContractAssessment)

    def forward(self, contract_text: str) -> dspy.Prediction:
        """
        Assess the contract from the company's perspective.

        Args:
            contract_text: The contract text to assess

        Returns:
            Assessment including concerns and recommendations
        """
        perspective = (
            "company - focusing on deliverable quality standards, "
            "timeline commitments, confidentiality, company protection, "
            "compliance requirements, and service level agreements"
        )
        return self.assess(contract_text=contract_text, perspective=perspective)


class DualAdvocateAssessor(dspy.Module):
    """
    Combines both contractor and company advocates for comprehensive assessment.
    """

    def __init__(self):
        super().__init__()
        self.contractor_advocate = ContractorAdvocate()
        self.company_advocate = CompanyAdvocate()

    def forward(self, contract_text: str) -> Dict[str, Any]:
        """
        Get assessments from both perspectives.

        Args:
            contract_text: The contract text to assess

        Returns:
            Dictionary with both contractor and company assessments
        """
        contractor_assessment = self.contractor_advocate(contract_text)
        company_assessment = self.company_advocate(contract_text)

        return {
            "contractor_view": {
                "assessment": contractor_assessment.assessment,
                "key_concerns": contractor_assessment.key_concerns,
                "recommendations": contractor_assessment.recommendations,
            },
            "company_view": {
                "assessment": company_assessment.assessment,
                "key_concerns": company_assessment.key_concerns,
                "recommendations": company_assessment.recommendations,
            },
        }
