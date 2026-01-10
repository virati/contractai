"""
DSPy-based reconciliation module for finding compromises between perspectives.
"""

import dspy
from typing import Dict, Any, Optional


class ConflictIdentification(dspy.Signature):
    """Identify conflicts between contractor and company perspectives."""

    contractor_assessment = dspy.InputField(desc="The contractor's assessment")
    contractor_concerns = dspy.InputField(desc="The contractor's key concerns")
    company_assessment = dspy.InputField(desc="The company's assessment")
    company_concerns = dspy.InputField(desc="The company's key concerns")

    conflicts = dspy.OutputField(desc="List of identified conflicts between perspectives")
    common_ground = dspy.OutputField(desc="Areas where both perspectives align")


class CompromiseGeneration(dspy.Signature):
    """Generate compromise solutions for identified conflicts."""

    conflicts = dspy.InputField(desc="Identified conflicts between perspectives")
    contractor_recommendations = dspy.InputField(desc="Contractor's recommendations")
    company_recommendations = dspy.InputField(desc="Company's recommendations")
    contractor_weight = dspy.InputField(desc="Weight for contractor perspective (0-1)")
    company_weight = dspy.InputField(desc="Weight for company perspective (0-1)")

    compromises = dspy.OutputField(desc="Proposed compromise solutions for each conflict")
    rationale = dspy.OutputField(desc="Reasoning for each compromise")
    implementation_steps = dspy.OutputField(desc="Steps to implement the compromises")


class ReconciliationModule(dspy.Module):
    """
    A DSPy module that reconciles contractor and company perspectives.
    Identifies conflicts and generates tunable compromise solutions.
    """

    def __init__(self):
        super().__init__()
        self.identify_conflicts = dspy.ChainOfThought(ConflictIdentification)
        self.generate_compromises = dspy.ChainOfThought(CompromiseGeneration)

    def forward(
        self,
        contractor_view: Dict[str, str],
        company_view: Dict[str, str],
        contractor_weight: float = 0.5,
        company_weight: float = 0.5,
    ) -> Dict[str, Any]:
        """
        Reconcile contractor and company perspectives.

        Args:
            contractor_view: Dictionary with contractor assessment, concerns, and recommendations
            company_view: Dictionary with company assessment, concerns, and recommendations
            contractor_weight: Weight for contractor perspective (0-1, default 0.5)
            company_weight: Weight for company perspective (0-1, default 0.5)

        Returns:
            Dictionary with conflicts, common ground, and compromise solutions
        """
        # Normalize weights
        total_weight = contractor_weight + company_weight
        if total_weight > 0:
            contractor_weight = contractor_weight / total_weight
            company_weight = company_weight / total_weight
        else:
            contractor_weight = 0.5
            company_weight = 0.5

        # Step 1: Identify conflicts and common ground
        conflict_analysis = self.identify_conflicts(
            contractor_assessment=contractor_view["assessment"],
            contractor_concerns=contractor_view["key_concerns"],
            company_assessment=company_view["assessment"],
            company_concerns=company_view["key_concerns"],
        )

        # Step 2: Generate compromises based on weights
        compromise_solution = self.generate_compromises(
            conflicts=conflict_analysis.conflicts,
            contractor_recommendations=contractor_view["recommendations"],
            company_recommendations=company_view["recommendations"],
            contractor_weight=str(contractor_weight),
            company_weight=str(company_weight),
        )

        return {
            "conflicts": conflict_analysis.conflicts,
            "common_ground": conflict_analysis.common_ground,
            "compromises": compromise_solution.compromises,
            "rationale": compromise_solution.rationale,
            "implementation_steps": compromise_solution.implementation_steps,
            "weights": {
                "contractor": contractor_weight,
                "company": company_weight,
            },
        }


class TunableReconciliationAssessor(dspy.Module):
    """
    Enhanced dual advocate assessor with tunable reconciliation.
    """

    def __init__(self):
        super().__init__()
        from .advocates import ContractorAdvocate, CompanyAdvocate

        self.contractor_advocate = ContractorAdvocate()
        self.company_advocate = CompanyAdvocate()
        self.reconciliation = ReconciliationModule()

    def forward(
        self,
        contract_text: str,
        contractor_weight: float = 0.5,
        company_weight: float = 0.5,
        include_reconciliation: bool = True,
    ) -> Dict[str, Any]:
        """
        Get assessments from both perspectives with optional reconciliation.

        Args:
            contract_text: The contract text to assess
            contractor_weight: Weight for contractor perspective (0-1)
            company_weight: Weight for company perspective (0-1)
            include_reconciliation: Whether to include reconciliation analysis

        Returns:
            Dictionary with assessments and optional reconciliation
        """
        # Get individual perspectives
        contractor_assessment = self.contractor_advocate(contract_text)
        company_assessment = self.company_advocate(contract_text)

        contractor_view = {
            "assessment": contractor_assessment.assessment,
            "key_concerns": contractor_assessment.key_concerns,
            "recommendations": contractor_assessment.recommendations,
        }

        company_view = {
            "assessment": company_assessment.assessment,
            "key_concerns": company_assessment.key_concerns,
            "recommendations": company_assessment.recommendations,
        }

        result = {
            "contractor_view": contractor_view,
            "company_view": company_view,
        }

        # Add reconciliation if requested
        if include_reconciliation:
            reconciliation_result = self.reconciliation(
                contractor_view=contractor_view,
                company_view=company_view,
                contractor_weight=contractor_weight,
                company_weight=company_weight,
            )
            result["reconciliation"] = reconciliation_result

        return result
