"""Tests for alembic helpers module."""

from unittest.mock import Mock, patch

import pytest
from alembic.autogenerate.api import render_python_code
from alembic.migration import MigrationContext
from alembic.operations.ops import CreateIndexOp, UpgradeOps
from sqlalchemy import Column, MetaData, Table, text

from molalchemy.alembic_helpers import (
    add_rdkit_extension,
    drop_rdkit_extension,
    render_item,
)
from molalchemy.bingo.index import (
    BingoBinaryMolIndex,
    BingoBinaryRxnIndex,
    BingoMolIndex,
    BingoRxnIndex,
)
from molalchemy.bingo.types import (
    BingoBinaryMol,
    BingoBinaryReaction,
    BingoMol,
    BingoReaction,
)
from molalchemy.rdkit.index import RdkitIndex
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
    (
        RdkitMol(),
        "molalchemy.rdkit.types",
        "RdkitMol",
        "RdkitMol(return_type='smiles')",
    ),
    (
        RdkitMol(return_type="mol"),
        "molalchemy.rdkit.types",
        "RdkitMol",
        "RdkitMol(return_type='mol')",
    ),
    (
        RdkitMol(return_type="bytes"),
        "molalchemy.rdkit.types",
        "RdkitMol",
        "RdkitMol(return_type='bytes')",
    ),
    (
        RdkitBitFingerprint(),
        "molalchemy.rdkit.types",
        "RdkitBitFingerprint",
        "RdkitBitFingerprint()",
    ),
    (
        RdkitSparseFingerprint(),
        "molalchemy.rdkit.types",
        "RdkitSparseFingerprint",
        "RdkitSparseFingerprint()",
    ),
    (
        RdkitReaction(),
        "molalchemy.rdkit.types",
        "RdkitReaction",
        "RdkitReaction(return_type='smiles')",
    ),
    (
        RdkitReaction(return_type="mol"),
        "molalchemy.rdkit.types",
        "RdkitReaction",
        "RdkitReaction(return_type='mol')",
    ),
    (RdkitQMol(), "molalchemy.rdkit.types", "RdkitQMol", "RdkitQMol()"),
    (RdkitXQMol(), "molalchemy.rdkit.types", "RdkitXQMol", "RdkitXQMol()"),
    # Bingo types
    (BingoMol(), "molalchemy.bingo.types", "BingoMol", "BingoMol()"),
    (
        BingoBinaryMol(),
        "molalchemy.bingo.types",
        "BingoBinaryMol",
        "BingoBinaryMol(preserve_pos=False, return_type='smiles')",
    ),
    (
        BingoBinaryMol(preserve_pos=True, return_type="molfile"),
        "molalchemy.bingo.types",
        "BingoBinaryMol",
        "BingoBinaryMol(preserve_pos=True, return_type='molfile')",
    ),
    (BingoReaction(), "molalchemy.bingo.types", "BingoReaction", "BingoReaction()"),
    (
        BingoBinaryReaction(),
        "molalchemy.bingo.types",
        "BingoBinaryReaction",
        "BingoBinaryReaction()",
    ),
]


class TestRenderAllTypes:
    """Test render_item for all type variants."""

    @pytest.mark.parametrize(
        ("instance", "expected_module", "class_name", "expected_repr"),
        ALL_TYPES,
        ids=[t[3] for t in ALL_TYPES],
    )
    def test_render_all_types(
        self, instance, expected_module, class_name, expected_repr
    ):
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
    def test_rendered_type_is_valid_constructor(
        self, instance, expected_module, class_name, expected_repr
    ):
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
        assert render_item("index", Mock(), autogen_context) is False
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


# Index variants with the PostgreSQL options Alembic must preserve.
ALL_INDEXES = [
    (
        RdkitIndex,
        RdkitMol,
        ("postgresql_using='gist'",),
    ),
    (
        BingoMolIndex,
        BingoMol,
        (
            "postgresql_using='bingo_idx'",
            "postgresql_ops={'structure': 'bingo.molecule'}",
        ),
    ),
    (
        BingoBinaryMolIndex,
        BingoBinaryMol,
        (
            "postgresql_using='bingo_idx'",
            "postgresql_ops={'structure': 'bingo.bmolecule'}",
        ),
    ),
    (
        BingoRxnIndex,
        BingoReaction,
        (
            "postgresql_using='bingo_idx'",
            "postgresql_ops={'structure': 'bingo.reaction'}",
        ),
    ),
    (
        BingoBinaryRxnIndex,
        BingoBinaryReaction,
        (
            "postgresql_using='bingo_idx'",
            "postgresql_ops={'structure': 'bingo.breaction'}",
        ),
    ),
]


def render_index_operation(index, render_item_callback=render_item):
    """Render an Alembic index operation with the offline PostgreSQL dialect."""
    migration_context = MigrationContext.configure(dialect_name="postgresql")
    upgrade_ops = UpgradeOps(ops=[CreateIndexOp.from_index(index)])
    return render_python_code(
        upgrade_ops,
        render_item=render_item_callback,
        migration_context=migration_context,
    )


class TestRenderAllIndexes:
    """Test Alembic's actual index operation renderer."""

    @pytest.mark.parametrize(
        ("index_type", "column_type", "expected_options"),
        ALL_INDEXES,
        ids=[index_type.__name__ for index_type, _, _ in ALL_INDEXES],
    )
    def test_alembic_renders_generic_index_operation(
        self, index_type, column_type, expected_options
    ):
        """Alembic preserves cartridge options in generic index operations."""
        metadata = MetaData()
        table = Table("items", metadata, Column("structure", column_type()))
        index = index_type("ix_items_structure", table.c.structure)

        rendered = render_index_operation(index)

        assert (
            "op.create_index('ix_items_structure', 'items', ['structure'], "
            "unique=False"
        ) in rendered
        for expected_option in expected_options:
            assert expected_option in rendered
        assert "molalchemy.bingo.index" not in rendered
        assert "molalchemy.rdkit.index" not in rendered
        compile(f"def upgrade():\n{rendered}", "<generated migration>", "exec")

    def test_alembic_does_not_call_custom_renderer_for_indexes(self):
        """Alembic index operations bypass the custom render_item hook."""
        metadata = MetaData()
        table = Table("items", metadata, Column("structure", BingoMol()))
        index = BingoMolIndex("ix_items_structure", table.c.structure)
        render_item_callback = Mock(return_value=False)

        render_index_operation(index, render_item_callback)

        render_item_callback.assert_not_called()

    def test_alembic_preserves_standard_index_options(self):
        """Index options survive conversion to an Alembic operation."""
        metadata = MetaData()
        table = Table("items", metadata, Column("structure", BingoMol()))
        index = BingoMolIndex(
            "ix_items_structure",
            table.c.structure,
            unique=True,
            postgresql_where=text("structure IS NOT NULL"),
            postgresql_with={"fillfactor": 70},
            postgresql_tablespace="fastspace",
            postgresql_concurrently=True,
        )

        rendered = render_index_operation(index)

        assert "unique=True" in rendered
        assert "postgresql_where=sa.text('structure IS NOT NULL')" in rendered
        assert "postgresql_with={'fillfactor': 70}" in rendered
        assert "postgresql_tablespace='fastspace'" in rendered
        assert "postgresql_concurrently=True" in rendered
