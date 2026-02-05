from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from sqlalchemy import Column, Function
from sqlalchemy.orm import InstrumentedAttribute, Mapped

from molalchemy.rdkit.types import (
    RdkitBitFingerprint,
    RdkitMol,
    RdkitQMol,
    RdkitReaction,
    RdkitSparseFingerprint,
    RdkitXQMol,
)

"""
Type aliases for RDKit-SQLAlchemy integration.
These aliases make it easier to annotate columns, mapped attributes,
and SQL functions that return RDKit objects (Mol, QMol, ...) while still
supporting literal values (e.g. SMILES strings) and raw bytes.
"""

# Python 3.10+ has TypeAlias built-in; otherwise fall back to typing_extensions.
if TYPE_CHECKING:
    from typing import TypeAlias  # pragma: no cover
else:
    try:
        from typing import TypeAlias  # type: ignore
    except ImportError:  # pragma: no cover
        from typing import TypeAlias  # type: ignore

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
# RDKit specific type aliases
# ----------------------------------------------------------------------
RdkitMolCoercible: TypeAlias = RdkitMol | LiteralStrBytes
AnyRdkitMolLike: TypeAlias = SQLAlchemyCoercible[RdkitMolCoercible] | RdkitMolCoercible
RdkitQMolCoercible: TypeAlias = RdkitQMol | LiteralStrBytes
AnyRdkitQMolLike: TypeAlias = (
    SQLAlchemyCoercible[RdkitQMolCoercible] | RdkitQMolCoercible
)
RdkitXQMolCoercible: TypeAlias = RdkitXQMol | LiteralStrBytes
AnyRdkitXQMolLike: TypeAlias = (
    SQLAlchemyCoercible[RdkitXQMolCoercible] | RdkitXQMolCoercible
)
RdkitBitFingerprintCoercible: TypeAlias = RdkitBitFingerprint | LiteralStrBytes
AnyRdkitBitFingerprintLike: TypeAlias = (
    SQLAlchemyCoercible[RdkitBitFingerprintCoercible] | RdkitBitFingerprintCoercible
)
RdkitSparseFingerprintCoercible: TypeAlias = RdkitSparseFingerprint | LiteralStrBytes
AnyRdkitSparseFingerprintLike: TypeAlias = (
    SQLAlchemyCoercible[RdkitSparseFingerprintCoercible]
    | RdkitSparseFingerprintCoercible
)
RdkitReactionCoercible: TypeAlias = RdkitReaction | LiteralStrBytes
AnyRdkitReactionLike: TypeAlias = (
    SQLAlchemyCoercible[RdkitReactionCoercible] | RdkitReactionCoercible
)

# ----------------------------------------------------------------------
# Combined fingerprint alias - convenient for functions that accept either.
# ----------------------------------------------------------------------
AnyRdkitFingerprintLike: TypeAlias = (
    AnyRdkitBitFingerprintLike | AnyRdkitSparseFingerprintLike
)

__all__ = [
    "AnyRdkitBitFingerprintLike",
    "AnyRdkitFingerprintLike",
    "AnyRdkitMolLike",
    "AnyRdkitQMolLike",
    "AnyRdkitReactionLike",
    "AnyRdkitSparseFingerprintLike",
    "AnyRdkitXQMolLike",
    "RdkitBitFingerprintCoercible",
    "RdkitMolCoercible",
    "RdkitQMolCoercible",
    "RdkitReactionCoercible",
    "RdkitSparseFingerprintCoercible",
    "RdkitXQMolCoercible",
    "SQLAlchemyCoercible",
    "TextLike",
]
