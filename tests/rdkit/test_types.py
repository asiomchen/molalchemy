"""Tests for RDKit types."""

import pytest
from rdkit import Chem
from rdkit.Chem import AllChem, rdChemReactions
from sqlalchemy import Column, Integer, MetaData, String, Table

from molalchemy.rdkit.comparators import RdkitFPComparator, RdkitMolComparator
from molalchemy.rdkit.types import (
    RdkitBitFingerprint,
    RdkitMol,
    RdkitReaction,
    RdkitSparseFingerprint,
)


class TestRdkitMol:
    """Test RdkitMol type."""

    def test_rdkit_mol_cache_ok(self):
        """Test that RdkitMol has cache_ok=True."""
        rdkit_mol = RdkitMol()
        assert rdkit_mol.cache_ok is True

    def test_rdkit_mol_col_spec(self):
        """Test that RdkitMol returns correct column specification."""
        rdkit_mol = RdkitMol()
        assert rdkit_mol.get_col_spec() == "mol"

    def test_rdkit_mol_comparator_factory(self):
        """Test that RdkitMol uses RdkitMolComparator."""
        rdkit_mol = RdkitMol()
        assert rdkit_mol.comparator_factory == RdkitMolComparator

    def test_rdkit_mol_default_return_type(self):
        """Test that RdkitMol has default return_type='smiles'."""
        rdkit_mol = RdkitMol()
        assert rdkit_mol.return_type == "smiles"

    def test_rdkit_mol_custom_return_types(self):
        """Test RdkitMol with different return types."""
        mol_smiles = RdkitMol(return_type="smiles")
        mol_bytes = RdkitMol(return_type="bytes")
        mol_mol = RdkitMol(return_type="mol")

        assert mol_smiles.return_type == "smiles"
        assert mol_bytes.return_type == "bytes"
        assert mol_mol.return_type == "mol"

    def test_rdkit_mol_in_table_definition(self):
        """Test RdkitMol can be used in table definition."""
        metadata = MetaData()
        test_table = Table(
            "test_molecules",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("mol", RdkitMol()),
        )

        # Should not raise any exceptions
        assert test_table.c.mol.type.__class__ == RdkitMol
        assert isinstance(test_table.c.mol.type, RdkitMol)

    @pytest.mark.parametrize("return_type", ["smiles", "bytes", "mol"])
    @pytest.mark.parametrize("value", ["CCO", "c1ccccc1"])
    def test_result_processor(self, return_type, value):
        """Test result_processor for different return types and values."""
        rdkit_mol = RdkitMol(return_type=return_type)
        processor = rdkit_mol.result_processor(None, None)
        input_value = value
        if return_type != "smiles":
            input_value = Chem.MolFromSmiles(value).ToBinary()
        processed = processor(input_value)

        if return_type == "smiles":
            assert processed == value
        elif return_type == "bytes":
            mol_bytes = Chem.MolFromSmiles(value).ToBinary()
            processed = processor(mol_bytes)
            assert processed == mol_bytes
        elif return_type == "mol":
            mol_bytes = Chem.MolFromSmiles(value).ToBinary()
            processed = processor(mol_bytes)
            assert isinstance(processed, Chem.Mol)
            assert Chem.MolToSmiles(processed) == value

    def test_bind_processor(self):
        """Test bind_processor for different input types."""
        rdkit_mol = RdkitMol()
        processor = rdkit_mol.bind_processor(None)

        # Test with SMILES string
        smiles = "CCO"
        processed = processor(smiles)
        assert isinstance(processed, bytes)
        assert Chem.MolToSmiles(Chem.Mol(processed)) == smiles

        # Test with Chem.Mol object
        mol = Chem.MolFromSmiles(smiles)
        processed = processor(mol)
        assert isinstance(processed, bytes)
        assert Chem.MolToSmiles(Chem.Mol(processed)) == smiles

        # Test with None
        processed = processor(None)
        assert processed is None

        # Test with invalid type
        with pytest.raises(ValueError):
            processor(123)  # Invalid type


class TestRdkitBitFingerprint:
    """Test RdkitBitFingerprint type."""

    def test_rdkit_bit_fingerprint_cache_ok(self):
        """Test that RdkitBitFingerprint has cache_ok=True."""
        rdkit_fp = RdkitBitFingerprint()
        assert rdkit_fp.cache_ok is True

    def test_rdkit_bit_fingerprint_col_spec(self):
        """Test that RdkitBitFingerprint returns correct column specification."""
        rdkit_fp = RdkitBitFingerprint()
        assert rdkit_fp.get_col_spec() == "bfp"

    def test_rdkit_bit_fingerprint_comparator_factory(self):
        """Test that RdkitBitFingerprint uses RdkitFPComparator."""
        rdkit_fp = RdkitBitFingerprint()
        assert rdkit_fp.comparator_factory == RdkitFPComparator

    def test_rdkit_bit_fingerprint_in_table_definition(self):
        """Test RdkitBitFingerprint can be used in table definition."""
        metadata = MetaData()
        test_table = Table(
            "test_fingerprints",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("mol_id", Integer),
            Column("fingerprint", RdkitBitFingerprint()),
        )

        # Should not raise any exceptions
        assert test_table.c.fingerprint.type.__class__ == RdkitBitFingerprint
        assert isinstance(test_table.c.fingerprint.type, RdkitBitFingerprint)

    @pytest.mark.parametrize("return_type", ["smiles", "bytes", "mol"])
    @pytest.mark.parametrize(
        "value", ["C.C>>CC", "[C:1](=[O:2])O.[N:3]>>[C:1](=[O:2])[N:3]"]
    )
    def test_result_processor(self, return_type, value):
        """Test result_processor for different return types and values."""
        rdkit_mol = RdkitReaction(return_type=return_type)
        processor = rdkit_mol.result_processor(None, None)
        input_value = value
        if return_type != "smiles":
            input_value = rdChemReactions.ReactionFromSmarts(value).ToBinary()
        processed = processor(input_value)

        if return_type == "smiles":
            assert processed == value
        elif return_type == "bytes":
            mol_bytes = rdChemReactions.ReactionFromSmarts(value).ToBinary()
            processed = processor(mol_bytes)
            assert processed == mol_bytes
        elif return_type == "mol":
            mol_bytes = rdChemReactions.ReactionFromSmarts(value).ToBinary()
            processed = processor(mol_bytes)
            assert isinstance(processed, AllChem.ChemicalReaction)
            assert rdChemReactions.ReactionToSmarts(processed) == value


