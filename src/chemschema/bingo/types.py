from sqlalchemy.types import UserDefinedType
from chemschema.bingo.comparators import BingoMolComparator


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
