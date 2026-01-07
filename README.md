# ContractAI

A contract assessment application that uses AI to analyze contracts from both contractor and company perspectives.

## Overview

ContractAI reads contracts in DOCX or PDF format, preprocesses them using the attachments library, and uses DSPy modules/agents to provide dual-perspective assessments:

- **Contractor Advocate**: Assesses contracts focusing on contractor rights, payment terms, liability, and obligations
- **Company Advocate**: Assesses contracts focusing on company protection, deliverables, quality standards, and compliance

## Features

- 📄 Support for DOCX and PDF contract formats
- 🤖 AI-powered dual perspective analysis using DSPy
- 📊 Preprocessing with attachments library
- 💡 Detailed assessments with key concerns and recommendations
- 🔍 Focus on relevant aspects for each stakeholder

## Installation

```bash
pip install -e .
```

Or install with development dependencies:

```bash
pip install -e ".[dev]"
```

## Quick Start

### As a Python Module

```python
from contractai import ContractAssessmentApp

# Initialize the app
app = ContractAssessmentApp()

# Assess a contract from both perspectives
result = app.assess_contract("path/to/contract.docx", perspective="both")

# Print the assessment
app.print_assessment(result)
```

### Command Line Interface

```bash
# Assess from both perspectives
python -m contractai path/to/contract.docx

# Assess from contractor perspective only
python -m contractai path/to/contract.pdf --perspective contractor

# Assess from company perspective only
python -m contractai path/to/contract.docx --perspective company

# Use a specific language model
python -m contractai path/to/contract.docx --model openai/gpt-3.5-turbo
```

## Architecture

### Components

1. **ContractReader**: Reads and extracts text from DOCX and PDF files
2. **Preprocessing**: Uses attachments library to preprocess contract text
3. **Advocates** (DSPy Modules):
   - `ContractorAdvocate`: Analyzes from contractor's viewpoint
   - `CompanyAdvocate`: Analyzes from company's viewpoint
   - `DualAdvocateAssessor`: Combines both perspectives
4. **ContractAssessmentApp**: Main application orchestrating the workflow

### DSPy Integration

The application uses DSPy (Declarative Self-improving Python) for building the assessment agents:

- Uses `dspy.Signature` to define the assessment interface
- Implements `dspy.Module` for each advocate
- Uses `dspy.ChainOfThought` for reasoning about contracts

## Configuration

To use with OpenAI or other LLM providers, configure DSPy:

```python
import dspy

# Configure OpenAI
lm = dspy.OpenAI(model='gpt-3.5-turbo', api_key='your-api-key')
dspy.settings.configure(lm=lm)

# Then use ContractAI
app = ContractAssessmentApp()
```

## Examples

See the `examples/` directory for more detailed usage examples:

- `example_usage.py`: Complete example demonstrating all features

## Development

Run tests:
```bash
pytest
```

Format code:
```bash
black contractai/
```

Lint code:
```bash
ruff check contractai/
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
