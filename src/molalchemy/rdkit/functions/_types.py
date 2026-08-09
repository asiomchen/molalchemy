"""Operand aliases for RDKit cartridge function wrappers."""

from typing import Any, TypeAlias, TypeVar

from rdkit import Chem
from rdkit.Chem.rdChemReactions import ChemicalReaction

from molalchemy.protocols import (
    RdkitFingerprintSqlOperand,
    RdkitMolSqlOperand,
    RdkitReactionSqlOperand,
    SqlOperand,
)

T = TypeVar("T")
SQLAlchemyCoercible: TypeAlias = SqlOperand[T]
SqlExpression: TypeAlias = SqlOperand[Any]
LiteralStrBytes: TypeAlias = str | bytes
TextLike: TypeAlias = str | bytes | SqlExpression

RdkitMolCoercible: TypeAlias = str | Chem.Mol
AnyRdkitMolLike: TypeAlias = RdkitMolCoercible | RdkitMolSqlOperand
RdkitQMolCoercible: TypeAlias = str
AnyRdkitQMolLike: TypeAlias = str | SqlOperand[str]
RdkitXQMolCoercible: TypeAlias = str
AnyRdkitXQMolLike: TypeAlias = str | SqlOperand[str]
RdkitBitFingerprintCoercible: TypeAlias = bytes
AnyRdkitBitFingerprintLike: TypeAlias = bytes | RdkitFingerprintSqlOperand
RdkitSparseFingerprintCoercible: TypeAlias = bytes
AnyRdkitSparseFingerprintLike: TypeAlias = bytes | RdkitFingerprintSqlOperand
RdkitReactionCoercible: TypeAlias = str | ChemicalReaction
AnyRdkitReactionLike: TypeAlias = RdkitReactionCoercible | RdkitReactionSqlOperand
AnyRdkitFingerprintLike: TypeAlias = bytes | RdkitFingerprintSqlOperand

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
