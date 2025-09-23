"""
Collection of RDKit PostgreSQL functions for molecular structure search and analysis.

This module provides static methods that wrap RDKit PostgreSQL functions for performing
various molecular operations including substructure search, exact matching, format conversions,
fingerprint generation, scaffold extraction, and molecular property calculations.
"""

from __future__ import annotations

from sqlalchemy import BinaryExpression, Function
from sqlalchemy.sql import cast, func
from sqlalchemy.sql.elements import ColumnElement

from molalchemy.rdkit.types import RdkitBitFingerprint, RdkitMol, RdkitSparseFingerprint
from molalchemy.types import CString


def equals(mol_column: ColumnElement[RdkitMol], query: str) -> BinaryExpression:
    """
    Perform exact molecular structure matching.

    Checks if the molecular structure in the column exactly matches
    the query molecule using the `@=` operator.

    Parameters
    ----------
    mol_column : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The database column containing the molecular structure to compare.
    query : str
        The query molecule as a string (SMILES, SMARTS, or other format).

    Returns
    -------
    BinaryExpression
        SQLAlchemy binary expression for the exact match comparison.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(Molecule).where(equals(Molecule.structure, "CCO"))
    """
    return mol_column.op("@=")(query)


def has_substructure(
    mol_column: ColumnElement[RdkitMol], query: str
) -> BinaryExpression:
    """
    Perform substructure search.

    Checks if the molecular structure in the column contains the query
    substructure using the `@>` operator.

    Parameters
    ----------
    mol_column : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The database column containing the molecular structure to search.
    query : str
        The query substructure as a string (SMILES, SMARTS, or other format).

    Returns
    -------
    BinaryExpression
        SQLAlchemy binary expression for the substructure search.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(Molecule).where(has_substructure(Molecule.structure, "C=O"))
    """
    return mol_column.op("@>")(query)


def to_binary(mol: ColumnElement[RdkitMol], **kwargs) -> Function[bytes]:
    """
    Convert a molecular structure to binary format.

    Serializes the molecular structure to a binary representation
    using the `mol_send` PostgreSQL function.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to convert.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[bytes]
        SQLAlchemy function that returns the binary representation.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(to_binary(Molecule.structure))
    """
    return func.mol_send(mol, **kwargs)


def to_smiles(mol: ColumnElement[RdkitMol], **kwargs) -> Function[str]:
    """
    Convert a molecular structure to SMILES format.

    Converts the molecular structure to SMILES (Simplified Molecular Input Line
    Entry System) format using the `mol_to_smiles` PostgreSQL function.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to convert.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[str]
        SQLAlchemy function that returns the SMILES representation.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(to_smiles(Molecule.structure))
    """
    return func.mol_to_smiles(mol, **kwargs)


def to_json(mol: ColumnElement[RdkitMol], **kwargs) -> Function[str]:
    """
    Convert a molecular structure to JSON format.

    Serializes the molecular structure to a JSON representation
    using the `mol_to_json` PostgreSQL function.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to convert.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[str]
        SQLAlchemy function that returns the JSON representation.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(to_json(Molecule.structure))
    """
    return func.mol_to_json(mol, **kwargs)


def to_cxsmiles(mol: ColumnElement[RdkitMol], **kwargs) -> Function[str]:
    """
    Convert a molecular structure to CXSMILES format.

    Converts the molecular structure to ChemAxon Extended SMILES (CXSMILES) format
    using the `mol_to_cxsmiles` PostgreSQL function.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to convert.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[str]
        SQLAlchemy function that returns the CXSMILES representation.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(to_cxsmiles(Molecule.structure))
    """
    return func.mol_to_cxsmiles(mol, **kwargs)


def to_smarts(mol: ColumnElement[RdkitMol], **kwargs) -> Function[str]:
    """
    Convert a molecular structure to SMARTS format.

    Converts the molecular structure to SMARTS (SMILES arbitrary target specification) format
    using the `mol_to_smarts` PostgreSQL function.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to convert.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[str]
        SQLAlchemy function that returns the SMARTS representation.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(to_smarts(Molecule.structure))
    """
    return func.mol_to_smarts(mol, **kwargs)


def to_pkl(mol: ColumnElement[RdkitMol], **kwargs) -> Function[bytes]:
    """
    Convert a molecular structure to pickle format.

    Serializes the molecular structure to a pickle (binary) format
    using the `mol_to_pkl` PostgreSQL function.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to convert.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[bytes]
        SQLAlchemy function that returns the pickle representation.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(to_pkl(Molecule.structure))
    """
    return func.mol_to_pkl(mol, **kwargs)


