"""Tests for RDKit comparators."""

import pytest
from sqlalchemy import (
    Column,
    ColumnElement,
    Integer,
    MetaData,
    String,
    Table,
    bindparam,
    cast,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import select

from molalchemy.rdkit import RdkitMolComparator, RdkitReactionComparator
from molalchemy.rdkit.types import (
    RdkitBitFingerprint,
    RdkitMol,
    RdkitQMol,
    RdkitReaction,
    RdkitSparseFingerprint,
)


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

    @pytest.mark.parametrize(
        ("method_name", "query", "operator"),
        [
            ("has_substructure", "c1ccccc1", "@>"),
            ("is_substructure_of", "CCOCC", "<@"),
            ("equals", "CCO", "@="),
            ("has_query_substructure", cast("[cH]", RdkitQMol), "@>>"),
            ("is_query_substructure_of", cast("[cH]", RdkitQMol), "<<@"),
        ],
    )
    def test_methods_compile_to_expected_operators(self, method_name, query, operator):
        """Live RDKit molecule operators are exposed directly on the comparator."""
        result = getattr(self.mol_column, method_name)(query)
        compiled = result.compile(dialect=postgresql.dialect())
        sql = str(compiled)

        assert operator in sql
        if isinstance(query, str):
            assert "mol_from_pkl" in sql
            assert query in compiled.params.values()
        else:
            assert "CAST" in sql
            assert "qmol" in sql

    def test_query_with_special_characters(self):
        """Test query with special molecular structures."""
        query = "CC(=O)O"  # acetic acid

        result = self.mol_column.equals(query)
        compiled = str(result.compile())

        assert "@=" in compiled
        # The query value will be a bind parameter, not literal
        assert ":structure_" in compiled

    def test_string_queries_compile_via_molecule_coercion(self):
        stmt = select(self.test_table).where(
            self.mol_column.has_substructure("x' OR 1=1 --")
        )

        compiled = stmt.compile(dialect=postgresql.dialect())
        sql = str(compiled)

        assert "mol_from_pkl" in sql
        assert "x' OR 1=1 --" not in sql
        assert "x' OR 1=1 --" in compiled.params.values()

    def test_query_expressions_are_preserved(self):
        stmt = select(self.test_table).where(
            self.mol_column.has_query_substructure(cast("[cH]", RdkitQMol))
        )

        compiled = stmt.compile(dialect=postgresql.dialect())
        sql = str(compiled)

        assert "CAST(" in sql
        assert " AS qmol)" in sql
        assert "mol_from_pkl" not in sql
        assert "[cH]" in compiled.params.values()

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


class TestRdkitReactionComparator:
    """Test RdkitReactionComparator methods."""

    def setup_method(self):
        """Set up test table with RdkitReaction columns."""
        self.metadata = MetaData()
        self.test_table = Table(
            "test_reactions",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("rxn", RdkitReaction()),
            Column("query_rxn", RdkitReaction()),
        )
        self.rxn_column = self.test_table.c.rxn

    @pytest.mark.parametrize(
        ("method_name", "query", "operator"),
        [
            ("has_substructure", "[C:1]>>[C:1][O]", "@>"),
            ("is_substructure_of", "[C:1][O]>>[C:1]", "<@"),
            ("equals", "[C:1]>>[C:1]", "@="),
            ("not_equals", "[C:1]>>[C:1][Cl]", "@<>"),
            ("has_substructure_fp", "[C:1]>>[C:1][Br]", "?>"),
            ("is_substructure_fp_of", "[C:1][Br]>>[C:1]", "?<"),
        ],
    )
    def test_methods_compile_to_expected_operator(self, method_name, query, operator):
        """Live RDKit reaction operators are exposed directly on the comparator."""
        result = getattr(self.rxn_column, method_name)(query)
        compiled = result.compile(dialect=postgresql.dialect())
        sql = str(compiled)

        assert operator in sql
        assert "reaction_from_smarts" in sql
        assert query in compiled.params.values()

    def test_string_queries_compile_via_reaction_coercion(self):
        """String queries must bind as reactions, not raw text."""
        stmt = select(self.test_table).where(
            self.rxn_column.has_substructure("x' OR 1=1 -- >> [C:1]")
        )

        compiled = stmt.compile(dialect=postgresql.dialect())
        sql = str(compiled)

        assert "reaction_from_smarts" in sql
        assert "x' OR 1=1 -- >> [C:1]" not in sql
        assert "x' OR 1=1 -- >> [C:1]" in compiled.params.values()

    def test_bindparam_queries_compile_via_reaction_coercion(self):
        stmt = select(self.test_table).where(
            self.rxn_column.equals(bindparam("query_rxn"))
        )

        compiled = stmt.compile(dialect=postgresql.dialect())
        sql = str(compiled)

        assert "@=" in sql
        assert "reaction_from_smarts" in sql
        assert "%(query_rxn)s" in sql

    def test_query_column_expressions_are_preserved(self):
        stmt = select(self.test_table).where(
            self.rxn_column.has_substructure(self.test_table.c.query_rxn)
        )

        compiled = str(
            stmt.compile(
                dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
            )
        )

        assert "test_reactions.query_rxn" in compiled
        assert "'test_reactions.query_rxn'" not in compiled
        assert "reaction_from_smarts" not in compiled


class TestComparatorReturnTypes:
    """Test that comparator methods return properly typed expressions."""

    def setup_method(self):
        self.metadata = MetaData()
        self.test_table = Table(
            "test_compounds",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("structure", RdkitMol()),
            Column("fingerprint", RdkitBitFingerprint()),
            Column("reaction", RdkitReaction()),
        )

    def test_has_substructure_returns_column_element(self):
        result = self.test_table.c.structure.has_substructure("CCO")
        assert isinstance(result, ColumnElement)

    def test_is_substructure_of_returns_column_element(self):
        result = self.test_table.c.structure.is_substructure_of("CCO")
        assert isinstance(result, ColumnElement)

    def test_equals_returns_column_element(self):
        result = self.test_table.c.structure.equals("CCO")
        assert isinstance(result, ColumnElement)

    def test_has_query_substructure_returns_column_element(self):
        result = self.test_table.c.structure.has_query_substructure(
            cast("[cH]", RdkitQMol)
        )
        assert isinstance(result, ColumnElement)

    def test_is_query_substructure_of_returns_column_element(self):
        result = self.test_table.c.structure.is_query_substructure_of(
            cast("[cH]", RdkitQMol)
        )
        assert isinstance(result, ColumnElement)

    def test_tanimoto_returns_column_element(self):
        result = self.test_table.c.fingerprint.tanimoto(b"fp")
        assert isinstance(result, ColumnElement)

    def test_dice_returns_column_element(self):
        result = self.test_table.c.fingerprint.dice(b"fp")
        assert isinstance(result, ColumnElement)

    def test_nearest_neighbors_returns_column_element(self):
        result = self.test_table.c.fingerprint.nearest_neighbors(b"fp")
        assert isinstance(result, ColumnElement)

    def test_reaction_equals_returns_column_element(self):
        result = self.test_table.c.reaction.equals("[C:1]>>[C:1]")
        assert isinstance(result, ColumnElement)

    def test_reaction_not_equals_returns_column_element(self):
        result = self.test_table.c.reaction.not_equals("[C:1]>>[C:1][O]")
        assert isinstance(result, ColumnElement)


class TestRdkitComparatorExports:
    """Test comparators are exported from the rdkit subpackage."""

    def test_import_mol_comparator_from_rdkit(self):
        assert RdkitMolComparator is not None

    def test_import_reaction_comparator_from_rdkit(self):
        assert RdkitReactionComparator is not None


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
