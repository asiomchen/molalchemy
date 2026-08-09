"""Tests for bingo types."""

import pytest
from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.dialects import postgresql

from molalchemy.bingo.comparators import BingoMolComparator, BingoRxnComparator
from molalchemy.bingo.types import (
    BingoBinaryMol,
    BingoBinaryReaction,
    BingoMol,
    BingoReaction,
)


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

    def test_rejects_unsupported_return_type_at_construction(self):
        with pytest.raises(
            ValueError,
            match=r"return_type must be one of .* got 'invalid'",
        ):
            BingoBinaryMol(return_type="invalid")  # type: ignore[arg-type]

    @pytest.mark.parametrize("return_type", [None, 1, b"smiles"])
    def test_rejects_non_string_return_type(self, return_type):
        with pytest.raises(TypeError, match="return_type must be a str"):
            BingoBinaryMol(return_type=return_type)

    @pytest.mark.parametrize("preserve_pos", [None, 0, 1, "true"])
    def test_rejects_non_boolean_preserve_pos(self, preserve_pos):
        with pytest.raises(TypeError, match="preserve_pos must be a bool"):
            BingoBinaryMol(preserve_pos=preserve_pos)

    def test_configuration_is_immutable_and_cacheable(self):
        bingo_binary_mol = BingoBinaryMol()

        with pytest.raises(AttributeError, match="return_type is immutable"):
            bingo_binary_mol.return_type = "bytes"  # type: ignore[misc]
        with pytest.raises(AttributeError, match="preserve_pos is immutable"):
            bingo_binary_mol.preserve_pos = True  # type: ignore[misc]

        assert bingo_binary_mol.return_type == "smiles"
        assert bingo_binary_mol.preserve_pos is False
        assert bingo_binary_mol._static_cache_key == (
            BingoBinaryMol,
            ("preserve_pos", False),
            ("return_type", "smiles"),
        )

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


class TestBingoReaction:
    """Test BingoReaction type."""

    def test_bingo_reaction_cache_ok(self):
        """Test that BingoReaction has cache_ok=True."""
        bingo_reaction = BingoReaction()
        assert bingo_reaction.cache_ok is True

    def test_bingo_reaction_col_spec(self):
        """Test that BingoReaction returns correct column specification."""
        bingo_reaction = BingoReaction()
        assert bingo_reaction.get_col_spec() == "varchar"

    def test_bingo_reaction_comparator_factory(self):
        """Test that BingoReaction uses BingoRxnComparator."""
        bingo_reaction = BingoReaction()
        assert bingo_reaction.comparator_factory == BingoRxnComparator

    def test_bingo_reaction_in_table_definition(self):
        """Test BingoReaction can be used in table definition."""
        metadata = MetaData()
        test_table = Table(
            "test_reactions",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("rxn", BingoReaction()),
        )

        assert test_table.c.rxn.type.__class__ == BingoReaction
        assert isinstance(test_table.c.rxn.type, BingoReaction)


class TestBingoBinaryReaction:
    """Test BingoBinaryReaction type."""

    def test_bingo_binary_reaction_cache_ok(self):
        """Test that BingoBinaryReaction has cache_ok=True."""
        bingo_binary_reaction = BingoBinaryReaction()
        assert bingo_binary_reaction.cache_ok is True

    def test_bingo_binary_reaction_col_spec(self):
        """Test that BingoBinaryReaction returns correct column specification."""
        bingo_binary_reaction = BingoBinaryReaction()
        assert bingo_binary_reaction.get_col_spec() == "bytea"

    def test_bingo_binary_reaction_comparator_factory(self):
        """Test that BingoBinaryReaction uses BingoRxnComparator."""
        bingo_binary_reaction = BingoBinaryReaction()
        assert bingo_binary_reaction.comparator_factory == BingoRxnComparator

    def test_bingo_binary_reaction_in_table_definition(self):
        """Test BingoBinaryReaction can be used in table definition."""
        metadata = MetaData()
        test_table = Table(
            "test_binary_reactions",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("rxn", BingoBinaryReaction()),
        )

        assert test_table.c.rxn.type.__class__ == BingoBinaryReaction
        assert isinstance(test_table.c.rxn.type, BingoBinaryReaction)

    def test_preserve_pos_is_immutable_and_cacheable(self):
        bingo_binary_reaction = BingoBinaryReaction()

        with pytest.raises(AttributeError, match="preserve_pos is immutable"):
            bingo_binary_reaction.preserve_pos = True  # type: ignore[misc]

        assert bingo_binary_reaction.preserve_pos is False
        assert bingo_binary_reaction._static_cache_key == (
            BingoBinaryReaction,
            ("preserve_pos", False),
        )

    @pytest.mark.parametrize("preserve_pos", [None, 0, 1, "true"])
    def test_rejects_non_boolean_preserve_pos(self, preserve_pos):
        with pytest.raises(TypeError, match="preserve_pos must be a bool"):
            BingoBinaryReaction(preserve_pos=preserve_pos)

    @pytest.mark.parametrize(
        "preserve_pos",
        [
            False,
            True,
        ],
    )
    def test_insert_uses_compact_reaction(self, preserve_pos):
        """Test inserts convert reaction text to Bingo binary reaction data."""
        metadata = MetaData()
        test_table = Table(
            "test_binary_reactions",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("rxn", BingoBinaryReaction(preserve_pos=preserve_pos)),
        )

        stmt = test_table.insert().values(id=1, rxn="CCO>>CC=O")
        compiled_statement = stmt.compile(dialect=postgresql.dialect())
        compiled = str(compiled_statement)

        assert "Bingo.CompactReaction" in compiled
        assert compiled_statement.params["rxn"] == "CCO>>CC=O"
        assert preserve_pos in compiled_statement.params.values()


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

    def test_reaction_types_have_same_comparator(self):
        """Test that both reaction types use the same comparator."""
        bingo_reaction = BingoReaction()
        bingo_binary_reaction = BingoBinaryReaction()

        assert (
            bingo_reaction.comparator_factory
            == bingo_binary_reaction.comparator_factory
        )
        assert bingo_reaction.comparator_factory == BingoRxnComparator

    def test_reaction_types_are_cache_ok(self):
        """Test that both reaction types have cache_ok=True."""
        bingo_reaction = BingoReaction()
        bingo_binary_reaction = BingoBinaryReaction()

        assert bingo_reaction.cache_ok is True
        assert bingo_binary_reaction.cache_ok is True
