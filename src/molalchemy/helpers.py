from sqlalchemy import Column
from sqlalchemy.orm.attributes import InstrumentedAttribute

from molalchemy.bingo import (
    BingoBinaryMol,
    BingoBinaryReaction,
    BingoMol,
    BingoReaction,
)
from molalchemy.bingo.proxy import BingoMolProxy, BingoRxnProxy


def bingo_col(column: Column | InstrumentedAttribute) -> BingoMolProxy:
    """
    Create a Bingo molecule proxy from a SQLAlchemy column. It is a way to trick IDE into showing
    syntax highlighting and autocompletion for the molecular column operations provided by custom Comparator.

    This function validates that the input column has a compatible Bingo molecule type
    and returns a proxy object that can be used for molecule-specific operations.

    Parameters
    ----------
    column : sqlalchemy.Column | sqlalchemy.orm.attributes.InstrumentedAttribute
        A SQLAlchemy column that should be of type `molalchemy.bingo.types.BingoMol`
        or `molalchemy.bingo.types.BingoBinaryMol`.

    Returns
    -------
    molalchemy.bingo.proxy.BingoMolProxy
        A proxy object for performing Bingo molecule operations on the column.

    Raises
    ------
    TypeError
        If the column is not a SQLAlchemy Column or InstrumentedAttribute, or if
        the column type is not `molalchemy.bingo.types.BingoMol` or
        `molalchemy.bingo.types.BingoBinaryMol`.
    """
    if isinstance(column, InstrumentedAttribute | Column):
        if isinstance(column.type, BingoMol) or isinstance(column.type, BingoBinaryMol):
            return column
        else:
            raise TypeError("Column is not of type BingoMol or BingoBinaryMol")
    else:
        raise TypeError(
            f"Input is not a SQLAlchemy Column or InstrumentedAttribute, got {type(column)}"
        )


def bingo_rxn_col(column: Column | InstrumentedAttribute) -> BingoRxnProxy:
    """
    Create a Bingo reaction proxy from a SQLAlchemy column. It is a way to trick IDE into showing
    syntax highlighting and autocompletion for the reaction column operations provided by custom Comparator.

    This function validates that the input column has a compatible Bingo reaction type
    and returns a proxy object that can be used for reaction-specific operations.

    Parameters
    ----------
    column : sqlalchemy.Column
        A SQLAlchemy column that should be of type `molalchemy.bingo.types.BingoReaction`
        or `molalchemy.bingo.types.BingoBinaryReaction`.

    Returns
    -------
    molalchemy.bingo.proxy.BingoRxnProxy
        A proxy object for performing Bingo reaction operations on the column.

    Raises
    ------
    TypeError
        If the column is not a SQLAlchemy Column or InstrumentedAttribute, or if
        the column type is not `molalchemy.bingo.types.BingoReaction` or
        `molalchemy.bingo.types.BingoBinaryReaction`.
    """
    if isinstance(column, InstrumentedAttribute | Column):
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
