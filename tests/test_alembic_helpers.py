"""Tests for alembic helpers module."""

from unittest.mock import Mock, patch

from molalchemy.alembic_helpers import (
    add_rdkit_extension,
    drop_rdkit_extension,
    render_item,
)
from molalchemy.bingo.types import BingoMol
from molalchemy.rdkit.types import RdkitMol


class TestRenderItem:
    """Test cases for the render_item function."""

    def test_render_rdkit_type(self):
        """Test rendering of RDKit types adds correct import and returns repr."""
        # Create a mock autogen_context with an imports set
        autogen_context = Mock()
        autogen_context.imports = set()

        # Create an RDKit type instance
        rdkit_mol = RdkitMol()

        # Call render_item
        result = render_item("type", rdkit_mol, autogen_context)

        # Check that the correct import was added
        expected_import = "from molalchemy.rdkit.types import RdkitMol"
        assert expected_import in autogen_context.imports

        # Check that the repr of the object was returned
        assert result == repr(rdkit_mol)

    def test_render_bingo_type(self):
        """Test rendering of Bingo types adds correct import and returns repr."""
        # Create a mock autogen_context with an imports set
        autogen_context = Mock()
        autogen_context.imports = set()

        # Create a Bingo type instance
        bingo_mol = BingoMol()

        # Call render_item
        result = render_item("type", bingo_mol, autogen_context)

        # Check that the correct import was added
        expected_import = "from molalchemy.bingo.types import BingoMol"
        assert expected_import in autogen_context.imports

        # Check that the repr of the object was returned
        assert result == repr(bingo_mol)

    def test_render_non_type_object(self):
        """Test rendering of non-type objects returns False."""
        autogen_context = Mock()
        autogen_context.imports = set()

        # Test with different object types
        result = render_item("column", Mock(), autogen_context)
        assert result is False

        result = render_item("table", Mock(), autogen_context)
        assert result is False

        # Ensure no imports were added
        assert len(autogen_context.imports) == 0

    def test_render_unknown_type(self):
        """Test rendering of unknown type objects returns False."""
        autogen_context = Mock()
        autogen_context.imports = set()

        # Create a mock object that doesn't inherit from base types
        unknown_type = Mock()

        # Call render_item with "type" but unknown object
        result = render_item("type", unknown_type, autogen_context)

        # Should return False for unknown types
        assert result is False

        # Ensure no imports were added
        assert len(autogen_context.imports) == 0

    def test_render_item_with_existing_imports(self):
        """Test that render_item doesn't duplicate imports."""
        autogen_context = Mock()
        autogen_context.imports = {"from molalchemy.rdkit.types import RdkitMol"}

        rdkit_mol = RdkitMol()

        # Call render_item
        result = render_item("type", rdkit_mol, autogen_context)

        # Should still work and return repr
        assert result == repr(rdkit_mol)

        # Should have only one import (set prevents duplicates)
        assert len(autogen_context.imports) == 1
        assert "from molalchemy.rdkit.types import RdkitMol" in autogen_context.imports


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
