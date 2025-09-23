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


def equals(mol_column: ColumnElement[RdkitMol], query: str) -> BinaryExpression:
    return mol_column.op("@=")(query)


def has_substructure(
    mol_column: ColumnElement[RdkitMol], query: str
) -> BinaryExpression:
    return mol_column.op("@>")(query)


def to_binary(mol: ColumnElement[RdkitMol], **kwargs) -> Function[bytes]:
    return func.mol_send(mol, **kwargs)


def to_json(mol: ColumnElement[RdkitMol], **kwargs) -> Function[str]:
    return func.mol_to_json(mol, **kwargs)


def to_cxsmiles(mol: ColumnElement[RdkitMol], **kwargs) -> Function[str]:
    return func.mol_to_cxsmiles(mol, **kwargs)


def to_smarts(mol: ColumnElement[RdkitMol], **kwargs) -> Function[str]:
    return func.mol_to_smarts(mol, **kwargs)


def to_pkl(mol: ColumnElement[RdkitMol], **kwargs) -> Function[bytes]:
    return func.mol_to_pkl(mol, **kwargs)


def from_smiles(smiles: ColumnElement[str], **kwargs) -> Function[RdkitMol]:
    return func.mol_from_smiles(cast(smiles, CString), **kwargs)


def from_pkl(pkl: ColumnElement[bytes], **kwargs) -> Function[RdkitMol]:
    return func.mol_from_pkl(pkl, **kwargs)


def maccs_fp(mol: ColumnElement[RdkitMol], **kwargs) -> Function[RdkitBitFingerprint]:
    return func.maccs_fp(mol, **kwargs)


def morgan_fp(
    mol: ColumnElement[RdkitMol], radius: int = 2, **kwargs
) -> Function[RdkitSparseFingerprint]:
    return func.morgan_fp(mol, radius, **kwargs)


def morganbv_fp(
    mol: ColumnElement[RdkitMol], radius: int = 2, **kwargs
) -> Function[RdkitBitFingerprint]:
    return func.morganbv_fp(mol, radius, **kwargs)


def torsion_fp(
    mol: ColumnElement[RdkitMol], **kwargs
) -> Function[RdkitSparseFingerprint]:
    return func.torsion_fp(mol, **kwargs)


def mol_murckoscaffold(mol: ColumnElement[RdkitMol], **kwargs) -> Function[RdkitMol]:
    return func.mol_murckoscaffold(mol, **kwargs)


def mol_tpsa(mol: ColumnElement[RdkitMol], **kwargs) -> Function[float]:
    return func.mol_tpsa(mol, **kwargs)


def mol_logp(mol: ColumnElement[RdkitMol], **kwargs) -> Function[float]:
    return func.mol_logp(mol, **kwargs)


def mol_num_atoms(mol: ColumnElement[RdkitMol], **kwargs) -> Function[int]:
    return func.mol_num_atoms(mol, **kwargs)


def mol_hba(mol: ColumnElement[RdkitMol], **kwargs) -> Function[int]:
    return func.mol_hba(mol, **kwargs)


def mol_hbd(mol: ColumnElement[RdkitMol], **kwargs) -> Function[int]:
    return func.mol_hbd(mol, **kwargs)
