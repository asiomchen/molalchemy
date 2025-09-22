import pytest
from sqlalchemy import BINARY, Column, String

from molalchemy.bingo.types import (
    BingoBinaryMol,
    BingoBinaryReaction,
    BingoMol,
    BingoReaction,
)
from molalchemy.helpers import bingo_col, bingo_rxn_col


@pytest.fixture(params=[BingoMol, BingoBinaryMol])
def good_bingo_mol_col(request: pytest.FixtureRequest):
    column_type = request.param
    return Column("structure", column_type)


@pytest.fixture(params=[BingoReaction, BingoBinaryReaction])
def good_bingo_rxn_col(request: pytest.FixtureRequest):
    column_type = request.param
    return Column("reaction", column_type)


@pytest.mark.parametrize("bad_type", [String, BINARY])
def test_bingo_mol_col_type_error(bad_type):
    col = Column("bad_structure", bad_type)
    with pytest.raises(
        TypeError, match="Column is not of type BingoMol or BingoBinaryMol"
    ):
        bingo_col(col)


@pytest.mark.parametrize("bad_type", [String, BINARY])
def test_bingo_rxn_col_type_error(bad_type):
    col = Column("bad_reaction", bad_type)
    with pytest.raises(
        TypeError, match="Column is not of type BingoReaction or BingoBinaryReaction"
    ):
        bingo_rxn_col(col)


def test_bingo_mol_col_invalid_input():
    with pytest.raises(
        TypeError, match="Input is not a SQLAlchemy Column or InstrumentedAttribute"
    ):
        bingo_col("not_a_column")


def test_bingo_rxn_col_invalid_input():
    with pytest.raises(
        TypeError, match="Input is not a SQLAlchemy InstrumentedAttribute or Column"
    ):
        bingo_rxn_col(123)


def test_bingo_mol_col_success(good_bingo_mol_col):
    result = bingo_col(good_bingo_mol_col)
    assert result is good_bingo_mol_col
