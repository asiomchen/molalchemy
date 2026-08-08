"""Semantic tests for Bingo comparators."""

import pytest
from sqlalchemy import (
    Boolean,
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    bindparam,
    select,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from molalchemy.bingo import BingoMolComparator, BingoRxnComparator
from molalchemy.bingo import functions as bingo_func
from molalchemy.bingo.types import (
    BingoBinaryMol,
    BingoBinaryReaction,
    BingoMol,
    BingoReaction,
)


def sql(expression) -> str:
    return str(expression.compile(dialect=postgresql.dialect()))


class Base(DeclarativeBase):
    pass


class Compound(Base):
    __tablename__ = "bingo_comparator_compounds"

    id: Mapped[int] = mapped_column(primary_key=True)
    mol: Mapped[str] = mapped_column(BingoMol())
    other_mol: Mapped[str] = mapped_column(BingoMol())
    query_parameters: Mapped[str] = mapped_column(String())


@pytest.fixture(params=[BingoMol(), BingoBinaryMol()])
def mol_columns(request):
    table = Table(
        f"bingo_mols_{type(request.param).__name__.lower()}",
        MetaData(),
        Column("id", Integer),
        Column("mol", request.param),
        Column("other", request.param),
        Column("query", String()),
    )
    return table.c


@pytest.fixture(params=[BingoReaction(), BingoBinaryReaction()])
def rxn_columns(request):
    table = Table(
        f"bingo_rxns_{type(request.param).__name__.lower()}",
        MetaData(),
        Column("id", Integer),
        Column("rxn", request.param),
        Column("other", request.param),
        Column("query", String()),
    )
    return table.c


@pytest.mark.parametrize(
    ("method", "search_type"),
    [
        ("has_substructure", "bingo.sub"),
        ("has_smarts", "bingo.smarts"),
        ("equals", "bingo.exact"),
        ("not_equals", "bingo.exact"),
    ],
)
def test_molecule_predicates_are_boolean(mol_columns, method, search_type):
    expression = getattr(mol_columns.mol, method)("CCO", "TAU")
    compiled = expression.compile(dialect=postgresql.dialect())

    assert isinstance(expression.type, Boolean)
    assert search_type in str(compiled)
    assert "CCO" in compiled.params.values()
    assert "TAU" in compiled.params.values()


@pytest.mark.parametrize(
    ("method", "search_type"),
    [
        ("has_substructure", "bingo.rsub"),
        ("has_smarts", "bingo.rsmarts"),
        ("equals", "bingo.rexact"),
        ("not_equals", "bingo.rexact"),
    ],
)
def test_reaction_predicates_are_boolean(rxn_columns, method, search_type):
    expression = getattr(rxn_columns.rxn, method)("CCO>>CC=O", "STE")
    compiled = expression.compile(dialect=postgresql.dialect())

    assert isinstance(expression.type, Boolean)
    assert search_type in str(compiled)
    assert "CCO>>CC=O" in compiled.params.values()
    assert "STE" in compiled.params.values()


def test_similarity_defaults_and_function_parity(mol_columns):
    method = mol_columns.mol.similar_to("CCO")
    function = bingo_func.mol_similar_to(mol_columns.mol, "CCO")

    assert isinstance(method.type, Boolean)
    assert sql(method) == sql(function)
    assert set(method.compile().params.values()) == {0.0, 1.0, "CCO", "Tanimoto"}


def test_legacy_similarity_function_preserves_old_keywords(mol_columns):
    canonical = bingo_func.mol_similar_to(
        mol_columns.mol, "CCO", minimum=0.2, maximum=0.8, metric="Dice"
    )
    legacy = bingo_func.mol_similarity(
        mol_columns.mol, "CCO", bottom=0.2, top=0.8, metric="Dice"
    )

    assert sql(canonical) == sql(legacy)
    assert set(canonical.compile().params.values()) == {0.2, 0.8, "CCO", "Dice"}


def test_similarity_score_comparator_and_function_parity(mol_columns):
    method = mol_columns.mol.similarity_score("CCO")
    function = bingo_func.mol_similarity_score(mol_columns.mol, "CCO")

    assert isinstance(method.type, Float)
    assert sql(method) == sql(function)
    assert "bingo.getsimilarity" in sql(method)
    assert set(method.compile().params.values()) == {"CCO", "Tanimoto"}


def test_similarity_predicate_accepts_open_bounds(mol_columns):
    expression = bingo_func.mol_similar_to(
        mol_columns.mol, "CCO", minimum=None, maximum=None
    )
    compiled = expression.compile(dialect=postgresql.dialect())

    assert isinstance(expression.type, Boolean)
    assert "bingo.sim" in str(compiled)
    assert "NULL, NULL" in str(compiled)


def test_similarity_custom_options_and_distinct_binds(mol_columns):
    statement = select(mol_columns.id).where(
        mol_columns.mol.similar_to("CCO", 0.2, 0.8, "Dice"),
        mol_columns.mol.similar_to("CCN", 0.4, 0.9, "Cosine"),
    )
    compiled = statement.compile(dialect=postgresql.dialect())

    assert "bingo.sim" in str(compiled)
    assert {"CCO", "CCN", 0.2, 0.8, 0.4, 0.9, "Dice", "Cosine"}.issubset(
        set(compiled.params.values())
    )


def test_sql_expression_tuple_members_are_preserved(mol_columns):
    minimum = bindparam("minimum", 0.3)
    expression = mol_columns.mol.similar_to(
        mol_columns.query, minimum, 1.0, bindparam("metric", "Tanimoto")
    )
    compiled = sql(expression)

    assert "query" in compiled
    assert "minimum" in compiled
    assert "metric" in compiled


def test_predicates_compose_negate_and_label(mol_columns):
    substructure = mol_columns.mol.has_substructure("CO")
    exact = mol_columns.mol.equals("CCO")
    statement = select((~substructure).label("not_sub")).where(substructure | exact)

    assert isinstance(substructure.type, Boolean)
    assert "NOT" in sql(statement)
    assert " OR " in sql(statement)


def test_native_molecule_equality_and_explicit_chemical_matching(mol_columns):
    assert " = " in sql(mol_columns.mol == mol_columns.other)
    assert " != " in sql(mol_columns.mol != mol_columns.other)
    assert " = " in sql(mol_columns.mol == "CCO")
    assert " != " in sql(mol_columns.mol != "CCO")
    assert "bingo.exact" not in sql(mol_columns.mol == mol_columns.other)
    assert "IS NULL" in sql(mol_columns.mol.__eq__(None))
    assert "IS NOT NULL" in sql(mol_columns.mol.__ne__(None))
    assert "bingo.exact" in sql(mol_columns.mol.equals(mol_columns.query))
    assert "NOT" in sql(mol_columns.mol.not_equals(mol_columns.query))


def test_native_reaction_equality_and_explicit_chemical_matching(rxn_columns):
    assert " = " in sql(rxn_columns.rxn == rxn_columns.other)
    assert " != " in sql(rxn_columns.rxn != rxn_columns.other)
    assert "bingo.rexact" not in sql(rxn_columns.rxn == rxn_columns.other)
    assert "IS NULL" in sql(rxn_columns.rxn.__eq__(None))
    assert "bingo.rexact" in sql(rxn_columns.rxn.equals(rxn_columns.query))


def test_orm_comparator_remains_available_at_runtime():
    expression = Compound.mol.similar_to("CCO", minimum=0.7)
    assert isinstance(expression.type, Boolean)
    assert "bingo.sim" in sql(select(Compound).where(expression))

    score = Compound.mol.similarity_score("CCO")
    assert isinstance(score.type, Float)
    assert "bingo.getsimilarity" in sql(select(score))


def test_orm_attributes_are_preserved_as_comparator_operands():
    expression = Compound.mol.equals(Compound.other_mol, Compound.query_parameters)
    compiled = sql(select(Compound).where(expression))

    assert "bingo.exact" in compiled
    assert "bingo_comparator_compounds.other_mol" in compiled
    assert "bingo_comparator_compounds.query_parameters" in compiled


def test_comparators_are_public():
    assert BingoMolComparator.__name__ == "BingoMolComparator"
    assert BingoRxnComparator.__name__ == "BingoRxnComparator"
