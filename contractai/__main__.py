#!/usr/bin/env python3
"""
Command-line interface for ContractAI.
"""

import argparse
import sys
from contractai import ContractAssessmentApp


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Assess contracts from contractor and company perspectives using AI"
    )
    parser.add_argument(
        "contract_file",
        help="Path to the contract file (docx or pdf)",
    )
    parser.add_argument(
        "--perspective",
        choices=["contractor", "company", "both"],
        default="both",
        help="Assessment perspective (default: both)",
    )
    parser.add_argument(
        "--model",
        help="Language model to use (e.g., 'openai/gpt-3.5-turbo')",
        default=None,
    )

    args = parser.parse_args()

    try:
        # Initialize and run the app
        app = ContractAssessmentApp(lm_model=args.model)
        result = app.assess_contract(args.contract_file, args.perspective)
        app.print_assessment(result)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
