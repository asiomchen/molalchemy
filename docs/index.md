<p align="center">
  <a href="https://molalchemy.readthedocs.io"><img src="https://raw.githubusercontent.com/asiomchen/molalchemy/refs/heads/main/docs/img/logo-full.svg" alt="MolAlchemy"></a>
</p>
<p align="center">
    <em>molalchemy - Making chemical databases as easy as regular databases! 🧪✨</em>
</p>


[![pypi version](https://img.shields.io/pypi/v/molalchemy.svg)](https://pypi.org/project/molalchemy/)
[![license](https://img.shields.io/github/license/asiomchen/molalchemy)](https://github.com/asiomchen/molalchemy/blob/main/LICENSE)
[![python versions](https://shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)]()
![PyPI - Downloads](https://img.shields.io/pypi/dm/molalchemy)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/molalchemy?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/molalchemy)
[![codecov](https://codecov.io/gh/asiomchen/molalchemy/graph/badge.svg?token=B1GKJTDZCK)](https://codecov.io/gh/asiomchen/molalchemy)
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
- **Alembic Integration**: Automatic handling of extensions and imports in database migrations
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
- Running PostgreSQL with chemical cartridge (Bingo or RDKit) (see [`docker-compose.yaml`](https://github.com/asiomchen/molalchemy/blob/main/docker-compose.yaml) for a ready-to-use setup)

For development or testing, you can use the provided Docker setup:

```bash
# For RDKit cartridge
docker-compose up rdkit

# For Bingo cartridge  
docker-compose up bingo
```

## 📁 Project Structure

```
molalchemy/
├── src/molalchemy/
│   ├── types.py              # Base type definitions
│   ├── helpers.py            # Common utilities
│   ├── alembic_helpers.py    # Alembic integration utilities
│   ├── bingo/               # Bingo PostgreSQL cartridge support
│   │   ├── types.py         # Bingo-specific types
│   │   ├── index.py         # Bingo indexing
│   │   ├── comparators.py   # SQLAlchemy comparators
│   │   └── functions/       # Bingo database functions
│   └── rdkit/               # RDKit PostgreSQL cartridge support
│       ├── types.py         # RDKit-specific types
│       ├── index.py         # RDKit indexing  
│       ├── comparators.py   # SQLAlchemy comparators
│       └── functions/       # RDKit database functions
├── tests/                   # Test suite
├── docs/                    # Documentation
└── dev_scripts/             # Development utilities
```


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
    # Individual function imports available, see documentation
    # for complete list of chemical analysis functions
)
```

### RDKit Cartridge

```python
from molalchemy.rdkit.types import (
    RdkitMol,              # RDKit molecule type with configurable return formats
    RdkitBitFingerprint,   # Binary fingerprints (bfp)
    RdkitSparseFingerprint,# Sparse fingerprints (sfp)
    RdkitReaction,         # Chemical reactions
    RdkitQMol,             # Query molecules
    RdkitXQMol,            # Extended query molecules
)
from molalchemy.rdkit.index import (
    RdkitIndex,            # RDKit molecule indexing (GIST index)
)
from molalchemy.rdkit.functions import (
    # Individual function imports available, see documentation
    # for complete list of 150+ RDKit functions
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

### Configurable Return Types

```python
from molalchemy.rdkit.types import RdkitMol

class MoleculeWithFormats(Base):
    __tablename__ = 'molecules_formatted'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Return as SMILES string (default)
    structure_smiles: Mapped[str] = mapped_column(RdkitMol())
    # Return as RDKit Mol object
    structure_mol: Mapped[bytes] = mapped_column(RdkitMol(return_type="mol"))
    # Return as raw bytes
    structure_bytes: Mapped[bytes] = mapped_column(RdkitMol(return_type="bytes"))
```

### Using Chemical Functions

The chemical functions are available as individual imports from the functions modules. Under the hood they use SQLAlchemy's `func` to call the corresponding database functions, and provide type hints and syntax highlighting in IDEs.

```python
from molalchemy.bingo.functions import smiles, getweight, gross, inchikey

# Calculate molecular properties using Bingo functions
results = session.query(
    Molecule.name,
    getweight(Molecule.structure).label('molecular_weight'),
    gross(Molecule.structure).label('formula'),
    smiles(Molecule.structure).label('canonical_smiles')
).all()

# Validate molecular structures
from molalchemy.bingo.functions import checkmolecule

invalid_molecules = session.query(Molecule).filter(
    checkmolecule(Molecule.structure).isnot(None)
).all()

# Format conversions
inchi_keys = session.query(
    Molecule.id,
    inchikey(Molecule.structure).label('inchikey')
).all()
```

For RDKit functions:

```python
from molalchemy.rdkit.functions import mol_amw, mol_formula, mol_inchikey

# Calculate molecular properties using RDKit functions
results = session.query(
    Molecule.name,
    mol_amw(Molecule.structure).label('molecular_weight'),
    mol_formula(Molecule.structure).label('formula'),
    mol_inchikey(Molecule.structure).label('inchikey')
).all()
```

### Alembic Database Migrations

Molalchemy provides utilities for Alembic integration.For automatic import handling in migrations, the library provides type rendering utilities that ensure proper import statements are generated for molalchemy types.

```python
# ...
from molalchemy import alembic_helpers
# ...

def run_migrations_offline():
    # ...
    context.configure(
        # ...
        render_item=alembic_helpers.render_item,
    )
    # ...


def run_migrations_online():
    # ...
    context.configure(
        # ...
        render_item=alembic_helpers.render_item,
    )
    # ...
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
# Run all tests with coverage
make test

# Or use uv directly
uv run pytest

# Run specific test module
uv run pytest tests/bingo/

# Run with coverage
uv run pytest --cov=src/molalchemy
```

### Code Quality

This project uses modern Python development tools:
- **uv**: For virtual environment and dependency management
- **Ruff**: For linting and formatting
- **pytest**: For testing

### Building Function Bindings

The chemical function bindings are automatically generated from cartridge documentation:

```bash
# Update RDKit function bindings
make update-rdkit-func

# Update Bingo function bindings  
make update-bingo-func

# Update all function bindings
make update-func
```

## 📚 Documentation

- **[📋 Project Roadmap](ROADMAP.md)** - Development phases, timeline, and contribution opportunities
- **[🤝 Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[🔧 API Reference](https://molalchemy.readthedocs.io/)** - Complete API documentation
- **[🐳 Bingo Manual](https://lifescience.opensource.epam.com/bingo/user-manual-postgres.html)** - Bingo PostgreSQL cartridge guide
- **[⚛️ RDKit Manual](https://www.rdkit.org/docs/Cartridge.html)** - RDKit PostgreSQL cartridge guide

## 🤝 Contributing

We welcome contributions! molalchemy offers many opportunities for developers interested in chemical informatics:

- **🔰 New to the project?** Check out [good first issues](https://github.com/asiomchen/molalchemy/labels/good%20first%20issue)
- **🔬 Chemical expertise?** Help complete RDKit integration or add ChemAxon support
- **🐳 DevOps skills?** Optimize our Docker containers and CI/CD pipeline
- **📚 Love documentation?** Create tutorials and improve API docs

Read our **[Contributing Guide](CONTRIBUTING.md)** for detailed instructions on getting started.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/asiomchen/molalchemy/blob/main/LICENSE) file for details.

## 🙏 Acknowledgments

### Core Technologies
- [RDKit](https://www.rdkit.org/) - Open-source cheminformatics toolkit
- [Bingo](https://lifescience.opensource.epam.com/bingo/) - Chemical database cartridge by EPAM
- [SQLAlchemy](https://sqlalchemy.org/) - Python SQL toolkit and ORM

### Inspiration and Similar Projects
- [GeoAlchemy2](https://github.com/geoalchemy/geoalchemy2) - Spatial extension for SQLAlchemy, served as architectural inspiration for cartridge integration patterns
- [ord-schema](https://github.com/open-reaction-database/ord-schema) - Open Reaction Database schema, is one of the few projects using custom chemical types with SQLAlchemy
- [Riccardo Vianello](https://github.com/rvianello) - His work on [django-rdkit](https://github.com/rdkit/django-rdkit) and [razi](https://github.com/rvianello/razi) provided valuable insights for chemical database integration (discovered after starting this project)

## 📧 Contact

- **Author**: Anton Siomchen
- **Email**: anton.siomchen+molalchemy@gmail.com
- **GitHub**: [@asiomchen](https://github.com/asiomchen)
- **LinkedIn**: [Anton Siomchen](https://www.linkedin.com/in/anton-siomchen/)

---

**molalchemy** - Making chemical databases as easy as regular databases! 🧪✨