from typing import Literal

from sqlalchemy.types import UserDefinedType


class RdkitMolComparator(UserDefinedType.Comparator):
    def has_substructure(self, query):
        """Check if this molecule contains `query` as a substructure (@>)."""
        return self.expr.op("@>")(query)

    def is_substructure_of(self, query):
        """Check if this molecule is a substructure of `query` (<@)."""
        return self.expr.op("<@")(query)

    def equals(self, query):
        """Check if this molecule is equal to `query` (@=)."""
        return self.expr.op("@=")(query)


class RdkitFPComparator(UserDefinedType.Comparator):
    def nearest_neighbors(self, query, type: Literal["tanimoto", "dice"] = "tanimoto"):
        if type == "tanimoto":
            return self.expr.op("<%>")(query)
        else:  # dice
            return self.expr.op("<#>")(query)

    def tanimoto(self, query_fp):
        """Tanimoto similarity threshold operator (%).

        Returns whether or not the Tanimoto similarity between two fingerprints
        (either two sfp or two bfp values) exceeds rdkit.tanimoto_threshold.
        """
        return self.expr.op("%")(query_fp)

    def dice(self, query_fp):
        """Dice similarity threshold operator (#).

        Returns whether or not the Dice similarity between two fingerprints
        (either two sfp or two bfp values) exceeds rdkit.dice_threshold.
        """
        return self.expr.op("#")(query_fp)
