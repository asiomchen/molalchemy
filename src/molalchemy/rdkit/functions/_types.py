"""Operand aliases for RDKit cartridge function wrappers."""

from typing import Any, TypeAlias, TypeVar

from rdkit import Chem
from rdkit.Chem.rdChemReactions import ChemicalReaction
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.elements import ColumnElement

T = TypeVar("T")
SQLAlchemyCoercible: TypeAlias = ColumnElement[T] | InstrumentedAttribute[T]
SqlExpression: TypeAlias = ColumnElement[Any] | InstrumentedAttribute[Any]
LiteralStrBytes: TypeAlias = str | bytes
TextLike: TypeAlias = str | bytes | SqlExpression

RdkitMolCoercible: TypeAlias = str | Chem.Mol
AnyRdkitMolLike: TypeAlias = RdkitMolCoercible | SqlExpression
RdkitQMolCoercible: TypeAlias = str
AnyRdkitQMolLike: TypeAlias = str | SqlExpression
RdkitXQMolCoercible: TypeAlias = str
AnyRdkitXQMolLike: TypeAlias = str | SqlExpression
RdkitBitFingerprintCoercible: TypeAlias = bytes
AnyRdkitBitFingerprintLike: TypeAlias = bytes | SqlExpression
RdkitSparseFingerprintCoercible: TypeAlias = bytes
AnyRdkitSparseFingerprintLike: TypeAlias = bytes | SqlExpression
RdkitReactionCoercible: TypeAlias = str | ChemicalReaction
AnyRdkitReactionLike: TypeAlias = RdkitReactionCoercible | SqlExpression
AnyRdkitFingerprintLike: TypeAlias = bytes | SqlExpression

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
