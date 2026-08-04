"""Semantic tests for RDKit comparators."""

import pytest
from sqlalchemy import (
    Boolean,
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    and_,
    bindparam,
    cast,
    or_,
    select,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from molalchemy.rdkit import RdkitFPComparator, RdkitMolComparator
from molalchemy.rdkit.types import (
    RdkitBitFingerprint,
    RdkitMol,
    RdkitQMol,
    RdkitReaction,
    RdkitSparseFingerprint,
)


def sql(expression) -> str:
    return str(expression.compile(dialect=postgresql.dialect(paramstyle="named")))


class Base(DeclarativeBase):
    pass


class Compound(Base):
    __tablename__ = "rdkit_comparator_compounds"

    id: Mapped[int] = mapped_column(primary_key=True)
    mol: Mapped[str] = mapped_column(RdkitMol())
    fp: Mapped[bytes] = mapped_column(RdkitBitFingerprint())


@pytest.fixture
def columns():
    table = Table(
        "rdkit_values",
        MetaData(),
        Column("id", Integer),
        Column("mol", RdkitMol()),
        Column("other_mol", RdkitMol()),
        Column("rxn", RdkitReaction()),
        Column("other_rxn", RdkitReaction()),
        Column("bfp", RdkitBitFingerprint()),
        Column("sfp", RdkitSparseFingerprint()),
        Column("text", String()),
    )
    return table.c


@pytest.mark.parametrize(
    ("method", "query", "operator"),
    [
        ("has_substructure", "c1ccccc1", "@>"),
        ("is_substructure_of", "CCO", "<@"),
        ("equals", "CCO", "@="),
        ("not_equals", "CCN", "@<>"),
        ("has_query_substructure", cast("[cH]", RdkitQMol), "@>>"),
        ("is_query_substructure_of", cast("[cH]", RdkitQMol), "<<@"),
    ],
)
def test_molecule_predicates_are_boolean(columns, method, query, operator):
    expression = getattr(columns.mol, method)(query)

    assert isinstance(expression.type, Boolean)
    assert operator in sql(expression)


def test_molecule_smarts_is_boolean(columns):
    expression = columns.mol.has_smarts("[#6]")

    assert isinstance(expression.type, Boolean)
    assert "qmol_from_smarts" in sql(expression)
    assert "@>" in sql(expression)


@pytest.mark.parametrize(
    ("method", "operator"),
    [
        ("has_substructure", "@>"),
        ("is_substructure_of", "<@"),
        ("equals", "@="),
        ("not_equals", "@<>"),
        ("has_substructure_fp", "?>"),
        ("is_substructure_fp_of", "?<"),
    ],
)
def test_reaction_predicates_are_boolean(columns, method, operator):
    expression = getattr(columns.rxn, method)("[C:1]>>[C:1]")

    assert isinstance(expression.type, Boolean)
    assert operator in sql(expression)


def test_reaction_smarts_is_boolean(columns):
    expression = columns.rxn.has_smarts("[C:1]>>[C:1][O]")

    assert isinstance(expression.type, Boolean)
    assert "substruct" in sql(expression)


@pytest.mark.parametrize("fingerprint", ["bfp", "sfp"])
@pytest.mark.parametrize(
    ("method", "operator", "result_type"),
    [
        ("tanimoto_matches", "%", Boolean),
        ("dice_matches", "#", Boolean),
        ("tanimoto_distance", "<%>", Float),
        ("dice_distance", "<#>", Float),
    ],
)
def test_fingerprint_operators_have_exact_types(
    columns, fingerprint, method, operator, result_type
):
    column = columns[fingerprint]
    expression = getattr(column, method)(bindparam("query_fp", b"fingerprint"))

    assert isinstance(expression.type, result_type)
    assert operator in sql(expression)


def test_removed_fingerprint_methods_have_no_compatibility_aliases(columns):
    for name in ("tanimoto", "dice", "nearest_neighbors"):
        with pytest.raises(AttributeError):
            getattr(columns.bfp, name)


def test_predicates_compose_negate_and_label(columns):
    substructure = columns.mol.has_substructure("CO")
    exact = columns.mol.equals(bindparam("exact", "CCO"))
    statement = select((~substructure).label("not_sub")).where(
        and_(or_(substructure, exact), ~columns.mol.not_equals("CCO"))
    )

    compiled = statement.compile(dialect=postgresql.dialect())
    assert isinstance(substructure.type, Boolean)
    assert {"CO", "CCO"}.issubset(set(compiled.params.values()))


def test_knn_distances_work_in_order_by(columns):
    query = bindparam("query_fp", b"fingerprint")
    statement = select(columns.id).order_by(
        columns.bfp.tanimoto_distance(query),
        columns.bfp.dice_distance(query),
    )

    compiled = sql(statement)
    assert "ORDER BY" in compiled
    assert "<%>" in compiled
    assert "<#>" in compiled


def test_sql_expression_operands_are_preserved(columns):
    subquery = select(columns.other_mol.label("query")).subquery()
    expression = columns.mol.has_substructure(subquery.c.query)
    compiled = sql(expression)

    assert "anon_1.query" in compiled
    assert "mol_from_pkl" not in compiled


@pytest.mark.parametrize("name", ["mol", "rxn"])
def test_native_equality_and_null_semantics(columns, name):
    column = columns[name]
    other = columns[f"other_{name}"]

    assert " = " in sql(column == other)
    assert " != " in sql(column != other)
    assert " = " in sql(column == "CCO")
    assert " != " in sql(column != "CCO")
    assert "@=" not in sql(column == other)
    assert "IS NULL" in sql(column.__eq__(None))
    assert "IS NOT NULL" in sql(column.__ne__(None))
    assert "@=" in sql(column.equals(other))
    assert "@<>" in sql(column.not_equals(other))


def test_orm_comparators_remain_available_at_runtime():
    predicate = Compound.mol.equals("CCO")
    distance = Compound.fp.tanimoto_distance(b"fingerprint")

    assert isinstance(predicate.type, Boolean)
    assert isinstance(distance.type, Float)
    assert "ORDER BY" in sql(select(Compound).order_by(distance))


def test_comparators_are_public():
    assert RdkitMolComparator.__name__ == "RdkitMolComparator"
    assert RdkitFPComparator.__name__ == "RdkitFPComparator"
