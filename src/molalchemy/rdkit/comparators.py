from typing import Any, Literal

from sqlalchemy import ColumnElement
from sqlalchemy.sql import cast, func
from sqlalchemy.types import UserDefinedType

from molalchemy.types import CString


class RdkitMolComparator(UserDefinedType.Comparator):
    def __eq__(self, other: Any) -> ColumnElement[bool]:
        # Native RDKit mol "=" is already chemical equality; keep "==" mapped to
        # equals() for explicit comparator parity with Bingo and reactions.
        if isinstance(other, ColumnElement) and not getattr(
            other, "is_clause_element", False
        ):
            return super().__eq__(other)
        if (
            isinstance(other, ColumnElement)
            and getattr(other, "table", None) is not None
        ):
            return super().__eq__(other)
        return self.equals(other)

    def has_substructure(self, query: Any) -> ColumnElement[bool]:
        """Check if this molecule contains `query` as a substructure (@>)."""
        return self.expr.op("@>")(query)

    def has_smarts(self, query: Any) -> ColumnElement[bool]:
        """Check if this molecule contains SMARTS pattern `query`."""
        return self.has_substructure(func.qmol_from_smarts(cast(query, CString)))

    def is_substructure_of(self, query: Any) -> ColumnElement[bool]:
        """Check if this molecule is a substructure of `query` (<@)."""
        return self.expr.op("<@")(query)

    def equals(self, query: Any) -> ColumnElement[bool]:
        """Check if this molecule is equal to `query` (@=)."""
        return self.expr.op("@=")(query)

    def not_equals(self, query: Any) -> ColumnElement[bool]:
        """Check if this molecule is not equal to `query` (@<>)."""
        return self.expr.op("@<>")(query)

    def has_query_substructure(self, query: Any) -> ColumnElement[bool]:
        """Check if this molecule contains a query substructure `query` (@>>)."""
        return self.expr.op("@>>")(query)

    def is_query_substructure_of(self, query: Any) -> ColumnElement[bool]:
        """Check if query structure `query` contains this molecule (<<@)."""
        return self.expr.op("<<@")(query)


class RdkitReactionComparator(UserDefinedType.Comparator):
    def __eq__(self, other: Any) -> ColumnElement[bool]:
        if isinstance(other, ColumnElement) and not getattr(
            other, "is_clause_element", False
        ):
            return super().__eq__(other)
        if (
            isinstance(other, ColumnElement)
            and getattr(other, "table", None) is not None
        ):
            return super().__eq__(other)
        return self.equals(other)

    def has_substructure(self, query: Any) -> ColumnElement[bool]:
        """Check if this reaction contains `query` as a substructure (@>)."""
        return self.expr.op("@>")(query)

    def is_substructure_of(self, query: Any) -> ColumnElement[bool]:
        """Check if this reaction is a substructure of `query` (<@)."""
        return self.expr.op("<@")(query)

    def equals(self, query: Any) -> ColumnElement[bool]:
        """Check if this reaction is equal to `query` (@=)."""
        return self.expr.op("@=")(query)

    def not_equals(self, query: Any) -> ColumnElement[bool]:
        """Check if this reaction is not equal to `query` (@<>)."""
        return self.expr.op("@<>")(query)

    def has_smarts(self, query: Any) -> ColumnElement[bool]:
        """Check if this reaction contains SMARTS pattern `query`."""
        return func.substruct(
            self.expr, func.reaction_from_smarts(cast(query, CString))
        )

    def has_substructure_fp(self, query: Any) -> ColumnElement[bool]:
        """Check if this reaction matches `query` via substructure fingerprints (?>)."""
        return self.expr.op("?>")(query)

    def is_substructure_fp_of(self, query: Any) -> ColumnElement[bool]:
        """Check if this reaction is fingerprint-substructure of `query` (?<)."""
        return self.expr.op("?<")(query)


class RdkitFPComparator(UserDefinedType.Comparator):
    def nearest_neighbors(
        self, query: ColumnElement, type: Literal["tanimoto", "dice"] = "tanimoto"
    ) -> ColumnElement[bool]:
        if type == "tanimoto":
            return self.expr.op("<%>")(query)
        else:  # dice
            return self.expr.op("<#>")(query)

    def tanimoto(self, query_fp: ColumnElement) -> ColumnElement[bool]:
        """Tanimoto similarity threshold operator (%).

        Returns whether or not the Tanimoto similarity between two fingerprints
        (either two sfp or two bfp values) exceeds rdkit.tanimoto_threshold.
        """
        return self.expr.op("%")(query_fp)

    def dice(self, query_fp: ColumnElement) -> ColumnElement[bool]:
        """Dice similarity threshold operator (#).

        Returns whether or not the Dice similarity between two fingerprints
        (either two sfp or two bfp values) exceeds rdkit.dice_threshold.
        """
        return self.expr.op("#")(query_fp)
