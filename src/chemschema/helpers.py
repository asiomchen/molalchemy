from chemschema.bingo import (
    BingoBinaryMol,
    BingoMol,
    BingoReaction,
    BingoBinaryReaction,
)
from chemschema.bingo.proxy import BingoRxnProxy, BingoMolProxy
from sqlalchemy import Column
from sqlalchemy.orm.attributes import InstrumentedAttribute


def bingo_col(column: Column) -> BingoMolProxy:
    if isinstance(column, (InstrumentedAttribute, Column)):
        if isinstance(column.type, BingoMol) or isinstance(column.type, BingoBinaryMol):
            return column
        else:
            raise TypeError("Column is not of type BingoMol or BingoBinaryMol")
    else:
        raise TypeError(
            f"Input is not a SQLAlchemy Column or InstrumentedAttribute, got {type(column)}"
        )


def bingo_rxn_col(column: Column) -> BingoRxnProxy:
    if isinstance(column, (InstrumentedAttribute, Column)):
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
            f"Input is not a SQLAlchemy InstrumentedAttribute or Column, got {type(column)}"
        )
