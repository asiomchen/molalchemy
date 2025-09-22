<p align="center">
  <a href="https://molalchemy.readthedocs.io"><img src="https://raw.githubusercontent.com/asiomchen/molalchemy/refs/heads/main/docs/img/logo-full.svg" alt="MolAlchemy"></a>
</p>
<p align="center">
    <em>molalchemy - Making chemical databases as easy as regular databases! 🧪✨</em>
</p>


[![pypi version](https://img.shields.io/pypi/v/molalchemy.svg)](https://pypi.org/project/molalchemy/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/molalchemy)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/molalchemy?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/molalchemy)
[![license](https://img.shields.io/github/license/asiomchen/molalchemy)](LICENSE)
[![python versions](https://shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)]()
![Codecov (with branch)](https://img.shields.io/codecov/c/github/asiomchen/molalchemy/main)
[![powered by rdkit](https://img.shields.io/badge/Powered%20by-RDKit-3838ff.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAFVBMVEXc3NwUFP8UPP9kZP+MjP+0tP////9ZXZotAAAAAXRSTlMAQObYZgAAAAFiS0dEBmFmuH0AAAAHdElNRQfmAwsPGi+MyC9RAAAAQElEQVQI12NgQABGQUEBMENISUkRLKBsbGwEEhIyBgJFsICLC0iIUdnExcUZwnANQWfApKCK4doRBsKtQFgKAQC5Ww1JEHSEkAAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMi0wMy0xMVQxNToyNjo0NyswMDowMDzr2J4AAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjItMDMtMTFUMTU6MjY6NDcrMDA6MDBNtmAiAAAAAElFTkSuQmCC)](https://www.rdkit.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-306998?logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


**Extensions for SQLAlchemy to work with chemical cartridges**

molalchemy provides seamless integration between python and chemical databases, enabling powerful chemical structure storage, indexing, and querying capabilities. The library supports popular chemical cartridges (Bingo PostgreSQL & RDKit PostgreSQL) and provides a unified API for chemical database operations.


**This project was originally supposed to be a part of RDKit UGM 2025 hackathon, but COVID had other plans for me. Currently it is in alpha stage as a proof of concept. Contributions are welcome!**

**To give it a hackathon vibe, I build this PoC in couple hours, so expect some rough edges and missing features.**

## 🚀 Features

- **Chemical Data Types**: Custom SQLAlchemy types for molecules, reactions and fingerprints
- **Chemical Cartridge Integration**: Support for Bingo and RDKit PostgreSQL cartridges
- **Substructure Search**: Efficient substructure and similarity searching
- **Chemical Indexing**: High-performance chemical structure indexing
- **Typing**: As much type hints as possible - no need to remember yet another abstract function name
- **Easy Integration**: Drop-in replacement for standard SQLAlchemy types

## 📦 Installation

### Using pip

```bash
pip install molalchemy
```

### From source

```bash
pip install git+https://github.com/asiomchen/molalchemy.git

# or clone the repo and install
git clone https://github.com/asiomchen/molalchemy.git
cd molalchemy
pip install .
```


### Prerequisites

- Python 3.10+

- SQLAlchemy 2.0+

- rdkit 2024.3.1+

- Running PostgreSQL with chemical cartridge (Bingo or RDKit) (see [`docker-compose.yaml`](docker-compose.yaml) for a ready-to-use setup)


## 🔧 Quick Start

To learn how to use molalchemy, check out the [Quick Start - RDKit](https://molalchemy.readthedocs.io/en/latest/tutorials/01_Getting_Started_rdkit_ORM/) and [Quick Start - Bingo](https://molalchemy.readthedocs.io/en/latest/tutorials/01_Getting_Started_bingo_ORM/) tutorials in the documentation.

## 🏗️ Supported Cartridges

### Bingo Cartridge

```python
from molalchemy.bingo.types import (
    BingoMol,              # Text-based molecule storage (SMILES/Molfile)
    BingoBinaryMol,        # Binary molecule storage with format conversion
    BingoReaction,         # Reaction storage (reaction SMILES/Rxnfile)
    BingoBinaryReaction    # Binary reaction storage
)
from molalchemy.bingo.index import (
    BingoMolIndex,         # Molecule indexing
    BingoBinaryMolIndex,   # Binary molecule indexing
    BingoRxnIndex,         # Reaction indexing
    BingoBinaryRxnIndex    # Binary reaction indexing
)
from molalchemy.bingo.functions import (
    mol,                   # Molecule functions
    rxn                    # Reaction functions
)
```

### RDKit Cartridge

```python
from molalchemy.rdkit.types import (
    RDKitMol,              # RDKit molecule type
    # Additional types available...
)
from molalchemy.rdkit.index import (
    RDKitIndex,         # RDKit molecule indexing (just GIST index)
)
from molalchemy.rdkit.functions import (
    mol,                   # RDKit molecule functions
    fp,                    # Fingerprint functions
    rxn                    # Reaction functions
)
```

## 🎯 Advanced Features

### Chemical Indexing

```python
from molalchemy.bingo.index import BingoMolIndex
from molalchemy.bingo.types import BingoMol

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
from molalchemy.bingo.types import BingoBinaryMol

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

### Using Chemical Functions

`mol` provides all static methods for functional-style queries. Under the hood it uses SQLAlchemy's `func` to call the corresponding database functions, but provides type hints and syntax highlighting in IDEs.

```python
from molalchemy.bingo.functions import mol

# Calculate molecular properties
results = session.query(
    Molecule.name,
    mol.get_weight(Molecule.structure).label('molecular_weight'),
    mol.gross_formula(Molecule.structure).label('formula'),
    mol.to_canonical(Molecule.structure).label('canonical_smiles')
).all()

# Validate molecular structures
invalid_molecules = session.query(Molecule).filter(
    mol.check_molecule(Molecule.structure).isnot(None)
).all()

# Format conversions
inchi_keys = session.query(
    Molecule.id,
    mol.to_inchikey(Molecule.structure).label('inchikey')
).all()
```


## 🧪 Development

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/asiomchen/molalchemy.git
cd molalchemy
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
uv run pytest --cov=molalchemy
```

### Code Quality

This project uses modern Python development tools:
- **uv**: For virtual environment and dependency management
- **Ruff**: For linting and formatting
- **pytest**: For testing

## 📚 Documentation

- **[📋 Project Roadmap](ROADMAP.md)** - Development phases, timeline, and contribution opportunities
- **[🤝 Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[🔧 API Reference](https://molalchemy.readthedocs.io/api)** - Complete API documentation
- **[🐳 Bingo Manual](https://lifescience.opensource.epam.com/bingo/user-manual-postgres.html)** - Bingo PostgreSQL cartridge guide
- **[⚛️ RDKit Manual](https://www.rdkit.org/docs/Cartridge.html)** - RDKit PostgreSQL cartridge guide

## 🤝 Contributing

We welcome contributions! molalchemy offers many opportunities for developers interested in chemical informatics:

- **🔰 New to the project?** Check out [good first issues](https://github.com/asiomchen/molalchemy/labels/good%20first%20issue)
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
- **Email**: anton.siomchen+molalchemy@gmail.com
- **GitHub**: [@asiomchen](https://github.com/asiomchen)
- **LinkedIn**: [Anton Siomchen](https://www.linkedin.com/in/anton-siomchen/)

---

**molalchemy** - Making chemical databases as easy as regular databases! 🧪✨