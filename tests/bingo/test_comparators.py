"""Tests for bingo comparators."""

from sqlalchemy import Column, Integer, String, MetaData, Table
from sqlalchemy.sql import select

from chemschema.bingo.types import BingoMol, BingoBinaryMol


class TestBingoMolComparator:
    """Test BingoMolComparator methods."""

    def setup_method(self):
        """Set up test table with BingoMol column."""
        self.metadata = MetaData()
        self.test_table = Table(
            "test_molecules",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("mol", BingoMol()),
        )
        self.mol_column = self.test_table.c.mol

    def test_substructure_query_generation(self):
        """Test substructure query generation."""
        query = "c1ccccc1"  # benzene
        parameters = ""

        result = self.mol_column.substructure(query, parameters)

        # Check that the result is a proper SQLAlchemy expression
        assert hasattr(result, "left")
        assert hasattr(result, "right")
        assert hasattr(result, "operator")

        # Check that we can compile it to SQL (basic check)
        compiled = str(result.compile(compile_kwargs={"literal_binds": True}))
        assert "@" in compiled
        assert "bingo.sub" in compiled
        assert query in compiled

    def test_substructure_with_parameters(self):
        """Test substructure query with parameters."""
        query = "c1ccccc1"
        parameters = "max=5"

        result = self.mol_column.substructure(query, parameters)
        compiled = str(result.compile(compile_kwargs={"literal_binds": True}))

        assert query in compiled
        assert parameters in compiled
        assert "bingo.sub" in compiled

    def test_smarts_query_generation(self):
        """Test SMARTS query generation."""
        query = (
            "[#6]1-[#6]-[#6]-[#6]-[#6]-[#6]-1"  # benzene SMARTS (using - instead of :)
        )
        parameters = ""

        result = self.mol_column.smarts(query, parameters)
        compiled = str(result.compile(compile_kwargs={"literal_binds": True}))

        assert "@" in compiled
        assert "bingo.smarts" in compiled
        # Check that the query appears in some form (may be escaped)
        assert "[#6]1" in compiled or query in compiled

    def test_smarts_with_parameters(self):
        """Test SMARTS query with parameters."""
        query = "[#6]1-[#6]-[#6]-[#6]-[#6]-[#6]-1"
        parameters = "max=10"

        result = self.mol_column.smarts(query, parameters)
        compiled = str(result.compile(compile_kwargs={"literal_binds": True}))

        # Check that the query appears in some form and parameters are present
        assert "[#6]1" in compiled or query in compiled
        assert parameters in compiled
        assert "bingo.smarts" in compiled

    def test_equals_query_generation(self):
        """Test exact match query generation."""
        query = "CCO"  # ethanol
        parameters = ""

        result = self.mol_column.equals(query, parameters)
        compiled = str(result.compile(compile_kwargs={"literal_binds": True}))

        assert "@" in compiled
        assert "bingo.exact" in compiled
        assert query in compiled

    def test_equals_with_parameters(self):
        """Test exact match query with parameters."""
        query = "CCO"
        parameters = "stereo=1"

        result = self.mol_column.equals(query, parameters)
        compiled = str(result.compile(compile_kwargs={"literal_binds": True}))

        assert query in compiled
        assert parameters in compiled
        assert "bingo.exact" in compiled

    def test_empty_parameters_handling(self):
        """Test that empty parameters are handled correctly."""
        query = "CCO"

        # Test with empty string
        result1 = self.mol_column.substructure(query, "")
        compiled1 = str(result1.compile(compile_kwargs={"literal_binds": True}))

        # Test with default (should be empty string)
        result2 = self.mol_column.substructure(query)
        compiled2 = str(result2.compile(compile_kwargs={"literal_binds": True}))

        # Both should be equivalent
        assert compiled1 == compiled2

    def test_query_with_special_characters(self):
        """Test queries with special characters are handled properly."""
        query = (
            "CC(=O)N[C@@H](CC1=CC=CC=C1)C(=O)O"  # phenylalanine with stereochemistry
        )

        result = self.mol_column.substructure(query)
        # Should not raise any exceptions when compiling
        compiled = str(result.compile(compile_kwargs={"literal_binds": True}))
        assert query in compiled


class TestBingoMolComparatorWithBinaryType:
    """Test that BingoMolComparator works with BingoBinaryMol too."""

    def setup_method(self):
        """Set up test table with BingoBinaryMol column."""
        self.metadata = MetaData()
        self.test_table = Table(
            "test_binary_molecules",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("mol", BingoBinaryMol()),
        )
        self.mol_column = self.test_table.c.mol

    def test_binary_mol_substructure(self):
        """Test substructure works with binary mol type."""
        query = "c1ccccc1"

        result = self.mol_column.substructure(query)
        compiled = str(result.compile(compile_kwargs={"literal_binds": True}))

        assert "@" in compiled
        assert "bingo.sub" in compiled
        assert query in compiled

    def test_binary_mol_smarts(self):
        """Test SMARTS works with binary mol type."""
        query = "[#6]1-[#6]-[#6]-[#6]-[#6]-[#6]-1"

        result = self.mol_column.smarts(query)
        compiled = str(result.compile(compile_kwargs={"literal_binds": True}))

        assert "@" in compiled
        assert "bingo.smarts" in compiled
        assert "[#6]1" in compiled or query in compiled

    def test_binary_mol_equals(self):
        """Test equals works with binary mol type."""
        query = "CCO"

        result = self.mol_column.equals(query)
        compiled = str(result.compile(compile_kwargs={"literal_binds": True}))

        assert "@" in compiled
        assert "bingo.exact" in compiled
        assert query in compiled


class TestBingoComparatorInQueries:
    """Test bingo comparator in actual SQL queries."""

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

    def test_substructure_in_select_query(self):
        """Test substructure comparator in SELECT query."""
        query = "c1ccccc1"

        stmt = select(self.test_table).where(
            self.test_table.c.structure.substructure(query)
        )

        # Should compile without errors
        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "SELECT" in compiled
        assert "FROM compounds" in compiled
        assert "WHERE" in compiled
        assert "@" in compiled
        assert "bingo.sub" in compiled

    def test_multiple_comparators_in_query(self):
        """Test using multiple bingo comparators in one query."""
        benzene = "c1ccccc1"
        ethanol = "CCO"

        stmt = select(self.test_table).where(
            self.test_table.c.structure.substructure(benzene)
            | self.test_table.c.structure.equals(ethanol)
        )

        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "bingo.sub" in compiled
        assert "bingo.exact" in compiled
        assert benzene in compiled
        assert ethanol in compiled
