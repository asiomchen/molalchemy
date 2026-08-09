"""Typed interfaces for cartridge-aware SQLAlchemy columns.

SQLAlchemy exposes custom comparator methods dynamically at runtime.  These
protocols provide a precise static view for the validation helpers in
``molalchemy.helpers``.
"""

from typing import Any, Literal, Protocol, TypeAlias, TypeVar

from rdkit import Chem
from rdkit.Chem.rdChemReactions import ChemicalReaction
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.elements import ColumnElement

_T = TypeVar("_T")

SqlOperand: TypeAlias = ColumnElement[_T] | InstrumentedAttribute[_T]
BooleanOperand: TypeAlias = bool | SqlOperand[bool]
IntegerOperand: TypeAlias = int | SqlOperand[int]
FloatOperand: TypeAlias = float | SqlOperand[float]
TextOperand: TypeAlias = str | SqlOperand[str]
BinaryOperand: TypeAlias = bytes | SqlOperand[bytes]
TextOrBinaryOperand: TypeAlias = TextOperand | BinaryOperand
BingoMolSqlOperand: TypeAlias = SqlOperand[str] | SqlOperand[bytes]
BingoReactionSqlOperand: TypeAlias = SqlOperand[str] | SqlOperand[bytes]
RdkitMolSqlOperand: TypeAlias = (
    SqlOperand[str] | SqlOperand[bytes] | SqlOperand[Chem.Mol]
)
RdkitReactionSqlOperand: TypeAlias = (
    SqlOperand[str] | SqlOperand[bytes] | SqlOperand[ChemicalReaction]
)
RdkitFingerprintSqlOperand: TypeAlias = SqlOperand[bytes]
RdkitMolOperand: TypeAlias = str | Chem.Mol | RdkitMolSqlOperand
RdkitReactionOperand: TypeAlias = str | ChemicalReaction | RdkitReactionSqlOperand
RdkitFingerprintOperand: TypeAlias = bytes | RdkitFingerprintSqlOperand
RdkitSimilarityMetric: TypeAlias = Literal["Tanimoto", "Dice"]
RdkitSimilarityBound: TypeAlias = float | None | SqlOperand[Any]
BingoOperand: TypeAlias = str | bytes | BingoMolSqlOperand
BingoParameters: TypeAlias = str | SqlOperand[Any]
BingoSimilarityBound: TypeAlias = float | None | SqlOperand[Any]


class BingoMolColumn(Protocol):
    def has_substructure(
        self, query: BingoOperand, parameters: BingoParameters = ""
    ) -> ColumnElement[bool]: ...

    def has_smarts(
        self, query: BingoOperand, parameters: BingoParameters = ""
    ) -> ColumnElement[bool]: ...

    def equals(
        self, query: BingoOperand, parameters: BingoParameters = ""
    ) -> ColumnElement[bool]: ...

    def not_equals(
        self, query: BingoOperand, parameters: BingoParameters = ""
    ) -> ColumnElement[bool]: ...

    def similar_to(
        self,
        query: BingoOperand,
        minimum: BingoSimilarityBound = 0.0,
        maximum: BingoSimilarityBound = 1.0,
        metric: BingoParameters = "Tanimoto",
    ) -> ColumnElement[bool]: ...

    def similarity_score(
        self,
        query: BingoOperand,
        metric: BingoParameters = "Tanimoto",
    ) -> ColumnElement[float]: ...


class BingoReactionColumn(Protocol):
    def has_substructure(
        self, query: BingoOperand, parameters: BingoParameters = ""
    ) -> ColumnElement[bool]: ...

    def has_smarts(
        self, query: BingoOperand, parameters: BingoParameters = ""
    ) -> ColumnElement[bool]: ...

    def equals(
        self, query: BingoOperand, parameters: BingoParameters = ""
    ) -> ColumnElement[bool]: ...

    def not_equals(
        self, query: BingoOperand, parameters: BingoParameters = ""
    ) -> ColumnElement[bool]: ...


class RdkitMolColumn(Protocol):
    def has_substructure(self, query: RdkitMolOperand) -> ColumnElement[bool]: ...
    def has_smarts(self, query: str | SqlOperand[Any]) -> ColumnElement[bool]: ...
    def is_substructure_of(self, query: RdkitMolOperand) -> ColumnElement[bool]: ...
    def equals(self, query: RdkitMolOperand) -> ColumnElement[bool]: ...
    def not_equals(self, query: RdkitMolOperand) -> ColumnElement[bool]: ...
    def has_query_substructure(self, query: SqlOperand[Any]) -> ColumnElement[bool]: ...
    def is_query_substructure_of(
        self, query: SqlOperand[Any]
    ) -> ColumnElement[bool]: ...


class RdkitReactionColumn(Protocol):
    def has_substructure(self, query: RdkitReactionOperand) -> ColumnElement[bool]: ...

    def is_substructure_of(
        self, query: RdkitReactionOperand
    ) -> ColumnElement[bool]: ...

    def equals(self, query: RdkitReactionOperand) -> ColumnElement[bool]: ...
    def not_equals(self, query: RdkitReactionOperand) -> ColumnElement[bool]: ...
    def has_smarts(self, query: str | SqlOperand[Any]) -> ColumnElement[bool]: ...
    def has_substructure_fp(
        self, query: RdkitReactionOperand
    ) -> ColumnElement[bool]: ...

    def is_substructure_fp_of(
        self, query: RdkitReactionOperand
    ) -> ColumnElement[bool]: ...


class RdkitFingerprintColumn(Protocol):
    def similar_to(
        self,
        query: RdkitFingerprintOperand,
        minimum: RdkitSimilarityBound = 0.0,
        maximum: RdkitSimilarityBound = 1.0,
        metric: RdkitSimilarityMetric = "Tanimoto",
    ) -> ColumnElement[bool]: ...

    def similarity_score(
        self,
        query: RdkitFingerprintOperand,
        metric: RdkitSimilarityMetric = "Tanimoto",
    ) -> ColumnElement[float]: ...

    def tanimoto_matches(
        self, query: RdkitFingerprintOperand
    ) -> ColumnElement[bool]: ...

    def dice_matches(self, query: RdkitFingerprintOperand) -> ColumnElement[bool]: ...
    def tanimoto_distance(
        self, query: RdkitFingerprintOperand
    ) -> ColumnElement[float]: ...

    def dice_distance(self, query: RdkitFingerprintOperand) -> ColumnElement[float]: ...


__all__ = [
    "BinaryOperand",
    "BingoMolColumn",
    "BingoMolSqlOperand",
    "BingoOperand",
    "BingoParameters",
    "BingoReactionColumn",
    "BingoReactionSqlOperand",
    "BingoSimilarityBound",
    "BooleanOperand",
    "FloatOperand",
    "IntegerOperand",
    "RdkitFingerprintColumn",
    "RdkitFingerprintOperand",
    "RdkitFingerprintSqlOperand",
    "RdkitMolColumn",
    "RdkitMolOperand",
    "RdkitMolSqlOperand",
    "RdkitReactionColumn",
    "RdkitReactionOperand",
    "RdkitReactionSqlOperand",
    "RdkitSimilarityBound",
    "RdkitSimilarityMetric",
    "SqlOperand",
    "TextOperand",
    "TextOrBinaryOperand",
]
