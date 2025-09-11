from chemschema.bingo import (
    BingoBinaryMol,
    BingoMol,
    BingoReaction,
    BingoBinaryReaction,
)
from chemschema.bingo.proxy import BingoMolProxy, BingoRxnProxy
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


def bingo_rxn_col(column: InstrumentedAttribute) -> BingoRxnProxy:
    if isinstance(column, InstrumentedAttribute):
        if isinstance(column.type, BingoReaction) or isinstance(
            column.type, BingoBinaryReaction
        ):
            return column
        else:
            raise TypeError(
                "Column is not of type BingoReaction or BingoBinaryReaction"
            )
    else:
        raise TypeError(
            f"Input is not a SQLAlchemy InstrumentedAttribute, got {type(column)}"
        )
