"""Bingo PostgreSQL types for chemical structures.

This module provides SQLAlchemy UserDefinedType classes for working with
chemical molecules and reactions in PostgreSQL using the Bingo cartridge.
"""

from typing import Any, Generic, Literal, TypeVar, overload

from sqlalchemy import func
from sqlalchemy.types import UserDefinedType

from molalchemy.bingo.comparators import BingoMolComparator, BingoRxnComparator

_BINGO_BINARY_MOL_RETURN_TYPES = ("smiles", "molfile", "cml", "bytes")
_T = TypeVar("_T")


def _validate_return_type(value: object) -> None:
    if not isinstance(value, str):
        raise TypeError(f"return_type must be a str, got {type(value).__name__}")
    if value not in _BINGO_BINARY_MOL_RETURN_TYPES:
        choices = ", ".join(repr(choice) for choice in _BINGO_BINARY_MOL_RETURN_TYPES)
        raise ValueError(f"return_type must be one of {choices}, got {value!r}")


def _validate_preserve_pos(value: object) -> None:
    if type(value) is not bool:
        raise TypeError(f"preserve_pos must be a bool, got {type(value).__name__}")


class BingoBaseType(UserDefinedType[_T], Generic[_T]):
    """Base class for Bingo types."""

    _immutable_options: frozenset[str] = frozenset()

    def __setattr__(self, name: str, value: Any) -> None:
        # SQLAlchemy builds _static_cache_key from constructor-named attributes
        # in __dict__; read-only properties backed by private names hide them.
        if name in self._immutable_options and name in self.__dict__:
            raise AttributeError(f"{name} is immutable")
        super().__setattr__(name, value)


