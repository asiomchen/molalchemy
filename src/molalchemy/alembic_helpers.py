"""Alembic helpers for RDKit and Bingo PostgreSQL cartridge integration.

This module provides utilities for Alembic migrations when using RDKit types and indices.
It automatically handles the necessary imports and some utility functions for RDKit and Bingo functionality.
"""

from alembic import op
from loguru import logger

from molalchemy.bingo.types import BingoBaseType
from molalchemy.rdkit.types import RdkitBaseType

_TYPE_TO_MODULE = {
    RdkitBaseType: "molalchemy.rdkit.types",
    BingoBaseType: "molalchemy.bingo.types",
}


def add_rdkit_extension():
    """Add the RDKit extension to PostgreSQL.

    This function creates the RDKit extension if it doesn't already exist.
    It should be called at the beginning of upgrade functions that use RDKit types.
    """
    op.execute("CREATE EXTENSION IF NOT EXISTS rdkit;")


def drop_rdkit_extension():
    """Drop the RDKit extension from PostgreSQL.

    This function removes the RDKit extension if it exists.
    It should be called at the end of downgrade functions that remove all RDKit usage.
    """
    op.execute("DROP EXTENSION IF EXISTS rdkit;")


def render_item(obj_type, obj, autogen_context):
    logger.debug(f"Rendering item: {obj_type}, {obj}")
    if obj_type == "type":
        import_name = obj.__class__.__name__
        for base_type, module in _TYPE_TO_MODULE.items():
            if isinstance(obj, base_type):
                autogen_context.imports.add(f"from {module} import {import_name}")
                return f"{obj!r}"

    # Default rendering for other objects
    return False
