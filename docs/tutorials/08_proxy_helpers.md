# Typed Comparator Helpers

MolAlchemy columns already expose chemical comparator methods at runtime. For
example, a `BingoMol` column can call `.has_substructure(...)` and an `RdkitMol`
column can call `.equals(...)`.

IDEs and type checkers cannot infer those custom SQLAlchemy comparator
methods from the mapped column type. The helpers in `molalchemy.helpers`
are a small typing bridge for that case.

```python
from molalchemy.helpers import bingo_col

stmt = select(Compound).where(
    bingo_col(Compound.structure).has_substructure("c1ccccc1")
)
```

At runtime, `bingo_col(Compound.structure)` returns `Compound.structure` itself.
It is not a wrapper and it does not change SQL generation. Its return annotation
points the editor at a typed protocol with the chemical methods, so autocomplete
and static analysis can see the comparator API and its precise result types.

## Bingo ORM

```python
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from molalchemy.bingo import BingoMol, BingoReaction
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

similarity_query = select(Compound).where(
    bingo_col(Compound.structure).similar_to("CCO", minimum=0.7)
)

similarity_score = bingo_col(Compound.structure).similarity_score("CCO")

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

from molalchemy.helpers import rdkit_col, rdkit_fp_col, rdkit_rxn_col
from molalchemy.rdkit import RdkitBitFingerprint, RdkitMol, RdkitReaction


class Base(DeclarativeBase):
    pass


class Compound(Base):
    __tablename__ = "rdkit_compounds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    structure: Mapped[str] = mapped_column(RdkitMol())
    fingerprint: Mapped[bytes] = mapped_column(RdkitBitFingerprint())


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

nearest = select(Compound).order_by(
    rdkit_fp_col(Compound.fingerprint).tanimoto_distance(b"query fingerprint")
)

bingo_compatible_match = select(Compound).where(
    rdkit_fp_col(Compound.fingerprint).similar_to(
        b"query fingerprint", minimum=0.7, metric="Tanimoto"
    )
)

bingo_compatible_score = rdkit_fp_col(Compound.fingerprint).similarity_score(
    b"query fingerprint", metric="Dice"
)
```

For RDKit molecule columns, `.equals()` is an explicit spelling of chemical
equality. RDKit maps its `@=` operator and the normal SQL `=` operator used by
`column == query` to the same `mol_eq` function. Similarly, `.not_equals()` and
`!=` both use RDKit's `mol_ne`. The helper form is useful for static typing; it
does not change the equality semantics.

## SQLAlchemy Core

The helpers also accept Core table columns.

```python
from sqlalchemy import Column, Integer, MetaData, String, Table, select

from molalchemy.bingo import BingoMol
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
| `rdkit_fp_col` | `RdkitBitFingerprint`, `RdkitSparseFingerprint` |

## When To Use Them

Direct comparator calls remain the runtime API. Use these helpers when you want
`ty` and editor autocomplete to know the cartridge-specific methods and their
`ColumnElement[bool]` or `ColumnElement[float]` results. SQLAlchemy currently
types direct dynamic comparator lookup as `Any`.

For a more explicit functional style, use the cartridge function modules:

```python
from molalchemy.bingo import functions as bingo_func
# instead of 
# select(Compound).where(Compound.structure.has_substructure("c1ccccc1"))
# use
stmt = select(Compound).where(
    bingo_func.mol_has_substructure(Compound.structure, "c1ccccc1")
)

similar = select(Compound).where(
    bingo_func.mol_similar_to(Compound.structure, "CCO", minimum=0.7)
)

scores = select(
    bingo_func.mol_similarity_score(Compound.structure, "CCO")
)
```
