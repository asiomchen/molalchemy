# Typed Proxy Helpers

MolAlchemy columns already expose chemical comparator methods at runtime. For
example, a `BingoMol` column can call `.has_substructure(...)` and an `RdkitMol`
column can call `.equals(...)`.

IDEs and type checkers cannot infer those custom SQLAlchemy comparator
methods from the mapped column type. The proxy helpers in `molalchemy.helpers`
are a small typing bridge for that case.

```python
from molalchemy.helpers import bingo_col

stmt = select(Compound).where(
    bingo_col(Compound.structure).has_substructure("c1ccccc1")
)
```

At runtime, `bingo_col(Compound.structure)` returns `Compound.structure` itself.
It is not a wrapper and it does not change SQL generation. Its return annotation
points the editor at a proxy class with the chemical methods, so autocomplete and
static analysis can see the API of comparator.

## Bingo ORM

```python
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from molalchemy.bingo.types import BingoMol, BingoReaction
from molalchemy.helpers import bingo_col, bingo_rxn_col


class Base(DeclarativeBase):
    pass


class Compound(Base):
    __tablename__ = "compounds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    structure: Mapped[str] = mapped_column(BingoMol())


class Reaction(Base):
    __tablename__ = "reactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    reaction: Mapped[str] = mapped_column(BingoReaction())


benzene_query = select(Compound).where(
    bingo_col(Compound.structure).has_substructure("c1ccccc1")
)

ethanol_query = select(Compound).where(
    bingo_col(Compound.structure).equals("CCO")
)

reaction_query = select(Reaction).where(
    bingo_rxn_col(Reaction.reaction).equals("CCO>>CC=O")
)
```

These statements compile to the same SQL as calling the comparator methods
directly on the mapped attributes.

## RDKit ORM

```python
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from molalchemy.helpers import rdkit_col, rdkit_rxn_col
from molalchemy.rdkit.types import RdkitMol, RdkitReaction


class Base(DeclarativeBase):
    pass


class Compound(Base):
    __tablename__ = "rdkit_compounds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    structure: Mapped[str] = mapped_column(RdkitMol())


class Reaction(Base):
    __tablename__ = "rdkit_reactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    reaction: Mapped[str] = mapped_column(RdkitReaction())


exact_match = select(Compound).where(
    rdkit_col(Compound.structure).equals("CCO")
)

reaction_smarts = select(Reaction).where(
    rdkit_rxn_col(Reaction.reaction).has_smarts("[C:1]>>[C:1][O]")
)
```

## SQLAlchemy Core

The helpers also accept Core table columns.

```python
from sqlalchemy import Column, Integer, MetaData, String, Table, select

from molalchemy.bingo.types import BingoMol
from molalchemy.helpers import bingo_col


metadata = MetaData()

compounds = Table(
    "compounds",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("structure", BingoMol()),
)

stmt = select(compounds).where(
    bingo_col(compounds.c.structure).has_substructure("c1ccccc1")
)
```

## Validation

Each helper checks that the input is a SQLAlchemy `Column` or ORM
`InstrumentedAttribute` with the expected MolAlchemy type.

```python
from sqlalchemy import Column, String

from molalchemy.helpers import bingo_col


name = Column("name", String)

bingo_col(name)
# TypeError: Column is not of type BingoMol or BingoBinaryMol
```

Use the matching helper for the cartridge and data kind:

| Helper | Accepted types |
| --- | --- |
| `bingo_col` | `BingoMol`, `BingoBinaryMol` |
| `bingo_rxn_col` | `BingoReaction`, `BingoBinaryReaction` |
| `rdkit_col` | `RdkitMol` |
| `rdkit_rxn_col` | `RdkitReaction` |

## When To Use Them

Use proxy helpers when your like ypur autocomplete or want to use static code analysis.

For a more explicit functional style, use the cartridge function modules:

```python
from molalchemy.bingo import functions as bingo_func
# instead of 
# select(Compound).where(Compound.structure.has_substructure("c1ccccc1"))
# use
stmt = select(Compound).where(
    bingo_func.mol_has_substructure(Compound.structure, "c1ccccc1")
)
```
