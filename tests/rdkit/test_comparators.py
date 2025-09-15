"""Tests for RDKit comparators."""

from sqlalchemy import Column, Integer, String, MetaData, Table
from sqlalchemy.sql import select

from molalchemy.rdkit.types import RdkitMol, RdkitBitFingerprint, RdkitSparseFingerprint


class TestRdkitMolComparator:
    """Test RdkitMolComparator methods."""

    def setup_method(self):
        """Set up test table with RdkitMol column."""
        self.metadata = MetaData()
        self.test_table = Table(
            "test_molecules",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("structure", RdkitMol()),
        )
        self.mol_column = self.test_table.c.structure

    def test_has_substructure_query_generation(self):
        """Test has_substructure query generation."""
        query = "c1ccccc1"  # benzene

        result = self.mol_column.has_substructure(query)

        # Check that the result is a proper SQLAlchemy expression
        assert hasattr(result, "left")
        assert hasattr(result, "right")
        assert hasattr(result, "operator")

        # Check that we can compile it to SQL (basic check)
        compiled = str(result.compile())
        assert "@>" in compiled
        # The query value will be a bind parameter, not literal
        assert ":structure_" in compiled

    def test_equals_query_generation(self):
        """Test equals query generation."""
        query = "CCO"  # ethanol

        result = self.mol_column.equals(query)

        # Check that the result is a proper SQLAlchemy expression
        assert hasattr(result, "left")
        assert hasattr(result, "right")
        assert hasattr(result, "operator")

        # Check that we can compile it to SQL (basic check)
        compiled = str(result.compile())
        assert "@=" in compiled
        # The query value will be a bind parameter, not literal
        assert ":structure_" in compiled

    def test_query_with_special_characters(self):
        """Test query with special molecular structures."""
        query = "CC(=O)O"  # acetic acid

        result = self.mol_column.equals(query)
        compiled = str(result.compile())

        assert "@=" in compiled
        # The query value will be a bind parameter, not literal
        assert ":structure_" in compiled

    def test_invalid_operator(self):
        """Test that invalid operators raise appropriate errors."""
        query = "CCO"

        # Test with a method that doesn't exist
        try:
            # This should raise AttributeError since invalid_method doesn't exist
            self.mol_column.invalid_method(query)
            assert False, "Should have raised AttributeError"
        except AttributeError:
            pass


