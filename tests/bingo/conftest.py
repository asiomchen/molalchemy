"""Pytest configuration for bingo tests."""

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
        'benzene': 'c1ccccc1',
        'ethanol': 'CCO',
        'methane': 'C',
        'aspirin': 'CC(=O)OC1=CC=CC=C1C(=O)O',
        'caffeine': 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C',
    }


@pytest.fixture  
def sample_smarts():
    """Provide common SMARTS patterns for testing."""
    return {
        'benzene': '[#6]1:[#6]:[#6]:[#6]:[#6]:[#6]:1',
        'carbonyl': '[#6]=[#8]',
        'alcohol': '[#6]-[#8]-[#1]',
        'aromatic_carbon': '[#6;a]',
    }


@pytest.fixture
def sample_parameters():
    """Provide common bingo parameters for testing."""
    return {
        'empty': '',
        'max_5': 'max=5',
        'timeout_1000': 'timeout=1000',
        'stereo': 'stereochemistry=1',
        'combined': 'max=10,timeout=5000',
    }
