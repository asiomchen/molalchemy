from sqlalchemy.types import UserDefinedType
from chemschema.bingo.comparators import BingoMolComparator, BingoRxnComparator
from .functions import bingo_func
from typing import Literal


class BingoMol(UserDefinedType):
    cache_ok = True
    comparator_factory = BingoMolComparator

    def get_col_spec(self):
        return "varchar"


class BingoBinaryMol(UserDefinedType):
    cache_ok = True
    comparator_factory = BingoMolComparator

    def __init__(
        self,
        preserve_pos: bool = False,
        return_type: Literal["smiles", "molfile", "cml", "bytes"] = "smiles",
    ):
        self.preserve_pos = preserve_pos
        self.return_type = return_type
        super().__init__()

    def get_col_spec(self):
        return "bytea"

    def bind_expression(self, bindvalue):
        return bingo_func.to_binary(bindvalue, self.preserve_pos)

    def column_expression(self, col):
        if self.return_type == "smiles":
            return bingo_func.to_smiles(col)
        elif self.return_type == "molfile":
            return bingo_func.to_molfile(col)
        elif self.return_type == "cml":
            return bingo_func.to_cml(col)
        elif self.return_type == "bytes":
            return col
        else:
            raise ValueError(
                f"Invalid return_type: {self.return_type}. Available options are 'smiles', 'molfile', 'cml', 'bytes'."
            )


class BingoReaction(UserDefinedType):
    cache_ok = True
    comparator_factory = BingoRxnComparator

    def get_col_spec(self):
        return "varchar"


class BingoBinaryReaction(UserDefinedType):
    cache_ok = True
    comparator_factory = BingoRxnComparator

    def get_col_spec(self):
        return "bytea"
