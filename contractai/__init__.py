"""
ContractAI - A contract assessment application using DSPy agents.
"""

__version__ = "0.1.0"

from .contract_reader import ContractReader
from .advocates import ContractorAdvocate, CompanyAdvocate
from .app import ContractAssessmentApp

__all__ = [
    "ContractReader",
    "ContractorAdvocate",
    "CompanyAdvocate",
    "ContractAssessmentApp",
]
