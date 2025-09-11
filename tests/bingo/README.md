# Bingo Query Structure Tests

This directory contains comprehensive tests for the Bingo query structure components in ChemSchema.

## Test Coverage

The test suite covers all major components of the Bingo integration:

### 1. Types (`test_types.py`)
- **BingoMol**: Text-based molecule storage type
- **BingoBinaryMol**: Binary molecule storage type
- Tests cover type properties, comparator factories, and table integration

### 2. Comparators (`test_comparators.py`)
- **BingoMolComparator**: Methods for molecular queries
  - `substructure()`: Substructure searching
  - `smarts()`: SMARTS pattern matching
  - `equals()`: Exact structure matching
- Tests cover query generation, parameter handling, and SQL compilation
- Compatible with both BingoMol and BingoBinaryMol types

### 3. Functions (`test_functions.py`)
- **bingo_func**: Static methods for functional-style queries
  - `substructure()`: Substructure searching
  - `smarts()`: SMARTS pattern matching  
  - `equals()`: Exact structure matching
  - `similarity()`: Similarity searching with Tanimoto/Dice metrics
- Tests cover SQL generation, parameter handling, and ORM integration

### 4. Indexes (`test_index.py`)
- **BingoMolIndex**: PostgreSQL bingo_idx indexes for BingoMol columns
- **BingoBinaryMolIndex**: PostgreSQL bingo_idx indexes for BingoBinaryMol columns
- Tests cover index creation, PostgreSQL-specific options, and table integration

### 5. Integration (`test_integration.py`)
- Complete query workflows using both Core and ORM APIs
- Complex queries with multiple conditions and joins
- Edge cases and special SMILES/SMARTS patterns
- Query variations and parameter combinations

## Test Structure

```
tests/bingo/
├── __init__.py          # Test exports and organization
├── conftest.py          # Pytest fixtures and configuration
├── test_types.py        # BingoMol and BingoBinaryMol types
├── test_comparators.py  # BingoMolComparator methods
├── test_functions.py    # bingo_func static methods  
├── test_index.py        # Bingo index types
└── test_integration.py  # Integration and workflow tests
```

## Running Tests

```bash
# Run all bingo tests
pytest tests/bingo/ -v

# Run with coverage
pytest tests/bingo/ --cov=src/chemschema/bingo --cov-report=term-missing

# Run specific test file
pytest tests/bingo/test_types.py -v

# Run specific test class
pytest tests/bingo/test_comparators.py::TestBingoMolComparator -v
```

## Test Fixtures

The `conftest.py` provides common fixtures:

- `metadata`: Clean SQLAlchemy MetaData instance
- `sample_smiles`: Common SMILES strings for testing
- `sample_smarts`: Common SMARTS patterns for testing  
- `sample_parameters`: Common bingo parameters for testing

## Coverage

Current test coverage: **100%** for all bingo module components.

## Key Test Scenarios

1. **Basic Functionality**: All comparator and function methods work correctly
2. **SQL Generation**: Proper PostgreSQL-specific SQL is generated
3. **Parameter Handling**: Various parameter combinations are supported
4. **Type Compatibility**: Both text and binary molecule types work
5. **ORM Integration**: Works with SQLAlchemy ORM models
6. **Complex Queries**: Multiple conditions, joins, and advanced patterns
7. **Edge Cases**: Special characters, empty parameters, unusual SMILES/SMARTS
8. **Index Creation**: Proper PostgreSQL bingo_idx indexes are created
