"""Pytest configuration for rdkit tests."""

import pytest
from sqlalchemy import MetaData


@pytest.fixture
def metadata():
    """Provide a clean MetaData instance for each test."""
    return MetaData()


@pytest.fixture
def sample_smiles():
    """Provide common SMILES strings for testing."""
    return {
        "benzene": "c1ccccc1",
        "ethanol": "CCO",
        "methane": "C",
        "aspirin": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "caffeine": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
    }
