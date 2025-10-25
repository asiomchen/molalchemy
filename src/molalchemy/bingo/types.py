"""Bingo PostgreSQL types for chemical structures.

This module provides SQLAlchemy UserDefinedType classes for working with
chemical molecules and reactions in PostgreSQL using the Bingo cartridge.
"""

from typing import Literal

from sqlalchemy import func
from sqlalchemy.types import UserDefinedType

from molalchemy.bingo.comparators import BingoMolComparator, BingoRxnComparator


class BingoBaseType(UserDefinedType):
    """Base class for Bingo types."""


class BingoMol(BingoBaseType):
    """SQLAlchemy type for molecule data stored as text (varchar).

    This type represents molecules stored as text in PostgreSQL, typically
    as SMILES strings or Molfiles. It uses varchar as the underlying storage
    type and provides molecular comparison capabilities through BingoMolComparator.

    Attributes
    ----------
    cache_ok : bool
        Indicates that this type can be safely cached.
    comparator_factory : type
        Factory class for creating molecular comparators.

    Examples
    --------
    >>> from sqlalchemy import Integer, String
    >>> from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
    >>> from molalchemy.bingo.types import BingoMol
    >>>
    >>> class Base(DeclarativeBase):
    ...     pass
    >>>
    >>> class Molecule(Base):
    ...     __tablename__ = 'molecules'
    ...
    ...     id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ...     smiles: Mapped[str] = mapped_column(BingoMol)
    ...     name: Mapped[str] = mapped_column(String(100))
    >>>
    >>> # Usage in queries
    >>> from molalchemy.bingo.functions import bingo_func
    >>>
    >>> # Find molecules containing benzene ring
    >>> benzene_derivatives = session.query(Molecule).filter(
    ...     bingo_func.has_substructure(Molecule.smiles, "c1ccccc1")
    ... ).all()
    """

    cache_ok = True
    comparator_factory = BingoMolComparator

    def get_col_spec(self):
        """Get the column specification for this type.

        Returns
        -------
        str
            The PostgreSQL column type specification ("varchar").
        """
        return "varchar"


class BingoBinaryMol(BingoBaseType):
    """SQLAlchemy type for binary molecule data with format conversion.

    This type represents molecules stored in Bingo's internal binary format
    in PostgreSQL. It provides automatic conversion between various molecular
    formats and the binary storage format, with options for preserving
    atomic coordinates and specifying the return format for queries.

    Parameters
        ----------
    preserve_pos : bool, default False
        Whether to preserve atomic coordinates when converting to binary format.
        If `True`, coordinates are stored; if `False`, they are discarded.
    return_type : Literal["smiles", "molfile", "cml", "bytes"]
        The format to return when reading data from the database:

        - `"smiles"`: Return as SMILES string

        - `"molfile"`: Return as MDL Molfile format

        - `"cml"`: Return as Chemical Markup Language format

        - `"bytes"`: Return raw binary data

    Warnings
    --------
    When `preserve_pos=True`, only inputs with present atomic coordinates should be used, otherwise an error will occur during conversion.

    Examples
    --------
    >>> from sqlalchemy import Integer, String
    >>> from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
    >>> from molalchemy.bingo.types import BingoBinaryMol
    >>>
    >>> class Base(DeclarativeBase):
    ...     pass
    >>>
    >>> class Molecule(Base):
    ...     __tablename__ = 'molecules'
    ...
    ...     id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ...     structure: Mapped[bytes] = mapped_column(
    ...         BingoBinaryMol(preserve_pos=True, return_type="smiles")
    ...     )
    ...     name: Mapped[str] = mapped_column(String(100))
    >>>
    >>> # Different return format configurations
    >>> class MoleculeWithMolfile(Base):
    ...     __tablename__ = 'molecules_molfile'
    ...
    ...     id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ...     structure: Mapped[bytes] = mapped_column(
    ...         BingoBinaryMol(preserve_pos=True, return_type="molfile")
    ...     )
    >>>
    >>> # Usage: When inserting SMILES, it's automatically converted to binary
    >>> # When querying, it's automatically converted back to SMILES
    >>> mol = Molecule(structure="CCO", name="ethanol")
    >>> session.add(mol)
    >>> session.commit()
    """

    cache_ok = True
    comparator_factory = BingoMolComparator

    def __init__(
        self,
        preserve_pos: bool = False,
        return_type: Literal["smiles", "molfile", "cml", "bytes"] = "smiles",
    ):
        self.preserve_pos = preserve_pos
        self.return_type = return_type
        super().__init__()

    def get_col_spec(self):
        """Get the column specification for this type.

        Returns
        -------
        str
            The PostgreSQL column type specification ("bytea").
        """
        return "bytea"

    def bind_expression(self, bindvalue):
        return func.Bingo.CompactMolecule(bindvalue, self.preserve_pos)

    def column_expression(self, col):
        if self.return_type == "smiles":
            return func.Bingo.smiles(col)
        elif self.return_type == "molfile":
            return func.Bingo.molfile(col)
        elif self.return_type == "cml":
            return func.Bingo.cml(col)
        elif self.return_type == "bytes":
            return col
        else:
            raise ValueError(
                f"Invalid return_type: {self.return_type}. Available options are 'smiles', 'molfile', 'cml', 'bytes'."
            )


