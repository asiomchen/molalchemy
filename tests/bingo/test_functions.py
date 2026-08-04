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
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from molalchemy.bingo import functions as bingo_func
from molalchemy.bingo.types import BingoMol, BingoReaction

all_funcs = bingo_func.__all__


class Base(DeclarativeBase):
    pass


class Compound(Base):
    __tablename__ = "bingo_function_compounds"

    id: Mapped[int] = mapped_column(primary_key=True)
    structure: Mapped[str] = mapped_column(BingoMol())
    query_structure: Mapped[str] = mapped_column(BingoMol())
    query_parameters: Mapped[str] = mapped_column(String())


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
        bingo_func.mol_has_substructure(compounds.c.structure, injected_query)
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
        bingo_func.mol_similarity(
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


def test_bingo_search_helpers_preserve_orm_attribute_inputs():
    """Mapped attributes should use their SQL expression, not become literals."""
    stmt = select(Compound).where(
        bingo_func.mol_equals(
            Compound.structure,
            Compound.query_structure,
            Compound.query_parameters,
        )
    )

    compiled = str(stmt.compile(dialect=postgresql.dialect()))

    assert "bingo.exact" in compiled
    assert "bingo_function_compounds.query_structure" in compiled
    assert "bingo_function_compounds.query_parameters" in compiled


@pytest.mark.parametrize(
    ("helper_name", "column_type", "query", "search_type"),
    [
        ("mol_has_substructure", BingoMol(), "c1ccccc1", "bingo.sub"),
        ("mol_has_smarts", BingoMol(), "[#6]", "bingo.smarts"),
        ("mol_equals", BingoMol(), "CCO", "bingo.exact"),
        ("rxn_has_substructure", BingoReaction(), "CCO>>CC=O", "bingo.rsub"),
        ("rxn_has_smarts", BingoReaction(), "[C:1]>>[C:1][O]", "bingo.rsmarts"),
        ("rxn_equals", BingoReaction(), "CCO>>CC=O", "bingo.rexact"),
    ],
)
def test_prefixed_search_helpers_compile_to_expected_search_types(
    helper_name, column_type, query, search_type
):
    """Each comparator search operation has a prefixed standalone helper."""
    structures = Table(
        "structures",
        MetaData(),
        Column("id", Integer),
        Column("structure", column_type),
    )

    helper = getattr(bingo_func, helper_name)
    stmt = select(structures).where(helper(structures.c.structure, query))

    compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))

    assert " @ " in compiled
    assert search_type in compiled
    assert query in compiled


def test_unprefixed_search_helpers_are_not_exported():
    """Bingo standalone helper names are explicit about molecule vs reaction."""
    assert "has_substructure" not in bingo_func.__all__
    assert "matches_smarts" not in bingo_func.__all__
    assert "similarity" not in bingo_func.__all__
    assert not hasattr(bingo_func, "has_substructure")
    assert not hasattr(bingo_func, "matches_smarts")
    assert not hasattr(bingo_func, "similarity")
