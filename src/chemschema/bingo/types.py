"""Bingo PostgreSQL types for chemical structures.

This module provides SQLAlchemy UserDefinedType classes for working with
chemical molecules and reactions in PostgreSQL using the Bingo cartridge.
"""

from sqlalchemy.types import UserDefinedType
from chemschema.bingo.comparators import BingoMolComparator, BingoRxnComparator
from .functions import bingo_func
from typing import Literal


class BingoMol(UserDefinedType):
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
    >>> from chemschema.bingo.types import BingoMol
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
    >>> from chemschema.bingo.functions import bingo_func
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


class BingoBinaryMol(UserDefinedType):
    """SQLAlchemy type for binary molecule data with format conversion.

    This type represents molecules stored in Bingo's internal binary format
    in PostgreSQL. It provides automatic conversion between various molecular
    formats and the binary storage format, with options for preserving
    atomic coordinates and specifying the return format for queries.

    Attributes
    ----------
    cache_ok : bool
        Indicates that this type can be safely cached.
    comparator_factory : type
        Factory class for creating molecular comparators.
    preserve_pos : bool
        Whether to preserve atomic coordinates in the binary format.
    return_type : str
        Format for returning data from the database.

    Examples
    --------
    >>> from sqlalchemy import Integer, String
    >>> from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
    >>> from chemschema.bingo.types import BingoBinaryMol
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
        """Initialize the BingoBinaryMol type.

        Parameters
        ----------
        preserve_pos : bool, default False
            Whether to preserve atomic coordinates when converting to binary format.
            If `True`, coordinates are stored; if `False`, they are discarded.
        return_type : {"smiles", "molfile", "cml", "bytes"}, default `"smiles"`
            The format to return when reading data from the database:
            - "smiles": Return as SMILES string
            - "molfile": Return as MDL Molfile format
            - "cml": Return as Chemical Markup Language format
            - "bytes": Return raw binary data
        """
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
        """Convert input value to binary format for database storage.

        Parameters
        ----------
        bindvalue : Any
            The input value to be converted (typically a SMILES string or Molfile).

        Returns
        -------
        Any
            SQL expression that converts the input to Bingo binary format.
        """
        return bingo_func.to_binary(bindvalue, self.preserve_pos)

    def column_expression(self, col):
        """Convert binary column data to the specified return format.

        Parameters
        ----------
        col : Any
            The database column containing binary molecular data.

        Returns
        -------
        Any
            SQL expression that converts the binary data to the specified format.

        Raises
        ------
        ValueError
            If return_type is not one of the supported formats.
        """
        if self.return_type == "smiles":
            return bingo_func.to_smiles(col)
        elif self.return_type == "molfile":
            return bingo_func.to_molfile(col)
        elif self.return_type == "cml":
            return bingo_func.to_cml(col)
        elif self.return_type == "bytes":
            return col
        else:
            raise ValueError(
                f"Invalid return_type: {self.return_type}. Available options are 'smiles', 'molfile', 'cml', 'bytes'."
            )


class BingoReaction(UserDefinedType):
    """SQLAlchemy type for chemical reaction data stored as text (varchar).

    This type represents chemical reactions stored as text in PostgreSQL,
    typically as reaction SMILES or Rxnfiles. It uses varchar as the underlying
    storage type and provides reaction comparison capabilities through
    BingoRxnComparator.

    Attributes
    ----------
    cache_ok : bool
        Indicates that this type can be safely cached.
    comparator_factory : type
        Factory class for creating reaction comparators.

    Examples
    --------
    >>> from sqlalchemy import Integer, String
    >>> from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
    >>> from chemschema.bingo.types import BingoReaction
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
    >>> from chemschema.bingo.functions import bingo_rxn_func
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


class BingoBinaryReaction(UserDefinedType):
    """SQLAlchemy type for binary chemical reaction data.

    This type represents chemical reactions stored in Bingo's internal binary
    format in PostgreSQL. It provides storage efficiency and fast comparison
    operations for reaction data.

    Attributes
    ----------
    cache_ok : bool
        Indicates that this type can be safely cached.
    comparator_factory : type
        Factory class for creating reaction comparators.

    Examples
    --------
    >>> from sqlalchemy import Integer, String
    >>> from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
    >>> from chemschema.bingo.types import BingoBinaryReaction
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
    >>> from chemschema.bingo.functions import bingo_rxn_func
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
