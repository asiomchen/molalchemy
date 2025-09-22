from typing import Literal

from sqlalchemy.types import UserDefinedType


class RdkitMolComparator(UserDefinedType.Comparator):
    def has_substructure(self, query):
        return self.expr.op("@>")(query)

    def equals(self, query):
        return self.expr.op("@=")(query)


class RdkitFPComparator(UserDefinedType.Comparator):
    def nearest_neighbors(self, query, type: Literal["tanimoto", "dice"] = "tanimoto"):
        if type == "tanimoto":
            return self.expr.op("<%>")(query)
        else:  # dice
            return self.expr.op("<#>")(query)

    def dice(self, query_fp):
        """
        operator used for similarity searches using Dice similarity.
        Returns whether or not the Dice similarity between two fingerprints (either two sfp or two bfp values) exceeds rdkit.dice_threshold.
        """
        return self.expr.op("#")(query_fp)