class BingoReaction(BingoBaseType):
    """SQLAlchemy type for chemical reaction data stored as text (varchar).

    This type represents chemical reactions stored as text in PostgreSQL,
    typically as reaction SMILES or Rxnfiles. It uses varchar as the underlying
    storage type and provides reaction comparison capabilities through
    BingoRxnComparator.


    Examples
    --------
    >>> from sqlalchemy import Integer, String
    >>> from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
    >>> from molalchemy.bingo.types import BingoReaction
    >>>
    >>> class Base(DeclarativeBase):
    ...     pass
    >>>
    >>> class Reaction(Base):
    ...     __tablename__ = 'reactions'
    ...
    ...     id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ...     reaction_smiles: Mapped[str] = mapped_column(BingoReaction)
    ...     name: Mapped[str] = mapped_column(String(200))
    >>>
    >>> # Usage in queries
    >>> from molalchemy.bingo.functions import bingo_rxn_func
    >>>
    >>> # Find reactions with specific substructure
    >>> oxidation_reactions = session.query(Reaction).filter(
    ...     bingo_rxn_func.has_reaction_substructure(
    ...         Reaction.reaction_smiles,
    ...         "[OH]>>[O]"
    ...     )
    ... ).all()
    >>>
    >>> # Insert a reaction
    >>> rxn = Reaction(
    ...     reaction_smiles="CCO>>CC=O",
    ...     name="ethanol oxidation"
    ... )
    >>> session.add(rxn)
    """

    cache_ok = True
    comparator_factory = BingoRxnComparator

    def get_col_spec(self):
        """Get the column specification for this type.

        Returns
        -------
        str
            The PostgreSQL column type specification ("varchar").
        """
        return "varchar"


class BingoBinaryReaction(BingoBaseType):
    """SQLAlchemy type for binary chemical reaction data.

    This type represents chemical reactions stored in Bingo's internal binary
    format in PostgreSQL. It provides storage efficiency and fast comparison
    operations for reaction data.


    Examples
    --------
    >>> from sqlalchemy import Integer, String
    >>> from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
    >>> from molalchemy.bingo.types import BingoBinaryReaction
    >>>
    >>> class Base(DeclarativeBase):
    ...     pass
    >>>
    >>> class Reaction(Base):
    ...     __tablename__ = 'reactions_binary'
    ...
    ...     id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ...     reaction_data: Mapped[bytes] = mapped_column(BingoBinaryReaction)
    ...     name: Mapped[str] = mapped_column(String(200))
    >>>
    >>> # Usage: Binary storage provides faster searching and less storage space
    >>> # Input as reaction SMILES, stored as binary, retrieved as binary
    >>> from molalchemy.bingo.functions import bingo_rxn_func
    >>>
    >>> # Convert to binary format when inserting
    >>> rxn = Reaction(name="hydrogenation")
    >>> # The reaction data would be converted using bingo_rxn_func.to_binary()
    >>> # during insertion
    >>>
    >>> # Search operations work directly on binary data
    >>> results = session.query(Reaction).filter(
    ...     bingo_rxn_func.has_reaction_substructure(
    ...         Reaction.reaction_data,
    ...         "C=C>>CC"
    ...     )
    ... ).all()
    """

    cache_ok = True
    comparator_factory = BingoRxnComparator

    def get_col_spec(self):
        """Get the column specification for this type.

        Returns
        -------
        str
            The PostgreSQL column type specification ("bytea").
        """
        return "bytea"
