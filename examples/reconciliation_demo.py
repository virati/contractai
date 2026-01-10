#!/usr/bin/env python3
"""
Demonstration of ContractAI's reconciliation feature.

This example shows how to:
1. Assess a contract from both perspectives
2. Use tunable weights to favor one perspective
3. Analyze the reconciliation results
"""

import dspy
from contractai import ContractAssessmentApp


def main():
    """Main demonstration function."""

    # Configure DSPy with your preferred LLM
    # Example with OpenAI (uncomment and add your API key):
    # lm = dspy.OpenAI(model='gpt-3.5-turbo', api_key='your-api-key')
    # dspy.settings.configure(lm=lm)

    # Or use with a local model via LM Studio or similar:
    # lm = dspy.OpenAI(model='local-model', api_base='http://localhost:1234/v1', api_key='dummy')
    # dspy.settings.configure(lm=lm)

    print("=" * 80)
    print("ContractAI Reconciliation Feature Demo")
    print("=" * 80)

    # Initialize the app
    app = ContractAssessmentApp()

    # Example 1: Balanced assessment (50/50 weights)
    print("\n\n" + "=" * 80)
    print("EXAMPLE 1: Balanced Assessment (50/50)")
    print("=" * 80)

    contract_file = "path/to/your/contract.docx"  # Replace with actual path

    try:
        result_balanced = app.assess_contract(
            contract_file,
            perspective="both",
            contractor_weight=0.5,
            company_weight=0.5,
            include_reconciliation=True
        )

        print("\nBalanced assessment completed!")
        print("\nReconciliation Summary:")
        if "reconciliation" in result_balanced["assessments"]:
            rec = result_balanced["assessments"]["reconciliation"]
            print(f"- Contractor Weight: {rec['weights']['contractor']:.2f}")
            print(f"- Company Weight: {rec['weights']['company']:.2f}")
            print(f"\nCommon Ground Found:")
            print(f"{rec['common_ground'][:200]}...")  # First 200 chars

    except FileNotFoundError:
        print(f"\nNote: Contract file not found at '{contract_file}'")
        print("Please update the path to point to an actual contract file.")
    except Exception as e:
        print(f"\nNote: {e}")
        print("Make sure DSPy is configured with an LLM provider.")

    # Example 2: Contractor-favored assessment (70/30 weights)
    print("\n\n" + "=" * 80)
    print("EXAMPLE 2: Contractor-Favored Assessment (70/30)")
    print("=" * 80)

    try:
        result_contractor = app.assess_contract(
            contract_file,
            perspective="both",
            contractor_weight=0.7,
            company_weight=0.3,
            include_reconciliation=True
        )

        print("\nContractor-favored assessment completed!")
        print("\nThis assessment prioritizes contractor concerns.")
        if "reconciliation" in result_contractor["assessments"]:
            rec = result_contractor["assessments"]["reconciliation"]
            print(f"\nCompromise will lean towards contractor protection:")
            print(f"- Contractor Weight: {rec['weights']['contractor']:.2f}")
            print(f"- Company Weight: {rec['weights']['company']:.2f}")

    except Exception as e:
        print(f"\nNote: Skipping example - {e}")

    # Example 3: Company-favored assessment (30/70 weights)
    print("\n\n" + "=" * 80)
    print("EXAMPLE 3: Company-Favored Assessment (30/70)")
    print("=" * 80)

    try:
        result_company = app.assess_contract(
            contract_file,
            perspective="both",
            contractor_weight=0.3,
            company_weight=0.7,
            include_reconciliation=True
        )

        print("\nCompany-favored assessment completed!")
        print("\nThis assessment prioritizes company protection.")
        if "reconciliation" in result_company["assessments"]:
            rec = result_company["assessments"]["reconciliation"]
            print(f"\nCompromise will lean towards company concerns:")
            print(f"- Contractor Weight: {rec['weights']['contractor']:.2f}")
            print(f"- Company Weight: {rec['weights']['company']:.2f}")

    except Exception as e:
        print(f"\nNote: Skipping example - {e}")

    # Example 4: Without reconciliation
    print("\n\n" + "=" * 80)
    print("EXAMPLE 4: Assessment Without Reconciliation")
    print("=" * 80)

    try:
        result_no_rec = app.assess_contract(
            contract_file,
            perspective="both",
            include_reconciliation=False
        )

        print("\nAssessment without reconciliation completed!")
        print("\nThis provides only the two separate perspectives.")
        print("Reconciliation" + (" NOT" if "reconciliation" not in result_no_rec["assessments"] else "") + " included.")

    except Exception as e:
        print(f"\nNote: Skipping example - {e}")

    print("\n\n" + "=" * 80)
    print("Demo Complete")
    print("=" * 80)
    print("\nKey Takeaways:")
    print("1. Reconciliation helps identify conflicts between perspectives")
    print("2. Tunable weights allow favoring contractor or company concerns")
    print("3. The system provides actionable compromise suggestions")
    print("4. Implementation steps guide how to resolve conflicts")
    print("\nFor real contract analysis, configure DSPy with your LLM provider!")


if __name__ == "__main__":
    main()
