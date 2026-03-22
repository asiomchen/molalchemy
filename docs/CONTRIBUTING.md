# Contributing to molalchemy

Welcome to molalchemy! We're excited to have you contribute to making chemical databases more accessible in Python. This guide will help you get started with contributing to the project.

## 🚀 Quick Start for Contributors

### Prerequisites
- Python 3.10+ 
- Docker (for running test databases)
- Git
- Basic knowledge of SQLAlchemy and chemical informatics

### Development Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/asiomchen/molalchemy.git
cd molalchemy

# 2. Install dependencies with uv
uv sync

# 3. Activate the virtual environment
source .venv/bin/activate

# 4. Start a test database
docker-compose up -d bingo  # or rdkit

# 5. Run tests to ensure everything works
uv run pytest tests/bingo/ -v

# 6. Start the documentation server
uv run mkdocs serve
```

### Working with SQL functions

All the SQL functions modules are generated automatically from the data in `./data` directory. Files are using `dev_scripts/gen_functions.py` script and Jinja2 templates in `dev_scripts/templates/` directory.


### 🧪 **Intermediate Contributions**

#### RDKit/Bingo Function Implementation

 As the RDKit/Bingo PostgreSQL functions are generated automatically from templates, 
#### Performance Benchmarking

Create benchmarks to measure and track molalchemy performance over time.

**Tasks:**
- Design realistic chemical database scenarios
- Implement benchmark scripts
- Create performance reporting
- Set up regression detection

#### Error Handling Improvements

Improve error messages and create custom exception classes for better debugging.

**Tasks:**
- Create molalchemy-specific exception hierarchy
- Improve error message clarity
- Add error handling guides
- Test error scenarios

### 🚀 **Advanced Contributions**

Improve error messages and create custom exception classes for better debugging.

**Tasks:**
- Create molalchemy-specific exception hierarchy
- Improve error message clarity
- Add error handling guides
- Test error scenarios

####  ChemAxon Cartridge Integration

Add support for ChemAxon's JChem PostgreSQL cartridge.

**This is a major contribution that would:**
- Significantly expand molalchemy's capabilities
- Require learning JChem APIs
- Need comprehensive testing
- Require detailed documentation

#### Advanced Chemical Operations

Implement higher-level chemical operations like scaffold analysis, fragment operations, or reaction processing.

#### Data Science Integration

Create pandas accessors and DataFrame operations for chemical data.

## 📋 Development Workflow

### Before You Start

1. **Check existing issues** - Someone might already be working on it
2. **Create an issue** - Discuss your idea before starting
3. **Fork the repository** - Work in your own copy
4. **Create a branch** - Use descriptive names like `feature/rdkit-mol-formula`

### Development Process

#### 1. **Set Up Your Environment**
```bash
# Create and activate virtual environment
uv sync
# if you plan to change the documentation too - install all dependencies
uv sync --all-extras --all-groups
source .venv/bin/activate

# Start relevant database
docker-compose up -d bingo  # or rdkit

# Run tests to ensure baseline works
uv run pytest tests/ -v
```

#### 2. **Code Style and Quality**

We use modern Python tooling for code quality:

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check --fix .
```

We also us `pre-commit` hooks to automate checks:

```bash
# Install pre-commit hooks
pre-commit install
```

If you want to install hooks faster we recommend using `pre-commit-uv`:

```bash
uv tool install pre-commit --with pre-commit-uv --force-reinstall
```

Then you can continue using `pre-commit` as usual, but all hooks will run in the virtual environment created by `uv`.


#### 3. **Testing Requirements**

**All new code must include tests:**

```bash
# Run tests for specific module
uv run pytest tests/bingo/ -v
uv run pytest tests/rdkit/ -v

# Run with coverage
uv run pytest tests/ --cov=src/molalchemy --cov-report=term-missing

# Test specific function
uv run pytest tests/bingo/test_functions.py::test_substructure -v
```

**Test guidelines:**
- Write tests before implementing features (TDD encouraged)
- Test both success and failure cases
- Include edge cases and error conditions
- Use meaningful test names and docstrings

#### 4. **Documentation Requirements**

**All public APIs must be documented:**

```python
def example_function(param: str) -> str:
    """Short description of the function.
    
    Longer description if needed, explaining the purpose,
    behavior, and any important details.
    
    Parameters
    ----------
    param : str
        Description of the parameter.
        
    Returns
    -------
    str
        Description of the return value.
        
    Examples
    --------
    >>> example_function("input")
    'output'
    
    Notes
    -----
    Any important notes about usage, limitations, or
    implementation details.
    """
    return f"processed_{param}"
```

**Documentation checklist:**
- [ ] NumPy-style docstrings for all public functions
- [ ] Working code examples in docstrings, if applicable
- [ ] Update relevant documentation files
- [ ] Test documentation builds: `uv run mkdocs serve`

#### 5. **Commit Guidelines**

Use clear, descriptive commit messages:

```bash
# Good examples
git commit -m "feat: add mol_formula function to RDKit integration"
git commit -m "fix: handle empty SMILES strings in BingoMol type"
git commit -m "docs: add tutorial for reaction searching"
git commit -m "test: add edge cases for similarity functions"

# Use conventional commit format
# feat: new features
# fix: bug fixes
# docs: documentation changes
# test: test additions/changes
# refactor: code refactoring
# perf: performance improvements
```

