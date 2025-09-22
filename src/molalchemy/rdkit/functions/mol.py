"""
Collection of RDKit PostgreSQL functions for molecular structure search and analysis.

This module provides static methods that wrap RDKit PostgreSQL functions for performing
various chemical reaction operations including reaction substructure search, exact matching,
and format conversions.
"""

from __future__ import annotations

from sqlalchemy import BinaryExpression, Function
from sqlalchemy.sql import cast, func
from sqlalchemy.sql.elements import ColumnElement

from molalchemy.rdkit.types import RdkitBitFingerprint, RdkitMol, RdkitSparseFingerprint
from molalchemy.types import CString


def equals(mol_column: ColumnElement, query: str) -> BinaryExpression:
    return mol_column.op("@=")(query)


def has_substructure(mol_column: ColumnElement, query: str) -> BinaryExpression:
    return mol_column.op("@>")(query)


def to_binary(mol: ColumnElement, **kwargs) -> Function[bytes]:
    return func.mol_send(mol, **kwargs)


def to_json(mol: ColumnElement, **kwargs) -> Function[str]:
    return func.mol_to_json(mol, **kwargs)


def to_cxsmiles(mol: ColumnElement, **kwargs) -> Function[str]:
    return func.mol_to_cxsmiles(mol, **kwargs)


def to_smarts(mol: ColumnElement, **kwargs) -> Function[str]:
    return func.mol_to_smarts(mol, **kwargs)


def mol_from_smiles(smiles: str, **kwargs) -> Function[RdkitMol]:
    return func.mol_from_smiles(cast(smiles, CString), **kwargs)


def maccs_fp(mol: ColumnElement, **kwargs) -> Function[RdkitBitFingerprint]:
    return func.maccs_fp(mol, **kwargs)


def morgan_fp(
    mol: ColumnElement, radius: int = 2, **kwargs
) -> Function[RdkitSparseFingerprint]:
    return func.morgan_fp(mol, radius, **kwargs)


def torsion_fp(mol: ColumnElement, **kwargs) -> Function[RdkitSparseFingerprint]:
    return func.torsion_fp(mol, **kwargs)
