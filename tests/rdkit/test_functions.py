"""Tests for RDKit functions."""

import pytest
from sqlalchemy import (
    BinaryExpression,
    Column,
    Function,
    Integer,
    MetaData,
    Table,
    bindparam,
    select,
)
from sqlalchemy.dialects import postgresql

from molalchemy.rdkit import functions as rdkit_func
from molalchemy.rdkit.types import RdkitMol, RdkitReaction

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


@pytest.mark.parametrize(
    ("helper_name", "query", "operator"),
    [
        ("rxn_has_substructure", "[C:1]>>[C:1][O]", "@>"),
        ("rxn_is_substructure_of", "[C:1][O]>>[C:1]", "<@"),
        ("rxn_equals", "[C:1]>>[C:1]", "@="),
        ("rxn_not_equals", "[C:1]>>[C:1][Cl]", "@<>"),
        ("rxn_has_substructure_fp", "[C:1]>>[C:1][Br]", "?>"),
        ("rxn_is_substructure_fp_of", "[C:1][Br]>>[C:1]", "?<"),
    ],
)
def test_reaction_search_helpers_compile_to_expected_operators(
    helper_name, query, operator
):
    """Live RDKit reaction operators are available as standalone helpers."""
    reactions = Table(
        "reactions",
        MetaData(),
        Column("id", Integer),
        Column("reaction", RdkitReaction()),
    )

    helper = getattr(rdkit_func, helper_name)
    stmt = select(reactions).where(helper(reactions.c.reaction, query))

    compiled = stmt.compile(dialect=postgresql.dialect())
    sql = str(compiled)

    assert operator in sql
    assert "reaction_from_smarts" in sql
    assert query in compiled.params.values()


def test_rxn_has_smarts_remains_function_backed():
    """SMARTS search stays distinct from operator-backed reaction substructure search."""
    reactions = Table(
        "reactions",
        MetaData(),
        Column("id", Integer),
        Column("reaction", RdkitReaction()),
    )

    stmt = select(reactions).where(
        rdkit_func.rxn_has_smarts(reactions.c.reaction, "[C:1]>>[C:1][O]")
    )

    compiled = stmt.compile(dialect=postgresql.dialect())
    sql = str(compiled)

    assert "substruct(" in sql
    assert "@>" not in sql


def test_reaction_search_helpers_preserve_bindparam_inputs():
    """Explicit reaction bind parameters should remain bind parameters."""
    reactions = Table(
        "reactions",
        MetaData(),
        Column("id", Integer),
        Column("reaction", RdkitReaction()),
    )

    stmt = select(reactions).where(
        rdkit_func.rxn_equals(reactions.c.reaction, bindparam("query_rxn"))
    )

    compiled = stmt.compile(dialect=postgresql.dialect())
    sql = str(compiled)

    assert "@=" in sql
    assert "reaction_from_smarts" in sql
    assert "%(query_rxn)s" in sql


def test_reaction_search_helpers_preserve_column_expression_inputs():
    """Reaction helpers should keep reaction-typed expressions as expressions."""
    reactions = Table(
        "reactions",
        MetaData(),
        Column("id", Integer),
        Column("reaction", RdkitReaction()),
        Column("query_reaction", RdkitReaction()),
    )

    stmt = select(reactions).where(
        rdkit_func.rxn_has_substructure(
            reactions.c.reaction, reactions.c.query_reaction
        )
    )

    compiled = str(
        stmt.compile(
            dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
        )
    )

    assert "reactions.query_reaction" in compiled
    assert "'reactions.query_reaction'" not in compiled
    assert "reaction_from_smarts" not in compiled
