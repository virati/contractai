# DSPy Configuration Guide

## Overview

ContractAI uses DSPy (Declarative Self-improving Python) as its AI framework. DSPy allows you to configure different language models (OpenAI, Anthropic, local models, etc.) for contract assessment.

## Configuring Language Models

### Option 1: OpenAI

```python
import dspy
from contractai import ContractAssessmentApp

# Configure OpenAI
lm = dspy.OpenAI(model='gpt-3.5-turbo', api_key='your-api-key-here')
dspy.settings.configure(lm=lm)

# Use ContractAI
app = ContractAssessmentApp()
result = app.assess_contract("path/to/contract.docx")
app.print_assessment(result)
```

### Option 2: Using Environment Variables

Set your API key in the environment:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

Then in Python:

```python
import os
import dspy
from contractai import ContractAssessmentApp

# Configure with env variable
lm = dspy.OpenAI(model='gpt-3.5-turbo', api_key=os.getenv('OPENAI_API_KEY'))
dspy.settings.configure(lm=lm)

app = ContractAssessmentApp()
```

### Option 3: Anthropic (Claude)

```python
import dspy

# Configure Anthropic
lm = dspy.Claude(model='claude-3-sonnet-20240229', api_key='your-api-key-here')
dspy.settings.configure(lm=lm)
```

### Option 4: Local Models

DSPy supports local models through various backends:

```python
import dspy

# Example with a local model
lm = dspy.HFModel(model='meta-llama/Llama-2-7b-chat-hf')
dspy.settings.configure(lm=lm)
```

## Running Assessments

### Basic Usage

```python
from contractai import ContractAssessmentApp

app = ContractAssessmentApp()

# Assess from both perspectives
result = app.assess_contract("contract.docx", perspective="both")
app.print_assessment(result)

# Assess from contractor perspective only
result = app.assess_contract("contract.pdf", perspective="contractor")

# Assess from company perspective only
result = app.assess_contract("contract.docx", perspective="company")
```

### Command Line Usage

```bash
# After configuring DSPy in your environment
python -m contractai path/to/contract.docx --perspective both
```

## Advanced Configuration

### Custom DSPy Settings

```python
import dspy

# Configure with custom settings
lm = dspy.OpenAI(
    model='gpt-4',
    api_key='your-api-key',
    max_tokens=2000,
    temperature=0.7
)
dspy.settings.configure(
    lm=lm,
    trace=[],  # Enable tracing for debugging
)
```

### Caching and Performance

DSPy supports caching for improved performance:

```python
import dspy

lm = dspy.OpenAI(model='gpt-3.5-turbo')
dspy.settings.configure(lm=lm, cache=True)
```

## Troubleshooting

### No Language Model Configured

If you see an error about no language model being configured, ensure you've run:

```python
import dspy
lm = dspy.OpenAI(model='gpt-3.5-turbo', api_key='your-key')
dspy.settings.configure(lm=lm)
```

### API Rate Limits

If you hit rate limits, consider:
1. Using a different model tier
2. Implementing retry logic
3. Adding delays between requests

### Cost Management

For cost-effective usage:
- Use `gpt-3.5-turbo` instead of `gpt-4`
- Set reasonable `max_tokens` limits
- Cache results when possible

## Example: Complete Workflow

```python
import os
import dspy
from contractai import ContractAssessmentApp

# 1. Configure DSPy
api_key = os.getenv('OPENAI_API_KEY')
lm = dspy.OpenAI(model='gpt-3.5-turbo', api_key=api_key)
dspy.settings.configure(lm=lm)

# 2. Initialize app
app = ContractAssessmentApp()

# 3. Assess contract
result = app.assess_contract(
    "examples/sample_contract.docx",
    perspective="both"
)

# 4. Display results
app.print_assessment(result)

# 5. Access specific assessments
contractor_concerns = result["assessments"]["contractor_view"]["key_concerns"]
company_concerns = result["assessments"]["company_view"]["key_concerns"]

print(f"\nContractor concerns: {contractor_concerns}")
print(f"Company concerns: {company_concerns}")
```

## Further Reading

- [DSPy Documentation](https://dspy-docs.vercel.app/)
- [DSPy GitHub](https://github.com/stanfordnlp/dspy)
- [OpenAI API Documentation](https://platform.openai.com/docs)