### Pull Request Process

#### 1. **Before Submitting**
- [ ] Tests pass: `uv run pytest`
- [ ] Code is formatted: `uv run ruff format .`
- [ ] Linting passes: `uv run ruff check .`
- [ ] Type checking passes: `uv run mypy src/`
- [ ] Documentation builds: `uv run mkdocs serve`
- [ ] Changelog updated (if applicable)

#### 2. **Pull Request Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing performed

## Documentation
- [ ] Docstrings added/updated
- [ ] Documentation updated
- [ ] Examples included

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Ready for review
```

## 🔍 Code Organization

### Project Structure
```
molalchemy/
├── src/molalchemy/          # Main package
│   ├── bingo/              # Bingo cartridge integration
│   │   ├── types.py        # SQLAlchemy types
│   │   ├── functions.py    # Database functions
│   │   ├── index.py        # Index classes
│   │   └── comparators.py  # Column comparators
│   ├── rdkit/              # RDKit cartridge integration
│   │   └── ...             # Same structure as bingo/
│   ├── base.py             # Common base classes
│   ├── helpers.py          # Utility functions
│   └── utils.py            # General utilities
├── tests/                  # Test suite
│   ├── bingo/             # Bingo-specific tests
│   ├── rdkit/             # RDKit-specific tests
│   └── conftest.py        # Test configuration
├── docs/                   # Documentation
├── docker/                 # Docker configurations
└── examples/               # Usage examples
```

### Coding Standards

#### **Type Hints**

Use type hints throughout:
```python
from typing import Optional, Union, List
from sqlalchemy import ColumnElement
from sqlalchemy.sql.functions import Function

def chemical_function(
    column: ColumnElement, 
    query: str, 
    threshold: Optional[float] = None
) -> Function[bool]:
    """Function with proper type hints."""
    pass
```

#### **Error Handling**

Create informative error messages:
```python
if not query.strip():
    raise ValueError(
        "Query string cannot be empty. "
        "Please provide a valid SMILES or SMARTS pattern."
    )
```

#### **Documentation**


Follow NumPy docstring style:
```python
def substructure_search(mol_column: ColumnElement, pattern: str) -> BinaryExpression:
    """Search for substructures in molecule column.
    
    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecular data.
    pattern : str
        SMILES or SMARTS pattern to search for.
        
    Returns
    -------
    BinaryExpression
        SQLAlchemy expression for use in WHERE clauses.
        
    Examples
    --------
    >>> # Find molecules containing benzene ring
    >>> session.query(Molecule).filter(
    ...     substructure_search(Molecule.structure, "c1ccccc1")
    ... ).all()
    """
```

## 🧪 Testing Guidelines

### Test Organization
- `tests/bingo/` - Bingo-specific tests
- `tests/rdkit/` - RDKit-specific tests

## 📚 Documentation Guidelines

### API Documentation
- Use NumPy-style docstrings
- Include working examples
- Document all parameters and return values
- Add notes for important usage details

### User Guides
- Step-by-step tutorials
- Real-world examples
- Common pitfalls and solutions
- Performance tips

### Code Examples
All examples should be:
- Runnable (tested in CI)
- Realistic use cases
- Well-commented
- Follow best practices

## 🐳 Docker Development

### Working with Containers

#### **Start Development Database**
```bash
# Bingo database
docker-compose up -d bingo

# RDKit database  
docker-compose up -d rdkit

```

#### **Connect to Database**
```bash
# Connect to Bingo
docker-compose exec bingo psql -U postgres

# Connect to RDKit
docker-compose exec rdkit psql -U postgres
```

#### **Reset Database**
```bash
# Remove containers and volumes
docker-compose down -v

# Restart containers
docker-compose up -d
```

## 🆘 Getting Help

### Before Asking for Help
1. Check existing documentation
2. Search GitHub issues
3. Review similar implementations
4. Try debugging with minimal examples

### Where to Get Help
- **GitHub Discussions** - General questions and design discussions
- **GitHub Issues** - Bug reports and feature requests
- **Direct Contact** - anton.siomchen+molalchemy@gmail.com for complex questions

### How to Ask Good Questions
1. **Provide context** - What are you trying to achieve?
2. **Show code** - Minimal, complete, reproducible example
3. **Include errors** - Full error messages and tracebacks
4. **Describe attempts** - What have you already tried?


## Release Process

1. **Update Changelog** - Follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
2. Create a new tag on `main` matching the semantic versioning format (e.g., `v0.1.0`). We use `hatch-vcs` for version management, so version will be updated automatically, based on the tag.
3. Push the tag to GitHub
4. GitHub Actions will build and wait for manual approval to publish to PyPI
5. After approval, the package will be published to PyPI automatically
6. Together with the package, documentation will be published to ReadTheDocs
7. Draft release is created automatically with auto-generated notes from the PR titles since the last release - please review and edit if necessary

---

## 📞 Contact

- **Project Lead**: Anton Siomchen anton.siomchen+molalchemy@gmail.com
- **GitHub**: [@asiomchen](https://github.com/asiomchen)
- **LinkedIn**: [Anton Siomchen](https://www.linkedin.com/in/anton-siomchen/)

Thank you for contributing to molalchemy! Together, we're making chemical databases more accessible to everyone. 🧪✨