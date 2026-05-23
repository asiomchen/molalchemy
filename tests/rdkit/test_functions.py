"""Tests for RDKit functions."""

import pytest
from sqlalchemy import (
    BinaryExpression,
    Column,
    Function,
    Integer,
    MetaData,
    Table,
    select,
)
from sqlalchemy.dialects import postgresql

from molalchemy.rdkit import functions as rdkit_func
from molalchemy.rdkit.types import RdkitMol

all_funcs = rdkit_func.__all__


@pytest.mark.parametrize("func", all_funcs)
def test_any_function_returns_function_object(func):
    """Test that any function returns a SQLAlchemy function object."""
    random_args = ["CCO"] * 10
    random_columns = [Column("dummy", RdkitMol())] * 10
    if callable(func):
        try:
            result = func(*random_args[: func.__code__.co_argcount])
            assert isinstance(result, Function)
        except AttributeError:
            result = func(*random_columns[: func.__code__.co_argcount])
            assert isinstance(result, BinaryExpression)


@pytest.mark.parametrize(
    ("helper_name", "query", "operator"),
    [
        ("mol_has_substructure", "c1ccccc1", "@>"),
        ("mol_is_substructure_of", "CCOCC", "<@"),
        ("mol_equals", "CCO", "@="),
    ],
)
def test_molecule_search_helpers_compile_to_expected_operators(
    helper_name, query, operator
):
    """Each molecule comparator search operation has a standalone helper."""
    structures = Table(
        "structures",
        MetaData(),
        Column("id", Integer),
        Column("structure", RdkitMol()),
    )

    helper = getattr(rdkit_func, helper_name)
    stmt = select(structures).where(helper(structures.c.structure, query))

    compiled = stmt.compile(dialect=postgresql.dialect())
    sql = str(compiled)

    assert operator in sql
    assert query in compiled.params.values()