class TestRdkitFPComparator:
    """Test RdkitFPComparator methods for fingerprint data."""

    def setup_method(self):
        """Set up test table with fingerprint columns."""
        self.metadata = MetaData()
        self.test_table = Table(
            "test_fingerprints",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("fingerprint", RdkitBitFingerprint()),
            Column("sparse_fp", RdkitSparseFingerprint()),
        )
        self.fp_column = self.test_table.c.fingerprint
        self.sparse_fp_column = self.test_table.c.sparse_fp

    def test_nearest_neighbors_tanimoto_query_generation(self):
        """Test nearest_neighbors with tanimoto query generation."""
        query_fp = b"test_fingerprint"

        result = self.fp_column.nearest_neighbors(query_fp, "tanimoto")

        # Check that the result is a proper SQLAlchemy expression
        assert hasattr(result, "left")
        assert hasattr(result, "right")
        assert hasattr(result, "operator")

        # Check that we can compile it to SQL (basic check)
        compiled = str(result.compile())
        assert "<%>" in compiled
        assert ":fingerprint_" in compiled

    def test_nearest_neighbors_dice_query_generation(self):
        """Test nearest_neighbors with dice query generation."""
        query_fp = b"test_fingerprint"

        result = self.fp_column.nearest_neighbors(query_fp, "dice")

        # Check that the result is a proper SQLAlchemy expression
        assert hasattr(result, "left")
        assert hasattr(result, "right")
        assert hasattr(result, "operator")

        # Check that we can compile it to SQL (basic check)
        compiled = str(result.compile())
        assert "<#>" in compiled
        assert ":fingerprint_" in compiled

    def test_nearest_neighbors_default_tanimoto(self):
        """Test that nearest_neighbors defaults to tanimoto."""
        query_fp = b"test_fingerprint"

        result = self.fp_column.nearest_neighbors(query_fp)
        compiled = str(result.compile())

        # Should default to tanimoto
        assert "<%>" in compiled
        assert ":fingerprint_" in compiled

    def test_dice_similarity_query_generation(self):
        """Test dice similarity query generation."""
        query_fp = b"test_fingerprint"

        result = self.fp_column.dice(query_fp)

        # Check that the result is a proper SQLAlchemy expression
        assert hasattr(result, "left")
        assert hasattr(result, "right")
        assert hasattr(result, "operator")

        # Check that we can compile it to SQL (basic check)
        compiled = str(result.compile())
        assert "#" in compiled
        assert ":fingerprint_" in compiled

    def test_sparse_fingerprint_comparator_methods(self):
        """Test that sparse fingerprint columns have the same comparator methods."""
        query_fp = b"test_sparse_fingerprint"

        # Test that sparse fingerprint columns also have the fingerprint comparator methods
        tanimoto_result = self.sparse_fp_column.nearest_neighbors(query_fp, "tanimoto")
        dice_result = self.sparse_fp_column.dice(query_fp)

        # Should compile without errors
        tanimoto_compiled = str(tanimoto_result.compile())
        dice_compiled = str(dice_result.compile())

        assert "<%>" in tanimoto_compiled
        assert "#" in dice_compiled
        assert ":sparse_fp_" in tanimoto_compiled
        assert ":sparse_fp_" in dice_compiled


class TestRdkitComparatorInQueries:
    """Test RDKit comparators in actual SQL queries."""

    def setup_method(self):
        """Set up test table for query testing."""
        self.metadata = MetaData()
        self.test_table = Table(
            "test_compounds",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("structure", RdkitMol()),
            Column("fingerprint", RdkitBitFingerprint()),
        )

    def test_has_substructure_in_select_query(self):
        """Test has_substructure comparator in SELECT query."""
        query = "c1ccccc1"

        stmt = select(self.test_table).where(
            self.test_table.c.structure.has_substructure(query)
        )

        # Should compile without errors
        compiled = str(stmt.compile())
        assert "SELECT" in compiled
        assert "@>" in compiled
        assert ":structure_" in compiled

    def test_equals_in_select_query(self):
        """Test equals comparator in SELECT query."""
        query = "CCO"

        stmt = select(self.test_table).where(self.test_table.c.structure.equals(query))

        # Should compile without errors
        compiled = str(stmt.compile())
        assert "SELECT" in compiled
        assert "@=" in compiled
        assert ":structure_" in compiled

    def test_fingerprint_similarity_in_select_query(self):
        """Test fingerprint similarity comparator in SELECT query."""
        query_fp = b"test_fingerprint"

        stmt = select(self.test_table).where(
            self.test_table.c.fingerprint.nearest_neighbors(query_fp)
        )

        # Should compile without errors
        compiled = str(stmt.compile())
        assert "SELECT" in compiled
        assert "<%>" in compiled
        assert ":fingerprint_" in compiled

    def test_multiple_comparators_in_query(self):
        """Test using multiple RDKit comparators in one query."""
        benzene = "c1ccccc1"
        ethanol = "CCO"
        query_fp = b"test_fingerprint"

        stmt = select(self.test_table).where(
            self.test_table.c.structure.has_substructure(benzene)
            | self.test_table.c.structure.equals(ethanol)
            | self.test_table.c.fingerprint.dice(query_fp)
        )

        compiled = str(stmt.compile())
        assert "SELECT" in compiled
        # Should contain all operators
        assert "@>" in compiled  # has_substructure
        assert "@=" in compiled  # equals
        assert "#" in compiled  # dice
        # Should have proper bind parameters
        assert ":structure_" in compiled
        assert ":fingerprint_" in compiled
