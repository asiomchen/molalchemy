"""Tests for alembic helpers module."""

from unittest.mock import Mock, patch

import pytest

from molalchemy.alembic_helpers import (
    add_rdkit_extension,
    drop_rdkit_extension,
    render_item,
)
from molalchemy.bingo.types import BingoBinaryMol, BingoBinaryReaction, BingoMol, BingoReaction
from molalchemy.rdkit.types import (
    RdkitBitFingerprint,
    RdkitMol,
    RdkitQMol,
    RdkitReaction,
    RdkitSparseFingerprint,
    RdkitXQMol,
)

# All type variants with expected module, class name, and constructor repr
ALL_TYPES = [
    # RDKit types
    (RdkitMol(), "molalchemy.rdkit.types", "RdkitMol", "RdkitMol(return_type='smiles')"),
    (RdkitMol(return_type="mol"), "molalchemy.rdkit.types", "RdkitMol", "RdkitMol(return_type='mol')"),
    (RdkitMol(return_type="bytes"), "molalchemy.rdkit.types", "RdkitMol", "RdkitMol(return_type='bytes')"),
    (RdkitBitFingerprint(), "molalchemy.rdkit.types", "RdkitBitFingerprint", "RdkitBitFingerprint()"),
    (RdkitSparseFingerprint(), "molalchemy.rdkit.types", "RdkitSparseFingerprint", "RdkitSparseFingerprint()"),
    (RdkitReaction(), "molalchemy.rdkit.types", "RdkitReaction", "RdkitReaction(return_type='smiles')"),
    (RdkitReaction(return_type="mol"), "molalchemy.rdkit.types", "RdkitReaction", "RdkitReaction(return_type='mol')"),
    (RdkitQMol(), "molalchemy.rdkit.types", "RdkitQMol", "RdkitQMol()"),
    (RdkitXQMol(), "molalchemy.rdkit.types", "RdkitXQMol", "RdkitXQMol()"),
    # Bingo types
    (BingoMol(), "molalchemy.bingo.types", "BingoMol", "BingoMol()"),
    (BingoBinaryMol(), "molalchemy.bingo.types", "BingoBinaryMol", "BingoBinaryMol(preserve_pos=False, return_type='smiles')"),
    (BingoBinaryMol(preserve_pos=True, return_type="molfile"), "molalchemy.bingo.types", "BingoBinaryMol", "BingoBinaryMol(preserve_pos=True, return_type='molfile')"),
    (BingoReaction(), "molalchemy.bingo.types", "BingoReaction", "BingoReaction()"),
    (BingoBinaryReaction(), "molalchemy.bingo.types", "BingoBinaryReaction", "BingoBinaryReaction()"),
]


class TestRenderAllTypes:
    """Test render_item for all type variants."""

    @pytest.mark.parametrize(
        ("instance", "expected_module", "class_name", "expected_repr"),
        ALL_TYPES,
        ids=[t[3] for t in ALL_TYPES],
    )
    def test_render_all_types(self, instance, expected_module, class_name, expected_repr):
        """Test that render_item produces correct import and repr for every type."""
        autogen_context = Mock()
        autogen_context.imports = set()

        result = render_item("type", instance, autogen_context)

        expected_import = f"from {expected_module} import {class_name}"
        assert expected_import in autogen_context.imports
        assert result == expected_repr

    @pytest.mark.parametrize(
        ("instance", "expected_module", "class_name", "expected_repr"),
        ALL_TYPES,
        ids=[t[3] for t in ALL_TYPES],
    )
    def test_repr_roundtrip(self, instance, expected_module, class_name, expected_repr):
        """Test that eval(repr(instance)) reconstructs the same type."""
        # Import the class into local namespace for eval
        mod = __import__(expected_module, fromlist=[class_name])
        cls = getattr(mod, class_name)
        reconstructed = eval(repr(instance), {class_name: cls})  # noqa: S307
        assert repr(reconstructed) == repr(instance)

    @pytest.mark.parametrize(
        ("instance", "expected_module", "class_name", "expected_repr"),
        ALL_TYPES,
        ids=[t[3] for t in ALL_TYPES],
    )
    def test_rendered_type_is_valid_constructor(self, instance, expected_module, class_name, expected_repr):
        """Test that the rendered string is exactly the constructor call."""
        autogen_context = Mock()
        autogen_context.imports = set()

        result = render_item("type", instance, autogen_context)
        assert result == expected_repr


class TestRenderNonTypes:
    """Test render_item for non-type objects."""

    def test_render_non_type_object(self):
        """Test rendering of non-type objects returns False."""
        autogen_context = Mock()
        autogen_context.imports = set()

        assert render_item("column", Mock(), autogen_context) is False
        assert render_item("table", Mock(), autogen_context) is False
        assert len(autogen_context.imports) == 0

    def test_render_unknown_type(self):
        """Test rendering of unknown type objects returns False."""
        autogen_context = Mock()
        autogen_context.imports = set()

        result = render_item("type", Mock(), autogen_context)

        assert result is False
        assert len(autogen_context.imports) == 0

    def test_render_item_with_existing_imports(self):
        """Test that render_item doesn't duplicate imports."""
        autogen_context = Mock()
        autogen_context.imports = {"from molalchemy.rdkit.types import RdkitMol"}

        result = render_item("type", RdkitMol(), autogen_context)

        assert result == repr(RdkitMol())
        assert len(autogen_context.imports) == 1


class TestExtensionFunctions:
    """Test cases for extension management functions."""

    @patch("molalchemy.alembic_helpers.op")
    def test_add_rdkit_extension(self, mock_op):
        """Test that add_rdkit_extension executes correct SQL."""
        add_rdkit_extension()
        mock_op.execute.assert_called_once_with("CREATE EXTENSION IF NOT EXISTS rdkit;")

    @patch("molalchemy.alembic_helpers.op")
    def test_drop_rdkit_extension(self, mock_op):
        """Test that drop_rdkit_extension executes correct SQL."""
        drop_rdkit_extension()
        mock_op.execute.assert_called_once_with("DROP EXTENSION IF EXISTS rdkit;")

