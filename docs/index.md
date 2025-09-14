![ChemSchema Logo](./img/logo-full.svg)
<p align="center">
    <em>ChemSchema - Making chemical databases as easy as regular databases! 🧪✨</em>
</p>
[![pypi version](https://img.shields.io/pypi/v/chemschema.svg)](https://pypi.org/project/chemschema/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/chemschema)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/chemschema?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/chemschema)
[![license](https://img.shields.io/github/license/asiomchen/chemschema)](LICENSE)
[![python versions](https://shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)]()
![Codecov (with branch)](https://img.shields.io/codecov/c/github/asiomchen/chemschema/main)
[![powered by rdkit](https://img.shields.io/badge/Powered%20by-RDKit-3838ff.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAFVBMVEXc3NwUFP8UPP9kZP+MjP+0tP////9ZXZotAAAAAXRSTlMAQObYZgAAAAFiS0dEBmFmuH0AAAAHdElNRQfmAwsPGi+MyC9RAAAAQElEQVQI12NgQABGQUEBMENISUkRLKBsbGwEEhIyBgJFsICLC0iIUdnExcUZwnANQWfApKCK4doRBsKtQFgKAQC5Ww1JEHSEkAAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMi0wMy0xMVQxNToyNjo0NyswMDowMDzr2J4AAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjItMDMtMTFUMTU6MjY6NDcrMDA6MDBNtmAiAAAAAElFTkSuQmCC)](https://www.rdkit.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-306998?logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


**Extensions for SQLAlchemy to work with chemical cartridges**

ChemSchema provides seamless integration between python and chemical databases, enabling powerful chemical structure storage, indexing, and querying capabilities. The library supports popular chemical cartridges (Bingo PostgreSQL & RDKit PostgreSQL) and provides a unified API for chemical database operations.


**This project was originally supposed to be a part of RDKit UGM 2025 hackathon, but COVID had other plans for me. Currently it is in alpha stage as a proof of concept. Contributions are welcome!**


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

### From source

```bash
pip install git+https://github.com/asiomchen/chemschema.git

# or clone the repo and install
git clone https://github.com/asiomchen/chemschema.git
cd chemschema
pip install .
```




### Prerequisites

ChemSchema requires:
- Python 3.10+
- Running PostgreSQL with chemical cartridge (Bingo or RDKit)
- SQLAlchemy 2.0+

## 🔧 Quick Start

### Basic Usage

```python
from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from chemschema.bingo.types import BingoMol

class Base(DeclarativeBase):
    pass

class Molecule(Base):
    __tablename__ = 'molecules'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    structure: Mapped[str] = mapped_column(BingoMol)
    name: Mapped[str] = mapped_column(String(100))

# Create engine and tables
engine = create_engine('postgresql://user:password@localhost/chemdb')
Base.metadata.create_all(engine)
```

### Chemical Queries

```python
from sqlalchemy.orm import sessionmaker
from chemschema.bingo.functions import bingo_func

Session = sessionmaker(bind=engine)
session = Session()

# Substructure search
benzene_substructures = session.query(Molecule).filter(
    bingo_func.has_substructure(Molecule.structure, 'c1ccccc1')
).all()

# SMARTS pattern matching
amines = session.query(Molecule).filter(
    bingo_func.matches_smarts(Molecule.structure, '[NX3;H2,H1;!$(NC=O)]')
).all()

# Exact structure match
exact_match = session.query(Molecule).filter(
    bingo_func.equals(Molecule.structure, 'CCO')
).first()

# Similarity search
similar_molecules = session.query(Molecule).filter(
    bingo_func.similarity(Molecule.structure, 'CCO', bottom=0.7)
).all()

# Calculate molecular properties
molecular_weights = session.query(
    Molecule.name,
    bingo_func.get_weight(Molecule.structure)
).all()
```

## 🏗️ Supported Cartridges

### Bingo Cartridge

```python
from chemschema.bingo.types import (
    BingoMol,              # Text-based molecule storage (SMILES/Molfile)
    BingoBinaryMol,        # Binary molecule storage with format conversion
    BingoReaction,         # Reaction storage (reaction SMILES/Rxnfile)
    BingoBinaryReaction    # Binary reaction storage
)
from chemschema.bingo.index import (
    BingoMolIndex,         # Molecule indexing
    BingoBinaryMolIndex,   # Binary molecule indexing
    BingoRxnIndex,         # Reaction indexing
    BingoBinaryRxnIndex    # Binary reaction indexing
)
from chemschema.bingo.functions import (
    bingo_func,            # Molecule functions
    bingo_rxn_func         # Reaction functions
)
```

### RDKit Cartridge

```python
from chemschema.rdkit.types import (
    RDKitMol,              # RDKit molecule type
    # Additional types available...
)
from chemschema.rdkit.index import (
    RDKitMolIndex,         # RDKit molecule indexing
    # Additional indices available...
)
from chemschema.rdkit.functions import (
    rdkit_func,            # RDKit functions
    # More function collections...
)
```

## 🎯 Advanced Features

### Chemical Indexing

```python
from chemschema.bingo.index import BingoMolIndex
from chemschema.bingo.types import BingoMol

class Molecule(Base):
    __tablename__ = 'molecules'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    structure: Mapped[str] = mapped_column(BingoMol)
    name: Mapped[str] = mapped_column(String(100))
    
    # Add chemical index for faster searching
    __table_args__ = (
        BingoMolIndex('mol_idx', 'structure'),
    )
```

### Binary Storage with Format Conversion

```python
from chemschema.bingo.types import BingoBinaryMol

class OptimizedMolecule(Base):
    __tablename__ = 'optimized_molecules'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Store as binary, return as SMILES
    structure: Mapped[bytes] = mapped_column(
        BingoBinaryMol(preserve_pos=False, return_type="smiles")
    )
    # Store as binary, return as Molfile (with coordinates)
    structure_3d: Mapped[bytes] = mapped_column(
        BingoBinaryMol(preserve_pos=True, return_type="molfile")
    )
```

### Reaction Storage and Searching

```python
from chemschema.bingo.types import BingoReaction
from chemschema.bingo.functions import bingo_rxn_func
from chemschema.bingo.index import BingoRxnIndex

class ChemicalReaction(Base):
    __tablename__ = 'reactions'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reaction_smiles: Mapped[str] = mapped_column(BingoReaction)
    name: Mapped[str] = mapped_column(String(200))
    
    __table_args__ = (
        BingoRxnIndex('rxn_idx', 'reaction_smiles'),
    )

# Search for oxidation reactions
oxidations = session.query(ChemicalReaction).filter(
    bingo_rxn_func.has_reaction_substructure(
        ChemicalReaction.reaction_smiles,
        "[C:1]-[OH:2]>>[C:1]=[O:2]"
    )
).all()
```

### Using Chemical Functions

`bingo_func` provides all static methods for functional-style queries. Under the hood it uses SQLAlchemy's `func` to call the corresponding database functions, but provides type hints and syntax highlighting in IDEs.

```python
from chemschema.bingo.functions import bingo_func

# Calculate molecular properties
results = session.query(
    Molecule.name,
    bingo_func.get_weight(Molecule.structure).label('molecular_weight'),
    bingo_func.gross_formula(Molecule.structure).label('formula'),
    bingo_func.to_canonical(Molecule.structure).label('canonical_smiles')
).all()

# Validate molecular structures
invalid_molecules = session.query(Molecule).filter(
    bingo_func.check_molecule(Molecule.structure).isnot(None)
).all()

# Format conversions
inchi_keys = session.query(
    Molecule.id,
    bingo_func.to_inchikey(Molecule.structure).label('inchikey')
).all()
```


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

- **[📋 Project Roadmap](ROADMAP.md)** - Development phases, timeline, and contribution opportunities
- **[🤝 Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[🔧 API Reference](https://chemschema.readthedocs.io/)** - Complete API documentation
- **[🐳 Bingo Manual](https://lifescience.opensource.epam.com/bingo/user-manual-postgres.html)** - Bingo PostgreSQL cartridge guide
- **[⚛️ RDKit Manual](https://www.rdkit.org/docs/Cartridge.html)** - RDKit PostgreSQL cartridge guide

## 🤝 Contributing

We welcome contributions! ChemSchema offers many opportunities for developers interested in chemical informatics:

- **🔰 New to the project?** Check out [good first issues](https://github.com/asiomchen/chemschema/labels/good%20first%20issue)
- **� Chemical expertise?** Help complete RDKit integration or add ChemAxon support  
- **🐳 DevOps skills?** Optimize our Docker containers and CI/CD pipeline
- **📚 Love documentation?** Create tutorials and improve API docs

Read our **[Contributing Guide](CONTRIBUTING.md)** for detailed instructions on getting started.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [RDKit](https://www.rdkit.org/) - Open-source cheminformatics toolkit
- [Bingo](https://lifescience.opensource.epam.com/bingo/) - Chemical database cartridge
- [SQLAlchemy](https://sqlalchemy.org/) - Python SQL toolkit

## 📧 Contact

- **Author**: Anton Siomchen
- **Email**: anton.siomchen+chemschema@gmail.com
- **GitHub**: [@asiomchen](https://github.com/asiomchen)
- **LinkedIn**: [Anton Siomchen](https://www.linkedin.com/in/anton-siomchen/)

---

**ChemSchema** - Making chemical databases as easy as regular databases! 🧪✨