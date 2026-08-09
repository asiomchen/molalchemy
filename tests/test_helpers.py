import pytest
from sqlalchemy import BINARY, Column, Integer, String, Table, select
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from molalchemy.bingo.types import (
    BingoBinaryMol,
    BingoBinaryReaction,
    BingoMol,
    BingoReaction,
)
from molalchemy.helpers import (
    bingo_col,
    bingo_rxn_col,
    rdkit_col,
    rdkit_fp_col,
    rdkit_rxn_col,
)
from molalchemy.rdkit.types import (
    RdkitBitFingerprint,
    RdkitMol,
    RdkitReaction,
    RdkitSparseFingerprint,
)


class Base(DeclarativeBase):
    pass


class BingoCompound(Base):
    __tablename__ = "helper_bingo_compounds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    structure: Mapped[str] = mapped_column(BingoMol())
    binary_structure: Mapped[str] = mapped_column(BingoBinaryMol())
    reaction: Mapped[str] = mapped_column(BingoReaction())


class RdkitCompound(Base):
    __tablename__ = "helper_rdkit_compounds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    structure: Mapped[str] = mapped_column(RdkitMol())
    other_structure: Mapped[str] = mapped_column(RdkitMol())
    reaction: Mapped[str] = mapped_column(RdkitReaction())
    other_reaction: Mapped[str] = mapped_column(RdkitReaction())
    fingerprint: Mapped[bytes] = mapped_column(RdkitBitFingerprint())
    other_fingerprint: Mapped[bytes] = mapped_column(RdkitBitFingerprint())


@pytest.fixture(params=[BingoMol, BingoBinaryMol])
def good_bingo_mol_col(request: pytest.FixtureRequest):
    column_type = request.param
    return Column("structure", column_type)


@pytest.fixture(params=[BingoReaction, BingoBinaryReaction])
def good_bingo_rxn_col(request: pytest.FixtureRequest):
    column_type = request.param
    return Column("reaction", column_type)


@pytest.fixture()
def good_rdkit_mol_col():
    return Column("structure", RdkitMol())


@pytest.fixture()
def good_rdkit_rxn_col():
    return Column("reaction", RdkitReaction())


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


def test_bingo_rxn_col_success(good_bingo_rxn_col):
    result = bingo_rxn_col(good_bingo_rxn_col)
    assert result is good_bingo_rxn_col


@pytest.mark.parametrize("bad_type", [String, BINARY])
def test_rdkit_mol_col_type_error(bad_type):
    col = Column("bad_structure", bad_type)
    with pytest.raises(TypeError, match="Column is not of type RdkitMol"):
        rdkit_col(col)


@pytest.mark.parametrize("bad_type", [String, BINARY])
def test_rdkit_rxn_col_type_error(bad_type):
    col = Column("bad_reaction", bad_type)
    with pytest.raises(TypeError, match="Column is not of type RdkitReaction"):
        rdkit_rxn_col(col)


def test_rdkit_mol_col_invalid_input():
    with pytest.raises(
        TypeError, match="Input is not a SQLAlchemy Column or InstrumentedAttribute"
    ):
        rdkit_col("not_a_column")


def test_rdkit_rxn_col_invalid_input():
    with pytest.raises(
        TypeError, match="Input is not a SQLAlchemy InstrumentedAttribute or Column"
    ):
        rdkit_rxn_col(123)


def test_rdkit_mol_col_success(good_rdkit_mol_col):
    result = rdkit_col(good_rdkit_mol_col)
    assert result is good_rdkit_mol_col


def test_rdkit_rxn_col_success(good_rdkit_rxn_col):
    result = rdkit_rxn_col(good_rdkit_rxn_col)
    assert result is good_rdkit_rxn_col


@pytest.mark.parametrize(
    "fingerprint_type", [RdkitBitFingerprint, RdkitSparseFingerprint]
)
def test_rdkit_fp_col_success(fingerprint_type):
    column = Column("fingerprint", fingerprint_type())
    assert rdkit_fp_col(column) is column


@pytest.mark.parametrize("bad_type", [String, BINARY, RdkitMol])
def test_rdkit_fp_col_type_error(bad_type):
    column = Column("fingerprint", bad_type())
    with pytest.raises(
        TypeError,
        match="Column is not of type RdkitBitFingerprint or RdkitSparseFingerprint",
    ):
        rdkit_fp_col(column)


def test_rdkit_fp_col_invalid_input():
    with pytest.raises(
        TypeError, match="Input is not a SQLAlchemy Column or InstrumentedAttribute"
    ):
        rdkit_fp_col(123)


def test_bingo_mol_proxy_helper_core_column_compiles_substructure():
    table = Table(
        "compounds",
        Base.metadata,
        Column("id", Integer, primary_key=True),
        Column("structure", BingoMol()),
        extend_existing=True,
    )

    stmt = select(table).where(
        bingo_col(table.c.structure).has_substructure("c1ccccc1")
    )
    compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))

    assert "bingo.sub" in compiled
    assert "c1ccccc1" in compiled


