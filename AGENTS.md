# Agent Instructions for molalchemy

## Build/Lint/Test Commands

```bash
# Run all tests with coverage
make test

# Run specific test file
uv run pytest tests/bingo/test_types.py -v

# Run single test
uv run pytest tests/bingo/test_functions.py::test_substructure -v

# Format code
uv run ruff format .

# Lint and auto-fix issues
uv run ruff check --fix .

# Type check
uv run mypy src/

# Serve documentation locally
uv run mkdocs serve

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate
```

## Dependency Management

- Use `uv` for all dependency management (not pip)
- Add packages: `uv add package_name`
- Add dev packages: `uv add --dev package_name`
- Sync environment: `uv sync`

## Code Style Guidelines

### Imports
- Group imports: stdlib, third-party, local
- Use absolute imports for local modules
- Use full paths in docstrings (e.g., `molalchemy.bingo.types.BingoMol`)

### Formatting
- Ruff 0.14.5 for linting and formatting
- Line length follows Ruff defaults
- Run `uv run ruff format .` before committing

### Type Hints
- Use type hints for all function parameters and return types
- Use `Optional`, `Union`, `Literal` from `typing` module
- mypy with SQLAlchemy plugin enabled

### Docstrings
- Use NumPy-style docstrings
- Include Parameters, Returns, Examples, Notes sections
- Use backticks for literals: `"smiles"`, `42`, `True`
- Reference types with full module paths

### Naming Conventions
- Classes: PascalCase (e.g., `BingoMol`, `RdkitIndex`)
- Functions/variables: snake_case (e.g., `get_mol_weight`)
- Constants: UPPER_SNAKE_CASE
- Private methods: `_leading_underscore`

### Error Handling
- Raise `ValueError` for invalid inputs with descriptive messages
- Create informative error messages explaining what went wrong
- Use type hints to prevent errors at runtime

### SQLAlchemy Patterns
- Prefer typed declarative ORM style in examples
- Use `Mapped[type]` annotations with `mapped_column()`
- Custom types inherit from `UserDefinedType`

### Testing
- Tests organized in `tests/bingo/` and `tests/rdkit/`
- Use pytest fixtures in `conftest.py`
- Test both success and failure cases
- Use descriptive test names

### Documentation
- All public APIs must have docstrings
- Include working code examples in docstrings
- Documentation built with MkDocs

## Project Structure

```
src/molalchemy/
├── bingo/           # Bingo PostgreSQL cartridge
├── rdkit/           # RDKit PostgreSQL cartridge
├── types.py         # Base types
├── helpers.py       # Utilities
└── alembic_helpers.py  # Migration utilities
```

## Pre-commit

Install pre-commit hooks:
```bash
uv tool install pre-commit --with pre-commit-uv --force-reinstall
pre-commit install
```

## GitHub Copilot Instructions (from .github/copilot-instructions.md)

- Use `uv run` to run scripts without activating venv
- NumPy docstring style required
- Full import paths in docstrings
- Backticks for literals
- SQLAlchemy typed declarative ORM style preferred
