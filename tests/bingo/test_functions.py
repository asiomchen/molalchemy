"""Tests for bingo functions."""

import pytest
from sqlalchemy import (
    BinaryExpression,
    Column,
    Function,
)

from molalchemy.bingo import functions as bingo_func
from molalchemy.bingo.types import BingoMol

all_funcs = bingo_func.__all__


@pytest.mark.parametrize("func", all_funcs)
def test_any_function_returns_function_object(func):
    """Test that any function returns a SQLAlchemy function object."""
    random_args = ["CCO"] * 10
    random_columns = [Column("dummy", BingoMol())] * 10
    if callable(func):
        try:
            result = func(*random_args[: func.__code__.co_argcount])
            assert isinstance(result, Function)
        except AttributeError:
            result = func(*random_columns[: func.__code__.co_argcount])
            assert isinstance(result, BinaryExpression)