class TestRdkitSparseFingerprint:
    """Test RdkitSparseFingerprint type."""

    def test_rdkit_sparse_fingerprint_cache_ok(self):
        """Test that RdkitSparseFingerprint has cache_ok=True."""
        rdkit_sfp = RdkitSparseFingerprint()
        assert rdkit_sfp.cache_ok is True

    def test_rdkit_sparse_fingerprint_col_spec(self):
        """Test that RdkitSparseFingerprint returns correct column specification."""
        rdkit_sfp = RdkitSparseFingerprint()
        assert rdkit_sfp.get_col_spec() == "sfp"

    def test_rdkit_sparse_fingerprint_comparator_factory(self):
        """Test that RdkitSparseFingerprint uses RdkitFPComparator."""
        rdkit_sfp = RdkitSparseFingerprint()
        assert rdkit_sfp.comparator_factory == RdkitFPComparator

    def test_rdkit_sparse_fingerprint_in_table_definition(self):
        """Test RdkitSparseFingerprint can be used in table definition."""
        metadata = MetaData()
        test_table = Table(
            "test_sparse_fingerprints",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("mol_id", Integer),
            Column("fingerprint", RdkitSparseFingerprint()),
        )

        # Should not raise any exceptions
        assert test_table.c.fingerprint.type.__class__ == RdkitSparseFingerprint
        assert isinstance(test_table.c.fingerprint.type, RdkitSparseFingerprint)


class TestRdkitReaction:
    """Test RdkitReaction type."""

    def test_rdkit_reaction_cache_ok(self):
        """Test that RdkitReaction has cache_ok=True."""
        rdkit_rxn = RdkitReaction()
        assert rdkit_rxn.cache_ok is True

    def test_rdkit_reaction_col_spec(self):
        """Test that RdkitReaction returns correct column specification."""
        rdkit_rxn = RdkitReaction()
        assert rdkit_rxn.get_col_spec() == "reaction"

    def test_rdkit_reaction_comparator_factory(self):
        """Test that RdkitReaction uses RdkitMolComparator."""
        rdkit_rxn = RdkitReaction()
        assert rdkit_rxn.comparator_factory == RdkitMolComparator

    def test_rdkit_reaction_default_return_type(self):
        """Test that RdkitReaction has default return_type='smiles'."""
        rdkit_rxn = RdkitReaction()
        assert rdkit_rxn.return_type == "smiles"

    def test_rdkit_reaction_custom_return_types(self):
        """Test RdkitReaction with different return types."""
        rxn_smiles = RdkitReaction(return_type="smiles")
        rxn_bytes = RdkitReaction(return_type="bytes")
        rxn_mol = RdkitReaction(return_type="mol")

        assert rxn_smiles.return_type == "smiles"
        assert rxn_bytes.return_type == "bytes"
        assert rxn_mol.return_type == "mol"

    def test_rdkit_reaction_in_table_definition(self):
        """Test RdkitReaction can be used in table definition."""
        metadata = MetaData()
        test_table = Table(
            "test_reactions",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("reaction", RdkitReaction()),
        )

        # Should not raise any exceptions
        assert test_table.c.reaction.type.__class__ == RdkitReaction
        assert isinstance(test_table.c.reaction.type, RdkitReaction)


class TestTypesIntegration:
    """Integration tests for RDKit types."""

    def test_fingerprint_types_have_same_comparator(self):
        """Test that both fingerprint types use the same comparator."""
        rdkit_bfp = RdkitBitFingerprint()
        rdkit_sfp = RdkitSparseFingerprint()

        assert rdkit_bfp.comparator_factory == rdkit_sfp.comparator_factory
        assert rdkit_bfp.comparator_factory == RdkitFPComparator

    def test_mol_and_reaction_have_same_comparator(self):
        """Test that mol and reaction types use the same comparator."""
        rdkit_mol = RdkitMol()
        rdkit_rxn = RdkitReaction()

        assert rdkit_mol.comparator_factory == rdkit_rxn.comparator_factory
        assert rdkit_mol.comparator_factory == RdkitMolComparator

    def test_all_types_are_cache_ok(self):
        """Test that all types have cache_ok=True."""
        rdkit_mol = RdkitMol()
        rdkit_bfp = RdkitBitFingerprint()
        rdkit_sfp = RdkitSparseFingerprint()
        rdkit_rxn = RdkitReaction()

        assert rdkit_mol.cache_ok is True
        assert rdkit_bfp.cache_ok is True
        assert rdkit_sfp.cache_ok is True
        assert rdkit_rxn.cache_ok is True