def test_bingo_binary_mol_proxy_helper_core_column_compiles_exact_search():
    table = Table(
        "binary_compounds",
        Base.metadata,
        Column("id", Integer, primary_key=True),
        Column("structure", BingoBinaryMol()),
        extend_existing=True,
    )

    stmt = select(table).where(bingo_col(table.c.structure).equals("CCO"))
    compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))

    assert "bingo.exact" in compiled
    assert "CCO" in compiled


def test_bingo_rxn_proxy_helper_core_column_compiles_exact_search():
    table = Table(
        "reactions",
        Base.metadata,
        Column("id", Integer, primary_key=True),
        Column("reaction", BingoReaction()),
        extend_existing=True,
    )

    stmt = select(table).where(bingo_rxn_col(table.c.reaction).equals("CCO>>CC=O"))
    compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))

    assert "bingo.rexact" in compiled
    assert "CCO>>CC=O" in compiled


def test_rdkit_mol_proxy_helper_core_column_compiles_substructure():
    table = Table(
        "rdkit_compounds",
        Base.metadata,
        Column("id", Integer, primary_key=True),
        Column("structure", RdkitMol()),
        extend_existing=True,
    )

    stmt = select(table).where(
        rdkit_col(table.c.structure).has_substructure("c1ccccc1")
    )
    compiled = str(stmt.compile(dialect=postgresql.dialect()))

    assert "@>" in compiled
    assert "structure_" in compiled


def test_rdkit_rxn_proxy_helper_core_column_compiles_smarts_search():
    table = Table(
        "rdkit_reactions",
        Base.metadata,
        Column("id", Integer, primary_key=True),
        Column("reaction", RdkitReaction()),
        extend_existing=True,
    )

    stmt = select(table).where(
        rdkit_rxn_col(table.c.reaction).has_smarts("[C:1]>>[C:1][O]")
    )
    compiled = str(stmt.compile(dialect=postgresql.dialect()))

    assert "substruct" in compiled
    assert "reaction_from_smarts" in compiled


def test_bingo_proxy_helpers_accept_orm_instrumented_attributes():
    assert bingo_col(BingoCompound.structure) is BingoCompound.structure
    assert bingo_col(BingoCompound.binary_structure) is BingoCompound.binary_structure
    assert bingo_rxn_col(BingoCompound.reaction) is BingoCompound.reaction

    stmt = select(BingoCompound).where(bingo_col(BingoCompound.structure).equals("CCO"))
    compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))

    assert "bingo.exact" in compiled
    assert "CCO" in compiled

    score = bingo_col(BingoCompound.structure).similarity_score("CCO")
    assert score.type.python_type is float
    assert "bingo.getsimilarity" in str(
        select(score).compile(dialect=postgresql.dialect())
    )


def test_rdkit_proxy_helpers_accept_orm_instrumented_attributes():
    assert rdkit_col(RdkitCompound.structure) is RdkitCompound.structure
    assert rdkit_rxn_col(RdkitCompound.reaction) is RdkitCompound.reaction
    assert rdkit_fp_col(RdkitCompound.fingerprint) is RdkitCompound.fingerprint

    stmt = select(RdkitCompound).where(
        rdkit_rxn_col(RdkitCompound.reaction).has_smarts("[C:1]>>[C:1][O]")
    )
    compiled = str(stmt.compile(dialect=postgresql.dialect()))

    assert "substruct" in compiled
    assert "reaction_from_smarts" in compiled


def test_rdkit_fingerprint_helper_compiles_distance_ordering():
    distance = rdkit_fp_col(RdkitCompound.fingerprint).tanimoto_distance(b"fingerprint")
    compiled = str(
        select(RdkitCompound)
        .order_by(distance)
        .compile(dialect=postgresql.dialect(paramstyle="named"))
    )

    assert "ORDER BY" in compiled
    assert "<%>" in compiled


def test_rdkit_helpers_accept_orm_column_operands():
    molecule_match = rdkit_col(RdkitCompound.structure).equals(
        RdkitCompound.other_structure
    )
    reaction_match = rdkit_rxn_col(RdkitCompound.reaction).equals(
        RdkitCompound.other_reaction
    )
    fingerprint_match = rdkit_fp_col(RdkitCompound.fingerprint).dice_matches(
        RdkitCompound.other_fingerprint
    )

    compiled = str(
        select(RdkitCompound)
        .where(molecule_match, reaction_match, fingerprint_match)
        .compile(dialect=postgresql.dialect(paramstyle="named"))
    )

    assert "structure @= helper_rdkit_compounds.other_structure" in compiled
    assert "reaction @= helper_rdkit_compounds.other_reaction" in compiled
    assert "fingerprint # helper_rdkit_compounds.other_fingerprint" in compiled
