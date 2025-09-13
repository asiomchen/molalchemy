# ChemSchema

![ChemSchema Logo](docs/logo.png)

[![python versions](https://shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)]()
[![pypi version](https://img.shields.io/pypi/v/chemschema.svg)](https://pypi.org/project/chemschema/)
[![license](https://img.shields.io/github/license/asiomchen/chemschema)](LICENSE)
[![powered by rdkit](https://img.shields.io/badge/Powered%20by-RDKit-3838ff.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAFVBMVEXc3NwUFP8UPP9kZP+MjP+0tP////9ZXZotAAAAAXRSTlMAQObYZgAAAAFiS0dEBmFmuH0AAAAHdElNRQfmAwsPGi+MyC9RAAAAQElEQVQI12NgQABGQUEBMENISUkRLKBsbGwEEhIyBgJFsICLC0iIUdnExcUZwnANQWfApKCK4doRBsKtQFgKAQC5Ww1JEHSEkAAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMi0wMy0xMVQxNToyNjo0NyswMDowMDzr2J4AAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjItMDMtMTFUMTU6MjY6NDcrMDA6MDBNtmAiAAAAAElFTkSuQmCC)](https://www.rdkit.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**Extensions for SQLAlchemy to work with chemical cartridges**

ChemSchema provides seamless integration between python and chemical databases, enabling powerful chemical structure storage, indexing, and querying capabilities. The library supports most popular chemical cartridges (Bingo PostgreSQL & RDKit PostgreSQL) and provides a unified API for chemical database operations.

**This project was originally supposed to be a part of RDKit UGM 2025 hackathon but COVID had other plans for me. Currently it is in alpha stage as a proof of concept. Contributions are welcome!**


## 🚀 Features

- **Chemical Data Types**: Custom SQLAlchemy types for molecules and reactions
- **Chemical Cartridge Integration**: Support for Bingo and RDKit PostgreSQL cartridges
- **Substructure Search**: Efficient substructure and similarity searching
- **Chemical Indexing**: High-performance chemical structure indexing
- **Typing**: As much type hints as possible - no need to remember yet another abstract function name
- **Easy Integration**: Drop-in replacement for standard SQLAlchemy types

## 📦 Installation

### Using pip

```bash
pip install chemschema
```

### Using uv (recommended for development)

```bash
uv add chemschema
```

### Prerequisites

ChemSchema requires:
- Python 3.10+
- Running PostgreSQL with chemical cartridge (Bingo or RDKit)
- SQLAlchemy 2.0+

## 🔧 Quick Start

### Basic Usage

```python
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from chemschema.bingo import BingoMol

Base = declarative_base()

class Molecule(Base):
    __tablename__ = 'molecules'
    
    id = Column(Integer, primary_key=True)
    structure = Column(BingoMol)

# Create engine and tables
engine = create_engine('postgresql://user:password@localhost/chemdb')
Base.metadata.create_all(engine)
```

### Chemical Queries

```python
from sqlalchemy.orm import sessionmaker
from chemschema.bingo import BingoMol

Session = sessionmaker(bind=engine)
session = Session()

# Substructure search
benzene_substructures = session.query(Molecule).filter(
    Molecule.structure.substructure('c1ccccc1')
).all()

# SMARTS pattern matching
amines = session.query(Molecule).filter(
    Molecule.structure.has_smarts('[NX3;H2,H1;!$(NC=O)]')
).all()

# Exact structure match
exact_match = session.query(Molecule).filter(
    Molecule.structure.equals('CCO')
).first()
```

## 🏗️ Supported Cartridges

### Bingo Cartridge

```python
from chemschema.bingo import (
    BingoMol,           # Text-based molecule storage
    BingoBinaryMol,     # Binary molecule storage  
    BingoReaction,      # Reaction storage
    BingoMolIndex,      # Molecule indexing
    bingo_func          # Bingo functions
)
```

### RDKit Cartridge (Coming Soon)

```python
from chemschema.rdkit import (
    RDKitMol,          # RDKit molecule type
    # More types coming...
)
```

## 🎯 Advanced Features

### Chemical Indexing

```python
from chemschema.bingo import BingoMolIndex

class Molecule(Base):
    __tablename__ = 'molecules'
    
    id = Column(Integer, primary_key=True)
    structure = Column(BingoMol)
    
    # Add chemical index for faster searching
    __table_args__ = (
        BingoMolIndex('mol_idx', 'structure'),
    )
```

### Custom Functions

bingo_func proovides all static methods for functional-style queries. Under the hood it uses SQLAlchemy's `func` to call the corresponding database functions. But provides type hints and syntax highlighting in IDEs.

```python
from chemschema.bingo import bingo_func

# Use Bingo functions directly
molecular_weight = session.query(
    bingo_func.get_mass(Molecule.structure)
).scalar()


## 🧪 Development

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/asiomchen/chemschema.git
cd chemschema
```

2. Install dependencies:
```bash
uv sync
```

3. Activate the virtual environment:
```bash
source .venv/bin/activate
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test module
uv run pytest tests/bingo/

# Run with coverage
uv run pytest --cov=chemschema
```

### Code Quality

This project uses modern Python development tools:

- **Ruff**: For linting and formatting
- **mypy**: For type checking
- **pytest**: For testing

## 📚 Documentation

- [API Reference](https://chemschema.readthedocs.io/)
- [User Guide](docs/user_guide.md)
- [Examples](examples/)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and development process.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [RDKit](https://www.rdkit.org/) - Open-source cheminformatics toolkit
- [Bingo](https://lifescience.opensource.epam.com/bingo/) - Chemical database cartridge
- [SQLAlchemy](https://sqlalchemy.org/) - Python SQL toolkit

## 📧 Contact

- **Author**: Anton Siomchen
- **Email**: anton.siomchen@gmail.com
- **GitHub**: [@asiomchen](https://github.com/asiomchen)
- **LinkedIn**: [Anton Siomchen](https://www.linkedin.com/in/anton-siomchen/)

---

**ChemSchema** - Making chemical databases as easy as regular databases! 🧪✨