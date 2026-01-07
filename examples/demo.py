"""
Demo script showing the ContractAI structure and workflow.
This demonstrates the application architecture without requiring LLM setup.
"""

from contractai import ContractReader


def demo_contract_reading():
    """Demonstrate contract reading capabilities."""
    print("=" * 80)
    print("CONTRACTAI DEMO - Contract Reading and Preprocessing")
    print("=" * 80)
    
    # Initialize the reader
    reader = ContractReader()
    
    # Read the sample contract
    contract_path = "examples/sample_contract.docx"
    print(f"\n1. Reading contract from: {contract_path}")
    contract_text = reader.read_contract(contract_path)
    
    print(f"\n2. Contract text (first 500 characters):")
    print("-" * 80)
    print(contract_text[:500] + "...")
    
    # Preprocess the contract with attachments library
    print(f"\n3. Preprocessing with attachments library...")
    preprocessed = reader.preprocess_with_attachments(contract_path)
    
    print(f"\n4. Preprocessing Results:")
    print(f"   - Word Count: {preprocessed['word_count']}")
    print(f"   - Character Count: {preprocessed['character_count']}")
    if preprocessed.get('metadata'):
        print(f"   - Metadata: {preprocessed['metadata']}")
    
    # Show what the advocates would analyze
    print(f"\n5. DSPy Advocate Architecture:")
    print("-" * 80)
    print("   Contractor Advocate would focus on:")
    print("   - Payment terms and schedules")
    print("   - Contractor rights and protections")
    print("   - Liability limitations")
    print("   - Scope clarity")
    print("   - Termination clauses")
    print("   - Intellectual property rights")
    
    print("\n   Company Advocate would focus on:")
    print("   - Deliverable quality standards")
    print("   - Timeline commitments")
    print("   - Confidentiality agreements")
    print("   - Company protection")
    print("   - Compliance requirements")
    print("   - Service level agreements")
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)
    print("\nTo use with actual LLM assessment:")
    print("1. Configure DSPy with your preferred LLM (OpenAI, Anthropic, etc.)")
    print("2. Run: python -m contractai examples/sample_contract.docx")
    print("\nFor more info, see README.md")


if __name__ == "__main__":
    demo_contract_reading()
