"""
Example usage of ContractAI application.
"""

from contractai import ContractAssessmentApp


def example_usage():
    """
    Example demonstrating how to use ContractAI.
    """
    # Initialize the app with an optional language model
    # For example: app = ContractAssessmentApp(lm_model='openai/gpt-3.5-turbo')
    app = ContractAssessmentApp()

    # Assess a contract from both perspectives
    contract_path = "sample_contract.docx"  # or "sample_contract.pdf"

    try:
        # Get assessment from both perspectives
        result = app.assess_contract(contract_path, perspective="both")

        # Print the results
        app.print_assessment(result)

        # You can also access specific parts of the assessment
        contractor_view = result["assessments"]["contractor_view"]
        company_view = result["assessments"]["company_view"]

        print("\nContractor's main concerns:")
        print(contractor_view["key_concerns"])

        print("\nCompany's main concerns:")
        print(company_view["key_concerns"])

    except FileNotFoundError:
        print(f"Contract file not found: {contract_path}")
    except Exception as e:
        print(f"Error during assessment: {e}")


if __name__ == "__main__":
    example_usage()
