from typing import Any, cast

from sqlalchemy import ColumnElement
from sqlalchemy.types import UserDefinedType

from molalchemy.protocols import (
    RdkitFingerprintOperand,
    RdkitMolOperand,
    RdkitReactionOperand,
    SqlOperand,
)
from molalchemy.rdkit.search import (
    _rdkit_distance,
    _rdkit_mol_smarts,
    _rdkit_predicate,
    _rdkit_rxn_smarts,
)


class RdkitMolComparator(UserDefinedType.Comparator):
    def has_substructure(self, query: RdkitMolOperand) -> ColumnElement[bool]:
        """Check if this molecule contains `query` as a substructure (@>)."""
        return _rdkit_predicate(self.expr, "@>", query)

    def has_smarts(self, query: str | SqlOperand) -> ColumnElement[bool]:
        """Check if this molecule contains SMARTS pattern `query`."""
        return _rdkit_mol_smarts(self.expr, query)

    def is_substructure_of(self, query: RdkitMolOperand) -> ColumnElement[bool]:
        """Check if this molecule is a substructure of `query` (<@)."""
        return _rdkit_predicate(self.expr, "<@", query)

    def equals(self, query: RdkitMolOperand) -> ColumnElement[bool]:
        """Check chemical equality using `@=` (an alias of `=`, both use `mol_eq`)."""
        return _rdkit_predicate(self.expr, "@=", query)

    def not_equals(self, query: RdkitMolOperand) -> ColumnElement[bool]:
        """Check chemical inequality using `@<>` (an alias of `<>`/`mol_ne`)."""
        return _rdkit_predicate(self.expr, "@<>", query)

    def has_query_substructure(self, query: SqlOperand) -> ColumnElement[bool]:
        """Check if this molecule contains a query substructure `query` (@>>)."""
        return _rdkit_predicate(self.expr, "@>>", query)

    def is_query_substructure_of(self, query: SqlOperand) -> ColumnElement[bool]:
        """Apply the reverse query-substructure spelling (`query <<@ molecule`)."""
        # RDKit declares this reverse operator as qmol/xqmol <<@ mol, unlike
        # the forward mol @>> qmol spelling.
        return _rdkit_predicate(cast(ColumnElement[Any], query), "<<@", self.expr)


class RdkitReactionComparator(UserDefinedType.Comparator):
    def has_substructure(self, query: RdkitReactionOperand) -> ColumnElement[bool]:
        """Check if this reaction contains `query` as a substructure (@>)."""
        return _rdkit_predicate(self.expr, "@>", query)

    def is_substructure_of(self, query: RdkitReactionOperand) -> ColumnElement[bool]:
        """Check if this reaction is a substructure of `query` (<@)."""
        return _rdkit_predicate(self.expr, "<@", query)

    def equals(self, query: RdkitReactionOperand) -> ColumnElement[bool]:
        """Check if this reaction is equal to `query` (@=)."""
        return _rdkit_predicate(self.expr, "@=", query)

    def not_equals(self, query: RdkitReactionOperand) -> ColumnElement[bool]:
        """Check if this reaction is not equal to `query` (@<>)."""
        return _rdkit_predicate(self.expr, "@<>", query)

    def has_smarts(self, query: str | SqlOperand) -> ColumnElement[bool]:
        """Check if this reaction contains SMARTS pattern `query`."""
        return _rdkit_rxn_smarts(self.expr, query)

    def has_substructure_fp(self, query: RdkitReactionOperand) -> ColumnElement[bool]:
        """Check if this reaction matches `query` via substructure fingerprints (?>)."""
        return _rdkit_predicate(self.expr, "?>", query)

    def is_substructure_fp_of(self, query: RdkitReactionOperand) -> ColumnElement[bool]:
        """Check if this reaction is fingerprint-substructure of `query` (?<)."""
        return _rdkit_predicate(self.expr, "?<", query)


class RdkitFPComparator(UserDefinedType.Comparator):
    def tanimoto_matches(self, query: RdkitFingerprintOperand) -> ColumnElement[bool]:
        """Tanimoto similarity threshold operator (%).

        Returns whether or not the Tanimoto similarity between two fingerprints
        (either two sfp or two bfp values) exceeds rdkit.tanimoto_threshold.
        """
        return _rdkit_predicate(self.expr, "%", query)

    def dice_matches(self, query: RdkitFingerprintOperand) -> ColumnElement[bool]:
        """Dice similarity threshold operator (#).

        Returns whether or not the Dice similarity between two fingerprints
        (either two sfp or two bfp values) exceeds rdkit.dice_threshold.
        """
        return _rdkit_predicate(self.expr, "#", query)

    def tanimoto_distance(self, query: RdkitFingerprintOperand) -> ColumnElement[float]:
        """Return the Tanimoto KNN distance to `query` (`<%>`)."""
        return _rdkit_distance(self.expr, "<%>", query)

    def dice_distance(self, query: RdkitFingerprintOperand) -> ColumnElement[float]:
        """Return the Dice KNN distance to `query` (`<#>`)."""
        return _rdkit_distance(self.expr, "<#>", query)
