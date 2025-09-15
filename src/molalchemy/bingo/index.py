"""
Bingo database index classes for chemical data.

This module provides specialized SQLAlchemy Index classes for creating
Bingo cartridge indices on chemical data columns in PostgreSQL databases.
"""

from sqlalchemy.schema import Index


# @compiles(BingoMolIndex, 'postgresql')
# def compile_bingo_rxn_index(element, compiler, **kw):
#     expr = list(element.expressions)[0]
#     print(expr)
#     return "CREATE INDEX %s ON %s USING bingo_idx (%s bingo.reaction)" % (
#         element.name,
#         compiler.preparer.format_table(expr.table),
#         compiler.process(expr, include_table=False)
#     )
class BingoMolIndex(Index):
    """
    Bingo index for molecule columns.

    Creates a PostgreSQL index using the Bingo cartridge's `bingo_idx`
    access method with the `bingo.molecule` operator class for efficient
    molecular similarity and substructure searching.

    Parameters
    ----------
    name : str
        Name of the index to be created.
    mol_column : sqlalchemy.schema.Column
        The column containing molecular data to be indexed.

    Examples
    --------
    >>> from sqlalchemy import Integer
    >>> from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
    >>> from molalchemy.bingo.index import BingoMolIndex
    >>> from molalchemy.bingo.types import BingoMol
    >>>
    >>> class Base(DeclarativeBase):
    ...     pass
    >>>
    >>> class Molecule(Base):
    ...     __tablename__ = 'molecules'
    ...
    ...     id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ...     structure: Mapped[BingoMol] = mapped_column(BingoMol)
    ...
    ...     __table_args__ = (
    ...         BingoMolIndex('idx_mol_structure', 'structure'),
    ...     )

    Notes
    -----
    This index type is specifically designed for use with Bingo cartridge
    in PostgreSQL. The underlying SQL command generated will be:
    ```sql
    CREATE INDEX {name} ON {table} USING bingo_idx ({column} bingo.molecule)
    ```
    """

    def __init__(self, name, mol_column):
        super().__init__(
            name,
            mol_column,
            postgresql_using="bingo_idx",
            postgresql_ops={mol_column: "bingo.molecule"},
        )


class BingoBinaryMolIndex(Index):
    """
    Bingo index for binary molecule columns.

    Creates a PostgreSQL index using the Bingo cartridge's `bingo_idx`
    access method with the `bingo.bmolecule` operator class for efficient
    searching on binary-encoded molecular data.

    Parameters
    ----------
    name : str
        Name of the index to be created.
    mol_column : sqlalchemy.schema.Column
        The column containing binary molecular data to be indexed.

    Examples
    --------
    >>> from sqlalchemy import Integer
    >>> from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
    >>> from molalchemy.bingo.index import BingoBinaryMolIndex
    >>> from molalchemy.bingo.types import BingoBinaryMol
    >>>
    >>> class Base(DeclarativeBase):
    ...     pass
    >>>
    >>> class Molecule(Base):
    ...     __tablename__ = 'molecules'
    ...
    ...     id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ...     structure_bin: Mapped[BingoBinaryMol] = mapped_column(BingoBinaryMol)
    ...
    ...     __table_args__ = (
    ...         BingoBinaryMolIndex('idx_mol_structure_bin', 'structure_bin'),
    ...     )

    Notes
    -----
    This index type is optimized for binary-encoded molecular data stored
    using Bingo's binary format. The underlying SQL command generated will be:

    ```sql
    CREATE INDEX {name} ON {table} USING bingo_idx ({column} bingo.bmolecule)
    ```
    """

    def __init__(self, name, mol_column):
        super().__init__(
            name,
            mol_column,
            postgresql_using="bingo_idx",
            postgresql_ops={mol_column: "bingo.bmolecule"},
        )


class BingoRxnIndex(Index):
    """
    Bingo index for reaction columns.

    Creates a PostgreSQL index using the Bingo cartridge's `bingo_idx`
    access method with the `bingo.reaction` operator class for efficient
    reaction similarity and substructure searching.

    Parameters
    ----------
    name : str
        Name of the index to be created.
    mol_column : sqlalchemy.schema.Column
        The column containing reaction data to be indexed.

    Examples
    --------
    >>> from sqlalchemy import Integer
    >>> from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
    >>> from molalchemy.bingo.index import BingoRxnIndex
    >>> from molalchemy.bingo.types import BingoRxn
    >>>
    >>> class Base(DeclarativeBase):
    ...     pass
    >>>
    >>> class Reaction(Base):
    ...     __tablename__ = 'reactions'
    ...
    ...     id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ...     reaction: Mapped[BingoRxn] = mapped_column(BingoRxn)
    ...
    ...     __table_args__ = (
    ...         BingoRxnIndex('idx_reaction_structure', 'reaction'),
    ...     )

    Notes
    -----
    This index type is specifically designed for chemical reaction data
    using Bingo cartridge. The underlying SQL command generated will be:

    ```sql
        CREATE INDEX {name} ON {table} USING bingo_idx ({column} bingo.reaction)
    ```
    """

    def __init__(self, name, mol_column):
        super().__init__(
            name,
            mol_column,
            postgresql_using="bingo_idx",
            postgresql_ops={mol_column: "bingo.reaction"},
        )


class BingoBinaryRxnIndex(Index):
    """
    Bingo index for binary reaction columns.

    Creates a PostgreSQL index using the Bingo cartridge's `bingo_idx`
    access method with the `bingo.breaction` operator class for efficient
    searching on binary-encoded reaction data.

    Parameters
    ----------
    name : str
        Name of the index to be created.
    mol_column : sqlalchemy.schema.Column
        The column containing binary reaction data to be indexed.

    Examples
    --------
    >>> from sqlalchemy import Integer
    >>> from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
    >>> from molalchemy.bingo.index import BingoBinaryRxnIndex
    >>> from molalchemy.bingo.types import BingoBinaryRxn
    >>>
    >>> class Base(DeclarativeBase):
    ...     pass
    >>>
    >>> class Reaction(Base):
    ...     __tablename__ = 'reactions'
    ...
    ...     id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ...     reaction_bin: Mapped[BingoBinaryRxn] = mapped_column(BingoBinaryRxn)
    ...
    ...     __table_args__ = (
    ...         BingoBinaryRxnIndex('idx_reaction_structure_bin', 'reaction_bin'),
    ...     )

    Notes
    -----
    This index type is optimized for binary-encoded reaction data stored
    using Bingo's binary format. The underlying SQL command generated will be:

    ```sql
        CREATE INDEX {name} ON {table} USING bingo_idx ({column} bingo.breaction)
    ```
    """

    def __init__(self, name, mol_column):
        super().__init__(
            name,
            mol_column,
            postgresql_using="bingo_idx",
            postgresql_ops={mol_column: "bingo.breaction"},
        )
