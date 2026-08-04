"""Typed interfaces for cartridge-aware SQLAlchemy columns.

SQLAlchemy exposes custom comparator methods dynamically at runtime.  These
protocols provide a precise static view for the validation helpers in
``molalchemy.helpers``.
"""

from typing import Any, Protocol, TypeAlias

from rdkit import Chem
from rdkit.Chem.rdChemReactions import ChemicalReaction
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.elements import ColumnElement

SqlOperand: TypeAlias = ColumnElement[Any] | InstrumentedAttribute[Any]
RdkitMolOperand: TypeAlias = str | Chem.Mol | SqlOperand
RdkitReactionOperand: TypeAlias = str | ChemicalReaction | SqlOperand
RdkitFingerprintOperand: TypeAlias = bytes | SqlOperand
BingoOperand: TypeAlias = str | bytes | SqlOperand
BingoParameters: TypeAlias = str | SqlOperand
BingoSimilarityBound: TypeAlias = float | SqlOperand


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
    def has_smarts(self, query: str | SqlOperand) -> ColumnElement[bool]: ...
    def is_substructure_of(self, query: RdkitMolOperand) -> ColumnElement[bool]: ...
    def equals(self, query: RdkitMolOperand) -> ColumnElement[bool]: ...
    def not_equals(self, query: RdkitMolOperand) -> ColumnElement[bool]: ...
    def has_query_substructure(self, query: SqlOperand) -> ColumnElement[bool]: ...
    def is_query_substructure_of(self, query: SqlOperand) -> ColumnElement[bool]: ...


class RdkitReactionColumn(Protocol):
    def has_substructure(self, query: RdkitReactionOperand) -> ColumnElement[bool]: ...

    def is_substructure_of(
        self, query: RdkitReactionOperand
    ) -> ColumnElement[bool]: ...

    def equals(self, query: RdkitReactionOperand) -> ColumnElement[bool]: ...
    def not_equals(self, query: RdkitReactionOperand) -> ColumnElement[bool]: ...
    def has_smarts(self, query: str | SqlOperand) -> ColumnElement[bool]: ...
    def has_substructure_fp(
        self, query: RdkitReactionOperand
    ) -> ColumnElement[bool]: ...

    def is_substructure_fp_of(
        self, query: RdkitReactionOperand
    ) -> ColumnElement[bool]: ...


class RdkitFingerprintColumn(Protocol):
    def tanimoto_matches(
        self, query: RdkitFingerprintOperand
    ) -> ColumnElement[bool]: ...

    def dice_matches(self, query: RdkitFingerprintOperand) -> ColumnElement[bool]: ...
    def tanimoto_distance(
        self, query: RdkitFingerprintOperand
    ) -> ColumnElement[float]: ...

    def dice_distance(self, query: RdkitFingerprintOperand) -> ColumnElement[float]: ...


__all__ = [
    "BingoMolColumn",
    "BingoOperand",
    "BingoParameters",
    "BingoReactionColumn",
    "BingoSimilarityBound",
    "RdkitFingerprintColumn",
    "RdkitFingerprintOperand",
    "RdkitMolColumn",
    "RdkitMolOperand",
    "RdkitReactionColumn",
    "RdkitReactionOperand",
    "SqlOperand",
]
