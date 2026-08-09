"""Operand aliases for Bingo cartridge function wrappers."""

from typing import Any, TypeAlias, TypeVar

from molalchemy.protocols import SqlOperand

T = TypeVar("T")
SQLAlchemyCoercible: TypeAlias = SqlOperand[T]
SqlExpression: TypeAlias = SqlOperand[Any]
LiteralStrBytes: TypeAlias = str | bytes
TextLike: TypeAlias = str | bytes | SqlExpression

BingoMolCoercible: TypeAlias = str
AnyBingoMolLike: TypeAlias = str | SqlExpression
BingoBinaryMolCoercible: TypeAlias = str | bytes
AnyBingoBinaryMolLike: TypeAlias = str | bytes | SqlExpression
BingoReactionCoercible: TypeAlias = str
AnyBingoReactionLike: TypeAlias = str | SqlExpression
BingoBinaryReactionCoercible: TypeAlias = str | bytes
AnyBingoBinaryReactionLike: TypeAlias = str | bytes | SqlExpression
AnyBingoMolLikeCombined: TypeAlias = str | bytes | SqlExpression
AnyBingoReactionLikeCombined: TypeAlias = str | bytes | SqlExpression

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