def from_smiles(smiles: ColumnElement[str], **kwargs) -> Function[RdkitMol]:
    """
    Parse a molecular structure from SMILES format.

    Converts a SMILES string to a molecular structure object
    using the `mol_from_smiles` PostgreSQL function.

    Parameters
    ----------
    smiles : ColumnElement[str]
        The SMILES string to parse.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[molalchemy.rdkit.types.RdkitMol]
        SQLAlchemy function that returns the parsed molecular structure.

    Examples
    --------
    >>> from sqlalchemy import select, literal
    >>> query = select(from_smiles(literal("CCO")))
    """
    return func.mol_from_smiles(cast(smiles, CString), **kwargs)


def from_pkl(pkl: ColumnElement[bytes], **kwargs) -> Function[RdkitMol]:
    """
    Parse a molecular structure from pickle format.

    Deserializes a molecular structure from a pickle (binary) representation
    using the `mol_from_pkl` PostgreSQL function.

    Parameters
    ----------
    pkl : ColumnElement[bytes]
        The pickle binary data to parse.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[molalchemy.rdkit.types.RdkitMol]
        SQLAlchemy function that returns the parsed molecular structure.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(from_pkl(Molecule.pickle_data))
    """
    return func.mol_from_pkl(pkl, **kwargs)


def maccs_fp(mol: ColumnElement[RdkitMol], **kwargs) -> Function[RdkitBitFingerprint]:
    """
    Generate MACCS fingerprint for a molecular structure.

    Computes the MACCS (Molecular ACCess System) keys fingerprint,
    a 166-bit structural key fingerprint using the `maccs_fp` PostgreSQL function.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to generate fingerprint for.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[molalchemy.rdkit.types.RdkitBitFingerprint]
        SQLAlchemy function that returns the MACCS fingerprint.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(maccs_fp(Molecule.structure))
    """
    return func.maccs_fp(mol, **kwargs)


def rdkit_fp(mol: ColumnElement[RdkitMol], **kwargs) -> Function[RdkitBitFingerprint]:
    """
    Generate RDKit fingerprint for a molecular structure.

    Computes the RDKit fingerprint, a topological fingerprint using the
    `rdkit_fp` PostgreSQL function.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to generate fingerprint for.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[molalchemy.rdkit.types.RdkitBitFingerprint]
        SQLAlchemy function that returns the RDKit fingerprint.
    """
    return func.rdkit_fp(mol, **kwargs)


def morgan_fp(
    mol: ColumnElement[RdkitMol], radius: int = 2, **kwargs
) -> Function[RdkitSparseFingerprint]:
    """
    Generate Morgan fingerprint for a molecular structure.

    Computes the Morgan (circular) fingerprint using the `morgan_fp` PostgreSQL function.
    This fingerprint encodes the molecular environment around each atom.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to generate fingerprint for.
    radius : int, default 2
        The radius for the Morgan fingerprint algorithm.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[molalchemy.rdkit.types.RdkitSparseFingerprint]
        SQLAlchemy function that returns the Morgan sparse fingerprint.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(morgan_fp(Molecule.structure, radius=3))
    """
    return func.morgan_fp(mol, radius, **kwargs)


def morganbv_fp(
    mol: ColumnElement[RdkitMol], radius: int = 2, **kwargs
) -> Function[RdkitBitFingerprint]:
    """
    Generate Morgan bit vector fingerprint for a molecular structure.

    Computes the Morgan (circular) fingerprint as a bit vector using the
    `morganbv_fp` PostgreSQL function. This is a fixed-length binary representation
    of the Morgan fingerprint.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to generate fingerprint for.
    radius : int, default 2
        The radius for the Morgan fingerprint algorithm.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[molalchemy.rdkit.types.RdkitBitFingerprint]
        SQLAlchemy function that returns the Morgan bit vector fingerprint.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(morganbv_fp(Molecule.structure, radius=3))
    """
    return func.morganbv_fp(mol, radius, **kwargs)


