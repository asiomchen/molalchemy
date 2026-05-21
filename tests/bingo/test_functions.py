"""Tests for bingo functions."""

import pytest
from sqlalchemy import (
    BinaryExpression,
    Column,
    Function,
    Integer,
    MetaData,
    String,
    Table,
    bindparam,
    select,
)
from sqlalchemy.dialects import postgresql

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


def test_bingo_search_helpers_bind_literal_inputs():
    """Search helper literals must compile as bind parameters, not SQL text."""
    compounds = Table(
        "compounds",
        MetaData(),
        Column("id", Integer),
        Column("structure", BingoMol()),
    )
    injected_query = "x' OR 1=1 --"

    stmt = select(compounds).where(
        bingo_func.has_substructure(compounds.c.structure, injected_query)
    )

    compiled = stmt.compile(dialect=postgresql.dialect())
    sql = str(compiled)

    assert injected_query not in sql
    assert "bingo.sub" in sql
    assert "CAST" in sql
    assert injected_query in compiled.params.values()


def test_bingo_search_helpers_preserve_bindparam_inputs():
    """Explicit bind parameters should remain bind parameters in generated SQL."""
    compounds = Table(
        "compounds",
        MetaData(),
        Column("id", Integer),
        Column("structure", BingoMol()),
    )

    stmt = select(compounds).where(
        bingo_func.mol_equals(compounds.c.structure, bindparam("query_mol"))
    )

    compiled = stmt.compile(dialect=postgresql.dialect())
    sql = str(compiled)

    assert "%(query_mol)s" in sql
    assert "':query_mol'" not in sql
    assert "bingo.exact" in sql


def test_bingo_similarity_preserves_column_expression_inputs():
    """Column expressions should compile as columns, not stringified values."""
    compounds = Table(
        "compounds",
        MetaData(),
        Column("id", Integer),
        Column("structure", BingoMol()),
        Column("query_structure", String),
    )

    stmt = select(compounds).where(
        bingo_func.similarity(
            compounds.c.structure,
            compounds.c.query_structure,
            0.2,
            0.9,
            "Dice",
        )
    )

    compiled = stmt.compile(
        dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
    )
    sql = str(compiled)

    assert "0.2, 0.9, compounds.query_structure" in sql
    assert "'compounds.query_structure'" not in sql
    assert " @ " in sql
    assert "bingo.sim" in sql
