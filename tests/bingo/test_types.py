"""Tests for bingo types."""

import pytest
from sqlalchemy import Column, Integer, MetaData, String, Table

from molalchemy.bingo.comparators import BingoMolComparator
from molalchemy.bingo.types import BingoBinaryMol, BingoMol


class TestBingoMol:
    """Test BingoMol type."""

    def test_bingo_mol_cache_ok(self):
        """Test that BingoMol has cache_ok=True."""
        bingo_mol = BingoMol()
        assert bingo_mol.cache_ok is True

    def test_bingo_mol_col_spec(self):
        """Test that BingoMol returns correct column specification."""
        bingo_mol = BingoMol()
        assert bingo_mol.get_col_spec() == "varchar"

    def test_bingo_mol_comparator_factory(self):
        """Test that BingoMol uses BingoMolComparator."""
        bingo_mol = BingoMol()
        assert bingo_mol.comparator_factory == BingoMolComparator

    def test_bingo_mol_in_table_definition(self):
        """Test BingoMol can be used in table definition."""
        metadata = MetaData()
        test_table = Table(
            "test_molecules",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("mol", BingoMol()),
        )

        # Should not raise any exceptions
        assert test_table.c.mol.type.__class__ == BingoMol
        assert isinstance(test_table.c.mol.type, BingoMol)


class TestBingoBinaryMol:
    """Test BingoBinaryMol type."""

    def test_bingo_binary_mol_cache_ok(self):
        """Test that BingoBinaryMol has cache_ok=True."""
        bingo_binary_mol = BingoBinaryMol()
        assert bingo_binary_mol.cache_ok is True

    def test_bingo_binary_mol_col_spec(self):
        """Test that BingoBinaryMol returns correct column specification."""
        bingo_binary_mol = BingoBinaryMol()
        assert bingo_binary_mol.get_col_spec() == "bytea"

    def test_bingo_binary_mol_comparator_factory(self):
        """Test that BingoBinaryMol uses BingoMolComparator."""
        bingo_binary_mol = BingoBinaryMol()
        assert bingo_binary_mol.comparator_factory == BingoMolComparator

    def test_bingo_binary_mol_in_table_definition(self):
        """Test BingoBinaryMol can be used in table definition."""
        metadata = MetaData()
        test_table = Table(
            "test_binary_molecules",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("mol", BingoBinaryMol()),
        )

        # Should not raise any exceptions
        assert test_table.c.mol.type.__class__ == BingoBinaryMol
        assert isinstance(test_table.c.mol.type, BingoBinaryMol)

    @pytest.mark.parametrize(
        "return_type, expected_sql",
        [
            ("smiles", "Bingo.smiles(mol)"),
            ("molfile", "Bingo.molfile(mol)"),
            ("cml", "Bingo.cml(mol)"),
            ("bytes", "mol"),
        ],
    )
    def test_column_expression(self, return_type, expected_sql):
        """Test column_expression returns correct SQL for smiles."""
        bingo_binary_mol = BingoBinaryMol(return_type=return_type)
        col = Column("mol", bingo_binary_mol)
        expr = bingo_binary_mol.column_expression(col)
        assert str(expr) == expected_sql


class TestTypesIntegration:
    """Integration tests for bingo types."""

    def test_both_types_have_same_comparator(self):
        """Test that both types use the same comparator."""
        bingo_mol = BingoMol()
        bingo_binary_mol = BingoBinaryMol()

        assert bingo_mol.comparator_factory == bingo_binary_mol.comparator_factory
        assert bingo_mol.comparator_factory == BingoMolComparator

    def test_both_types_are_cache_ok(self):
        """Test that both types have cache_ok=True."""
        bingo_mol = BingoMol()
        bingo_binary_mol = BingoBinaryMol()

        assert bingo_mol.cache_ok is True
        assert bingo_binary_mol.cache_ok is True
