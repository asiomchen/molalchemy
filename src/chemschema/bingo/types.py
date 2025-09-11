from sqlalchemy.types import UserDefinedType
from chemschema.bingo.comparators import BingoMolComparator, BingoRxnComparator


class BingoMol(UserDefinedType):
    cache_ok = True
    comparator_factory = BingoMolComparator

    def get_col_spec(self):
        return "varchar"


class BingoBinaryMol(UserDefinedType):
    cache_ok = True
    comparator_factory = BingoMolComparator

    def get_col_spec(self):
        return "bytea"


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