class BingoMol(BingoBaseType[str]):
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
    ...     smiles: Mapped[str] = mapped_column(BingoMol())
    ...     name: Mapped[str] = mapped_column(String(100))
    >>>
    >>> # Usage in queries
    >>> from molalchemy.bingo import functions as bingo_func
    >>>
    >>> # Find molecules containing benzene ring
    >>> benzene_derivatives = session.query(Molecule).filter(
    ...     bingo_func.mol_has_substructure(Molecule.smiles, "c1ccccc1")
    ... ).all()
    """

    cache_ok = True
    comparator_factory = BingoMolComparator

    def __repr__(self) -> str:
        return "BingoMol()"

    def get_col_spec(self, **kwargs: Any) -> str:
        """Get the column specification for this type.

        Returns
        -------
        str
            The PostgreSQL column type specification ("varchar").
        """
        return "varchar"


class BingoBinaryMol(BingoBaseType[_T], Generic[_T]):
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

    Raises
    ------
    TypeError
        If `preserve_pos` is not a boolean or `return_type` is not a string.
    ValueError
        If `return_type` is not one of the supported values.

    Notes
    -----
    `preserve_pos` and `return_type` are immutable after construction.

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
    ...     structure: Mapped[str] = mapped_column(
    ...         BingoBinaryMol(preserve_pos=True, return_type="smiles")
    ...     )
    ...     name: Mapped[str] = mapped_column(String(100))
    >>>
    >>> # Different return format configurations
    >>> class MoleculeWithMolfile(Base):
    ...     __tablename__ = 'molecules_molfile'
    ...
    ...     id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ...     structure: Mapped[str] = mapped_column(
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
    _immutable_options = frozenset(("preserve_pos", "return_type"))

    @overload
    def __init__(
        self: "BingoBinaryMol[str]",
        preserve_pos: bool = False,
        return_type: Literal["smiles", "molfile", "cml"] = "smiles",
    ) -> None: ...

    @overload
    def __init__(
        self: "BingoBinaryMol[bytes]",
        preserve_pos: bool = False,
        return_type: Literal["bytes"] = "bytes",
    ) -> None: ...

    def __init__(
        self,
        preserve_pos: bool = False,
        return_type: Literal["smiles", "molfile", "cml", "bytes"] = "smiles",
    ) -> None:
        _validate_preserve_pos(preserve_pos)
        _validate_return_type(return_type)
        self.preserve_pos = preserve_pos
        self.return_type = return_type
        super().__init__()

    def __repr__(self) -> str:
        return (
            f"BingoBinaryMol(preserve_pos={self.preserve_pos!r}, "
            f"return_type={self.return_type!r})"
        )

    def get_col_spec(self, **kwargs: Any) -> str:
        return "bytea"

    def bind_expression(self, bindvalue):
        return func.Bingo.CompactMolecule(bindvalue, self.preserve_pos)

    def column_expression(self, colexpr):
        if self.return_type == "smiles":
            return func.Bingo.smiles(colexpr)
        elif self.return_type == "molfile":
            return func.Bingo.molfile(colexpr)
        elif self.return_type == "cml":
            return func.Bingo.cml(colexpr)
        elif self.return_type == "bytes":
            return colexpr
        raise AssertionError("validated return_type was not handled")


class BingoReaction(BingoBaseType[str]):
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
    ...     reaction_smiles: Mapped[str] = mapped_column(BingoReaction())
    ...     name: Mapped[str] = mapped_column(String(200))
    >>>
    >>> # Usage in queries
    >>> from molalchemy.bingo import functions as bingo_func
    >>>
    >>> # Find reactions with specific substructure
    >>> oxidation_reactions = session.query(Reaction).filter(
    ...     bingo_func.rxn_has_substructure(
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

    def __repr__(self) -> str:
        return "BingoReaction()"

    def get_col_spec(self, **kwargs: Any) -> str:
        return "varchar"


class BingoBinaryReaction(BingoBaseType[bytes]):
    """SQLAlchemy type for binary chemical reaction data.

    This type represents chemical reactions stored in Bingo's internal binary
    format in PostgreSQL. It provides storage efficiency and fast comparison
    operations for reaction data.

    Parameters
    ----------
    preserve_pos : bool, default False
        Whether to preserve atom coordinates when converting to binary format.
        If `True`, coordinates are stored; if `False`, they are discarded.

    Warnings
    --------
    When `preserve_pos=True`, only inputs with present atomic coordinates should be used, otherwise conversion can return `NULL`.

    Raises
    ------
    TypeError
        If `preserve_pos` is not a boolean.

    Notes
    -----
    `preserve_pos` is immutable after construction.

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
    ...     reaction_data: Mapped[bytes] = mapped_column(BingoBinaryReaction())
    ...     name: Mapped[str] = mapped_column(String(200))
    >>>
    >>> # Usage: Binary storage provides faster searching and less storage space
    >>> # Input as reaction SMILES, stored as binary, retrieved as binary
    >>> from molalchemy.bingo import functions as bingo_func
    >>>
    >>> # Convert to binary format when inserting
    >>> rxn = Reaction(name="hydrogenation")
    >>> # The reaction data is converted by BingoBinaryReaction during insertion.
    >>> # during insertion
    >>>
    >>> # Search operations work directly on binary data
    >>> results = session.query(Reaction).filter(
    ...     bingo_func.rxn_has_substructure(
    ...         Reaction.reaction_data,
    ...         "C=C>>CC"
    ...     )
    ... ).all()
    """

    cache_ok = True
    comparator_factory = BingoRxnComparator
    _immutable_options = frozenset(("preserve_pos",))

    def __init__(self, preserve_pos: bool = False) -> None:
        _validate_preserve_pos(preserve_pos)
        self.preserve_pos = preserve_pos
        super().__init__()

    def __repr__(self) -> str:
        return f"BingoBinaryReaction(preserve_pos={self.preserve_pos!r})"

    def get_col_spec(self, **kwargs: Any) -> str:
        return "bytea"

    def bind_expression(self, bindvalue):
        return func.Bingo.CompactReaction(bindvalue, self.preserve_pos)
