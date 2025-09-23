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
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import select

from molalchemy.bingo import functions as bingo_func
from molalchemy.bingo.types import BingoMol


class TestBingoFunc:
    """Test bingo_func static methods."""

    def setup_method(self):
        """Set up test table."""
        self.metadata = MetaData()
        self.test_table = Table(
            "test_compounds",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("structure", BingoMol()),
        )
        self.mol_column = self.test_table.c.structure

    def test_has_substructure_function(self):
        """Test has_substructure function generates correct SQL."""
        query = "c1ccccc1"
        parameters = ""

        result = bingo_func.mol.has_substructure(self.mol_column, query, parameters)

        # Should return a binary expression (column @ operator)
        assert hasattr(result, "left")
        assert hasattr(result, "right")
        assert hasattr(result, "operator")

        # Check the generated SQL string
        sql_str = str(result)
        assert "test_compounds.structure" in sql_str
        assert "@" in sql_str
        assert "bingo.sub" in sql_str
        assert query in sql_str

    def test_has_substructure_with_parameters(self):
        """Test has_substructure function with parameters."""
        query = "c1ccccc1"
        parameters = "max=5"

        result = bingo_func.mol.has_substructure(self.mol_column, query, parameters)
        sql_str = str(result)

        assert query in sql_str
        assert parameters in sql_str
        assert "bingo.sub" in sql_str

    def test_matches_smarts_function(self):
        """Test SMARTS function generates correct SQL."""
        query = "[#6]1:[#6]:[#6]:[#6]:[#6]:[#6]:1"
        parameters = ""

        result = bingo_func.mol.matches_smarts(self.mol_column, query, parameters)
        sql_str = str(result)

        assert "test_compounds.structure" in sql_str
        assert "@" in sql_str
        assert "bingo.smarts" in sql_str
        assert query in sql_str

    def test_matches_smarts_with_parameters(self):
        """Test SMARTS function with parameters."""
        query = "[#6]1:[#6]:[#6]:[#6]:[#6]:[#6]:1"
        parameters = "timeout=1000"

        result = bingo_func.mol.matches_smarts(self.mol_column, query, parameters)
        sql_str = str(result)

        assert query in sql_str
        assert parameters in sql_str
        assert "bingo.smarts" in sql_str

    def test_equals_function(self):
        """Test equals function generates correct SQL."""
        query = "CCO"
        parameters = ""

        result = bingo_func.mol.equals(self.mol_column, query, parameters)
        sql_str = str(result)

        assert "test_compounds.structure" in sql_str
        assert "@" in sql_str
        assert "bingo.exact" in sql_str
        assert query in sql_str

    def test_equals_with_parameters(self):
        """Test equals function with parameters."""
        query = "CCO"
        parameters = "stereo=1"

        result = bingo_func.mol.equals(self.mol_column, query, parameters)
        sql_str = str(result)

        assert query in sql_str
        assert parameters in sql_str
        assert "bingo.exact" in sql_str

    def test_similarity_function(self):
        """Test similarity function generates correct SQL."""
        query = "CCO"
        bottom = 0.5
        top = 1.0
        metric = "Tanimoto"

        result = bingo_func.mol.similarity(self.mol_column, query, bottom, top, metric)
        sql_str = str(result)

        assert "test_compounds.structure" in sql_str
        assert "%" in sql_str  # similarity uses % operator, not @
        assert "bingo.sim" in sql_str
        assert query in sql_str
        assert str(bottom) in sql_str
        assert str(top) in sql_str
        assert metric in sql_str

    def test_similarity_with_defaults(self):
        """Test similarity function with default parameters."""
        query = "CCO"

        result = bingo_func.mol.similarity(self.mol_column, query)
        sql_str = str(result)

        assert "0.0" in sql_str  # default bottom
        assert "1.0" in sql_str  # default top
        assert "Tanimoto" in sql_str  # default metric
        assert "bingo.sim" in sql_str

    def test_similarity_with_custom_metric(self):
        """Test similarity function with custom metric."""
        query = "CCO"
        metric = "Dice"

        result = bingo_func.mol.similarity(self.mol_column, query, metric=metric)
        sql_str = str(result)

        assert metric in sql_str
        assert "bingo.sim" in sql_str


class TestBingoFuncWithORM:
    """Test bingo_func with ORM-style columns."""

    def setup_method(self):
        """Set up ORM model for testing."""

        class Base(DeclarativeBase):
            pass

        class Compound(Base):
            __tablename__ = "compounds"

            id: Mapped[int] = mapped_column(Integer, primary_key=True)
            name: Mapped[str] = mapped_column(String(100))
            structure: Mapped[str] = mapped_column(BingoMol())

        self.Compound = Compound

    def test_equals_with_orm_column(self):
        """Test equals function with ORM column."""
        query = "CCO"

        # This should work with get_column_name utility
        result = bingo_func.mol.equals(self.Compound.structure, query)
        sql_str = str(result)

        assert "@" in sql_str
        assert "bingo.exact" in sql_str
        assert query in sql_str
        # Should contain table.column reference
        assert "compounds.structure" in sql_str

    def test_similarity_with_orm_column(self):
        """Test similarity function with ORM column."""
        query = "CCO"

        result = bingo_func.mol.similarity(self.Compound.structure, query)
        sql_str = str(result)

        assert "%" in sql_str  # similarity uses % operator, not @
        assert "bingo.sim" in sql_str
        assert query in sql_str
        assert "compounds.structure" in sql_str


class TestBingoFuncIntegration:
    """Integration tests for bingo functions in queries."""

    def setup_method(self):
        """Set up test table."""
        self.metadata = MetaData()
        self.test_table = Table(
            "compounds",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("structure", BingoMol()),
        )

    def test_has_substructure_in_where_clause(self):
        """Test using has_substructure function in WHERE clause."""
        query = "c1ccccc1"

        # Create a query using the function
        substructure_expr = bingo_func.mol.has_substructure(
            self.test_table.c.structure, query
        )

        stmt = select(self.test_table).where(substructure_expr)

        # Should compile without errors
        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "SELECT" in compiled
        assert "FROM compounds" in compiled
        assert "WHERE" in compiled
        assert "bingo.sub" in compiled

    def test_multiple_functions_in_query(self):
        """Test using multiple bingo functions in one query."""
        benzene = "c1ccccc1"
        ethanol = "CCO"

        substructure_expr = bingo_func.mol.has_substructure(
            self.test_table.c.structure, benzene
        )
        equals_expr = bingo_func.mol.equals(self.test_table.c.structure, ethanol)

        # Combine using text() expressions properly with or_()
        from sqlalchemy import or_

        stmt = select(self.test_table).where(or_(substructure_expr, equals_expr))

        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "bingo.sub" in compiled
        assert "bingo.exact" in compiled
        assert benzene in compiled
        assert ethanol in compiled


all_mol_func = [
    getattr(bingo_func.mol, f) for f in bingo_func.mol.__all__ if not f.startswith("_")
]

all_rxn_func = [
    getattr(bingo_func.rxn, f) for f in bingo_func.rxn.__all__ if not f.startswith("_")
]
all_funcs = all_mol_func + all_rxn_func


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
