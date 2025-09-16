"""
Collection of RDKit PostgreSQL functions for molecular structure search and analysis.

This module provides static methods that wrap RDKit PostgreSQL functions for performing
various chemical reaction operations including reaction substructure search, exact matching,
and format conversions.
"""

from sqlalchemy.sql import func, cast
from sqlalchemy import Function
from sqlalchemy.sql.elements import ClauseElement, ColumnElement
from molalchemy.types import CString


def equals(mol_column: ColumnElement, query: str) -> ClauseElement:
    return mol_column.op("@=")(query)


def has_substructure(mol_column: ColumnElement, query: str) -> ClauseElement:
    return mol_column.op("@>")(query)


def to_binary(mol: ColumnElement, **kwargs) -> Function[bytes]:
    return func.mol_send(mol, **kwargs)


def mol_from_smiles(smiles: str, **kwargs) -> ClauseElement:
    return func.mol_from_smiles(cast(smiles, CString), **kwargs)


def maccs_fp(mol: ColumnElement, **kwargs) -> ClauseElement:
    return func.maccs_fp(mol, **kwargs)
