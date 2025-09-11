from chemschema.bingo import BingoBinaryMol, BingoMol
from chemschema.bingo.functions import BingoMolProxy
from sqlalchemy.orm.attributes import InstrumentedAttribute


def bingo_col(column: InstrumentedAttribute) -> BingoMolProxy:
    if isinstance(column, InstrumentedAttribute):
        if isinstance(column.type, BingoMol) or isinstance(column.type, BingoBinaryMol):
            return column
        else:
            raise TypeError("Column is not of type BingoMol or BingoBinaryMol")
    else:
        raise TypeError(
            f"Input is not a SQLAlchemy InstrumentedAttribute, got {type(column)}"
        )
