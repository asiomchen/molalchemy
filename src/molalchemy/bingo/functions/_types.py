from __future__ import annotations

from typing import (
    TypeAlias,  # pragma: no cover
    TypeVar,
)

from sqlalchemy import Column, Function
from sqlalchemy.orm import InstrumentedAttribute, Mapped

from molalchemy.bingo.types import (
    BingoBinaryMol,
    BingoBinaryReaction,
    BingoMol,
    BingoReaction,
)

"""
Type aliases for Bingo-SQLAlchemy integration.
These aliases make it easier to annotate columns, mapped attributes,
and SQL functions that return Bingo objects (Mol, BinaryMol, Reaction, BinaryReaction)
while still supporting literal values (e.g. SMILES strings) and raw bytes.
"""


T = TypeVar("T")
SQLAlchemyCoercible: TypeAlias = (
    InstrumentedAttribute[T] | Column[T] | Mapped[T] | Function[T]
)

LiteralStrBytes: TypeAlias = str | bytes

# Text-like types for string/bytes inputs
TextLike: TypeAlias = (
    str | bytes | Column[str] | Mapped[str] | InstrumentedAttribute[str]
)

# ----------------------------------------------------------------------
# Bingo specific type aliases
# ----------------------------------------------------------------------
BingoMolCoercible: TypeAlias = BingoMol | str
AnyBingoMolLike: TypeAlias = SQLAlchemyCoercible[BingoMolCoercible] | BingoMolCoercible

BingoBinaryMolCoercible: TypeAlias = BingoBinaryMol | bytes
AnyBingoBinaryMolLike: TypeAlias = (
    SQLAlchemyCoercible[BingoBinaryMolCoercible] | BingoBinaryMolCoercible
)

BingoReactionCoercible: TypeAlias = BingoReaction | LiteralStrBytes
AnyBingoReactionLike: TypeAlias = (
    SQLAlchemyCoercible[BingoReactionCoercible] | BingoReactionCoercible
)

BingoBinaryReactionCoercible: TypeAlias = BingoBinaryReaction | LiteralStrBytes
AnyBingoBinaryReactionLike: TypeAlias = (
    SQLAlchemyCoercible[BingoBinaryReactionCoercible] | BingoBinaryReactionCoercible
)

# ----------------------------------------------------------------------
# Combined aliases - convenience for functions accepting text or binary
# ----------------------------------------------------------------------
AnyBingoMolLikeCombined: TypeAlias = AnyBingoMolLike | AnyBingoBinaryMolLike
AnyBingoReactionLikeCombined: TypeAlias = (
    AnyBingoReactionLike | AnyBingoBinaryReactionLike
)

__all__ = [
    "AnyBingoBinaryMolLike",
    "AnyBingoBinaryReactionLike",
    "AnyBingoMolLike",
    "AnyBingoMolLikeCombined",
    "AnyBingoReactionLike",
    "AnyBingoReactionLikeCombined",
    "BingoBinaryMolCoercible",
    "BingoBinaryReactionCoercible",
    "BingoMolCoercible",
    "BingoReactionCoercible",
    "SQLAlchemyCoercible",
    "TextLike",
]
