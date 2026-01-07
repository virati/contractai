"""
Main application for contract assessment.
"""

import os
from typing import Dict, Any, Optional
import dspy

from .contract_reader import ContractReader
from .advocates import ContractorAdvocate, CompanyAdvocate, DualAdvocateAssessor


class ContractAssessmentApp:
    """
    Main application for assessing contracts using DSPy advocates.
    """

    def __init__(self, lm_model: Optional[str] = None):
        """
        Initialize the contract assessment application.

        Args:
            lm_model: Optional language model to use (e.g., 'openai/gpt-3.5-turbo')
                     If None, uses default DSPy configuration
        """
        self.reader = ContractReader()
        self.assessor = DualAdvocateAssessor()

        # Configure DSPy language model if provided
        if lm_model:
            lm = dspy.OpenAI(model=lm_model)
            dspy.settings.configure(lm=lm)

    def assess_contract(
        self, file_path: str, perspective: str = "both"
    ) -> Dict[str, Any]:
        """
        Assess a contract file from specified perspective(s).

        Args:
            file_path: Path to the contract file (docx or pdf)
            perspective: Assessment perspective - 'contractor', 'company', or 'both'

        Returns:
            Assessment results including preprocessing info and advocate assessments

        Raises:
            ValueError: If perspective is invalid
        """
        if perspective not in ["contractor", "company", "both"]:
            raise ValueError(
                f"Invalid perspective: {perspective}. "
                "Must be 'contractor', 'company', or 'both'"
            )

        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Contract file not found: {file_path}")

        # Read and preprocess the contract
        print(f"Reading contract from: {file_path}")
        
        print("Preprocessing contract with attachments library...")
        preprocessed = self.reader.preprocess_with_attachments(file_path)

        # Get assessments based on perspective
        print(f"Assessing contract from {perspective} perspective(s)...")
        if perspective == "both":
            assessments = self.assessor(preprocessed["processed_text"])
        elif perspective == "contractor":
            contractor_advocate = ContractorAdvocate()
            contractor_assessment = contractor_advocate(preprocessed["processed_text"])
            assessments = {
                "contractor_view": {
                    "assessment": contractor_assessment.assessment,
                    "key_concerns": contractor_assessment.key_concerns,
                    "recommendations": contractor_assessment.recommendations,
                }
            }
        else:  # perspective == "company"
            company_advocate = CompanyAdvocate()
            company_assessment = company_advocate(preprocessed["processed_text"])
            assessments = {
                "company_view": {
                    "assessment": company_assessment.assessment,
                    "key_concerns": company_assessment.key_concerns,
                    "recommendations": company_assessment.recommendations,
                }
            }

        return {
            "file_path": file_path,
            "preprocessing": {
                "word_count": preprocessed["word_count"],
                "character_count": preprocessed["character_count"],
            },
            "assessments": assessments,
        }

    def print_assessment(self, result: Dict[str, Any]) -> None:
        """
        Pretty print the assessment results.

        Args:
            result: Assessment result dictionary
        """
        print("\n" + "=" * 80)
        print(f"CONTRACT ASSESSMENT: {result['file_path']}")
        print("=" * 80)

        print(f"\nPreprocessing Info:")
        print(f"  - Word Count: {result['preprocessing']['word_count']}")
        print(f"  - Character Count: {result['preprocessing']['character_count']}")

        assessments = result["assessments"]

        if "contractor_view" in assessments:
            print("\n" + "-" * 80)
            print("CONTRACTOR PERSPECTIVE")
            print("-" * 80)
            cv = assessments["contractor_view"]
            print(f"\nAssessment:\n{cv['assessment']}")
            print(f"\nKey Concerns:\n{cv['key_concerns']}")
            print(f"\nRecommendations:\n{cv['recommendations']}")

        if "company_view" in assessments:
            print("\n" + "-" * 80)
            print("COMPANY PERSPECTIVE")
            print("-" * 80)
            cv = assessments["company_view"]
            print(f"\nAssessment:\n{cv['assessment']}")
            print(f"\nKey Concerns:\n{cv['key_concerns']}")
            print(f"\nRecommendations:\n{cv['recommendations']}")

        print("\n" + "=" * 80)