def torsion_fp(
    mol: ColumnElement[RdkitMol], **kwargs
) -> Function[RdkitSparseFingerprint]:
    """
    Generate torsion fingerprint for a molecular structure.

    Computes the topological torsion fingerprint using the `torsion_fp` PostgreSQL function.
    This fingerprint encodes four-atom torsion patterns in the molecule.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to generate fingerprint for.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[molalchemy.rdkit.types.RdkitSparseFingerprint]
        SQLAlchemy function that returns the torsion sparse fingerprint.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(torsion_fp(Molecule.structure))
    """
    return func.torsion_fp(mol, **kwargs)


def torsionbv_fp(
    mol: ColumnElement[RdkitMol], **kwargs
) -> Function[RdkitBitFingerprint]:
    """
    Generate torsion bit vector fingerprint for a molecular structure.

    Computes the topological torsion fingerprint as a bit vector using the
    `torsionbv_fp` PostgreSQL function. This is a fixed-length binary representation
    of the torsion fingerprint.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to generate fingerprint for.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[molalchemy.rdkit.types.RdkitBitFingerprint]
        SQLAlchemy function that returns the torsion bit vector fingerprint.
    """
    return func.torsionbv_fp(mol, **kwargs)


def mol_murckoscaffold(mol: ColumnElement[RdkitMol], **kwargs) -> Function[RdkitMol]:
    """
    Generate Murcko scaffold for a molecular structure.

    Computes the Murcko scaffold (framework) of the molecule using the
    `mol_murckoscaffold` PostgreSQL function. The scaffold represents the
    core structure without side chains.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to extract scaffold from.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[molalchemy.rdkit.types.RdkitMol]
        SQLAlchemy function that returns the Murcko scaffold structure.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(mol_murckoscaffold(Molecule.structure))
    """
    return func.mol_murckoscaffold(mol, **kwargs)


def mol_tpsa(mol: ColumnElement[RdkitMol], **kwargs) -> Function[float]:
    """
    Calculate topological polar surface area (TPSA) of a molecular structure.

    Computes the TPSA using the `mol_tpsa` PostgreSQL function. TPSA is
    a descriptor that correlates well with drug permeability and bioavailability.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to calculate TPSA for.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[float]
        SQLAlchemy function that returns the TPSA value in Ų.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(mol_tpsa(Molecule.structure))
    """
    return func.mol_tpsa(mol, **kwargs)


def mol_logp(mol: ColumnElement[RdkitMol], **kwargs) -> Function[float]:
    """
    Calculate logP (partition coefficient) of a molecular structure.

    Computes the logP using the `mol_logp` PostgreSQL function. LogP is
    a measure of lipophilicity, representing the logarithm of the partition
    coefficient between octanol and water.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to calculate logP for.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[float]
        SQLAlchemy function that returns the logP value.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(mol_logp(Molecule.structure))
    """
    return func.mol_logp(mol, **kwargs)


def mol_num_atoms(mol: ColumnElement[RdkitMol], **kwargs) -> Function[int]:
    """
    Count the number of atoms in a molecular structure.

    Counts the total number of atoms using the `mol_num_atoms` PostgreSQL function.
    This includes all atoms (heavy atoms and hydrogens).

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to count atoms for.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[int]
        SQLAlchemy function that returns the number of atoms.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(mol_num_atoms(Molecule.structure))
    """
    return func.mol_num_atoms(mol, **kwargs)


def mol_hba(mol: ColumnElement[RdkitMol], **kwargs) -> Function[int]:
    """
    Count hydrogen bond acceptors in a molecular structure.

    Counts the number of hydrogen bond acceptors using the `mol_hba` PostgreSQL function.
    Hydrogen bond acceptors are typically nitrogen and oxygen atoms with lone pairs.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to count hydrogen bond acceptors for.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[int]
        SQLAlchemy function that returns the number of hydrogen bond acceptors.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(mol_hba(Molecule.structure))
    """
    return func.mol_hba(mol, **kwargs)


def mol_hbd(mol: ColumnElement[RdkitMol], **kwargs) -> Function[int]:
    """
    Count hydrogen bond donors in a molecular structure.

    Counts the number of hydrogen bond donors using the `mol_hbd` PostgreSQL function.
    Hydrogen bond donors are typically nitrogen, oxygen, or sulfur atoms bonded to hydrogen.

    Parameters
    ----------
    mol : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The molecular structure to count hydrogen bond donors for.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[int]
        SQLAlchemy function that returns the number of hydrogen bond donors.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(mol_hbd(Molecule.structure))
    """
    return func.mol_hbd(mol, **kwargs)
