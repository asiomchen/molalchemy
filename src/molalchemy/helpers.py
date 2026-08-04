"""Runtime-validated helpers for statically typed cartridge columns."""

from typing import Any, cast

from sqlalchemy import Column
from sqlalchemy.orm.attributes import InstrumentedAttribute

from molalchemy.bingo import (
    BingoBinaryMol,
    BingoBinaryReaction,
    BingoMol,
    BingoReaction,
)
from molalchemy.rdkit import RdkitMol, RdkitReaction
from molalchemy.rdkit.types import RdkitBitFingerprint, RdkitSparseFingerprint

from .protocols import (
    BingoMolColumn,
    BingoReactionColumn,
    RdkitFingerprintColumn,
    RdkitMolColumn,
    RdkitReactionColumn,
)

ChemicalColumn = Column[Any] | InstrumentedAttribute[Any]


def bingo_col(column: ChemicalColumn) -> BingoMolColumn:
    """
    Validate a Bingo molecule column and expose its typed comparator protocol.

    This function validates that the input column has a compatible Bingo molecule type
    and returns the same object with molecule-specific static typing.

    Parameters
    ----------
    column : sqlalchemy.Column | sqlalchemy.orm.attributes.InstrumentedAttribute
        A SQLAlchemy column that should be of type `molalchemy.bingo.types.BingoMol`
        or `molalchemy.bingo.types.BingoBinaryMol`.

    Returns
    -------
    molalchemy.protocols.BingoMolColumn
        The original column typed with Bingo molecule operations.

    Raises
    ------
    TypeError
        If the column is not a SQLAlchemy Column or InstrumentedAttribute, or if
        the column type is not `molalchemy.bingo.types.BingoMol` or
        `molalchemy.bingo.types.BingoBinaryMol`.
    """
    if isinstance(column, InstrumentedAttribute | Column):
        if isinstance(column.type, BingoMol) or isinstance(column.type, BingoBinaryMol):
            return cast(BingoMolColumn, column)
        else:
            raise TypeError("Column is not of type BingoMol or BingoBinaryMol")
    else:
        raise TypeError(
            f"Input is not a SQLAlchemy Column or InstrumentedAttribute, got {type(column)}"
        )


def bingo_rxn_col(column: ChemicalColumn) -> BingoReactionColumn:
    """
    Validate a Bingo reaction column and expose its typed comparator protocol.

    This function validates that the input column has a compatible Bingo reaction type
    and returns the same object with reaction-specific static typing.

    Parameters
    ----------
    column : sqlalchemy.Column
        A SQLAlchemy column that should be of type `molalchemy.bingo.types.BingoReaction`
        or `molalchemy.bingo.types.BingoBinaryReaction`.

    Returns
    -------
    molalchemy.protocols.BingoReactionColumn
        The original column typed with Bingo reaction operations.

    Raises
    ------
    TypeError
        If the column is not a SQLAlchemy Column or InstrumentedAttribute, or if
        the column type is not `molalchemy.bingo.types.BingoReaction` or
        `molalchemy.bingo.types.BingoBinaryReaction`.
    """
    if isinstance(column, InstrumentedAttribute | Column):
        if isinstance(column.type, BingoReaction) or isinstance(
            column.type, BingoBinaryReaction
        ):
            return cast(BingoReactionColumn, column)
        else:
            raise TypeError(
                "Column is not of type BingoReaction or BingoBinaryReaction"
            )
    else:
        raise TypeError(
            f"Input is not a SQLAlchemy InstrumentedAttribute or Column, got {type(column)}"
        )


def rdkit_col(column: ChemicalColumn) -> RdkitMolColumn:
    """
    Validate an RDKit molecule column and expose its typed comparator protocol.

    This validates that the input column uses `molalchemy.rdkit.types.RdkitMol`
    and returns the original column typed for IDE autocomplete.
    """
    if isinstance(column, InstrumentedAttribute | Column):
        if isinstance(column.type, RdkitMol):
            return cast(RdkitMolColumn, column)
        else:
            raise TypeError("Column is not of type RdkitMol")
    else:
        raise TypeError(
            f"Input is not a SQLAlchemy Column or InstrumentedAttribute, got {type(column)}"
        )


def rdkit_rxn_col(column: ChemicalColumn) -> RdkitReactionColumn:
    """
    Validate an RDKit reaction column and expose its typed comparator protocol.

    This validates that the input column uses `molalchemy.rdkit.types.RdkitReaction`
    and returns the original column typed for IDE autocomplete.
    """
    if isinstance(column, InstrumentedAttribute | Column):
        if isinstance(column.type, RdkitReaction):
            return cast(RdkitReactionColumn, column)
        else:
            raise TypeError("Column is not of type RdkitReaction")
    else:
        raise TypeError(
            f"Input is not a SQLAlchemy InstrumentedAttribute or Column, got {type(column)}"
        )


def rdkit_fp_col(column: ChemicalColumn) -> RdkitFingerprintColumn:
    """Validate and statically expose an RDKit fingerprint column."""
    if isinstance(column, InstrumentedAttribute | Column):
        if isinstance(column.type, RdkitBitFingerprint | RdkitSparseFingerprint):
            return cast(RdkitFingerprintColumn, column)
        raise TypeError(
            "Column is not of type RdkitBitFingerprint or RdkitSparseFingerprint"
        )
    raise TypeError(
        f"Input is not a SQLAlchemy Column or InstrumentedAttribute, got {type(column)}"
    )
