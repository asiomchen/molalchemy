"""
Collection of RDKit PostgreSQL functions for fingerprint similarity and distance calculations.

This module provides static methods that wrap RDKit PostgreSQL functions for computing
similarity and distance metrics between molecular fingerprints. These functions are
essential for chemical similarity searching and clustering operations.
"""

from sqlalchemy import Function
from sqlalchemy.sql import func
from sqlalchemy.sql.elements import ColumnElement

from molalchemy.rdkit.types import RdkitBitFingerprint, RdkitSparseFingerprint

AnyRdkitFingerprint = RdkitBitFingerprint | RdkitSparseFingerprint


def tanimoto_sml(
    fp1: ColumnElement[AnyRdkitFingerprint],
    fp2: ColumnElement[AnyRdkitFingerprint],
    **kwargs,
) -> Function[float]:
    """
    Calculate Tanimoto similarity between two molecular fingerprints.

    Computes the Tanimoto coefficient (Jaccard index) between two fingerprints
    using the `tanimoto_sml` PostgreSQL function. The Tanimoto coefficient is
    the most widely used similarity metric in cheminformatics.

    Parameters
    ----------
    fp1 : ColumnElement[molalchemy.rdkit.types.RdkitBitFingerprint | molalchemy.rdkit.types.RdkitSparseFingerprint]
        The first fingerprint to compare.
    fp2 : ColumnElement[molalchemy.rdkit.types.RdkitBitFingerprint | molalchemy.rdkit.types.RdkitSparseFingerprint]
        The second fingerprint to compare.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[float]
        SQLAlchemy function that returns the Tanimoto similarity coefficient (0.0 to 1.0).

    Notes
    -----
    The Tanimoto coefficient is calculated as the ratio of the intersection
    to the union of the two fingerprints: T(A,B) = |A ∩ B| / |A ∪ B|.
    A value of 1.0 indicates identical fingerprints, while 0.0 indicates
    no common features.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(tanimoto_sml(mol1.morgan_fp, mol2.morgan_fp))
    """
    return func.tanimoto_sml(fp1, fp2, **kwargs)


def tanimoto_dist(
    fp1: ColumnElement[AnyRdkitFingerprint],
    fp2: ColumnElement[AnyRdkitFingerprint],
    **kwargs,
) -> Function[float]:
    """
    Calculate Tanimoto distance between two molecular fingerprints.

    Computes the Tanimoto distance between two fingerprints using the
    `tanimoto_dist` PostgreSQL function. The Tanimoto distance is the
    complement of the Tanimoto similarity coefficient.

    Parameters
    ----------
    fp1 : ColumnElement[molalchemy.rdkit.types.RdkitBitFingerprint | molalchemy.rdkit.types.RdkitSparseFingerprint]
        The first fingerprint to compare.
    fp2 : ColumnElement[molalchemy.rdkit.types.RdkitBitFingerprint | molalchemy.rdkit.types.RdkitSparseFingerprint]
        The second fingerprint to compare.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[float]
        SQLAlchemy function that returns the Tanimoto distance (0.0 to 1.0).

    Notes
    -----
    The Tanimoto distance is calculated as: D(A,B) = 1 - T(A,B), where
    T(A,B) is the Tanimoto similarity coefficient. A value of 0.0 indicates
    identical fingerprints, while 1.0 indicates maximum dissimilarity.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(tanimoto_dist(mol1.morgan_fp, mol2.morgan_fp))
    """
    return func.tanimoto_dist(fp1, fp2, **kwargs)


def tversky_sml(
    fp1: ColumnElement[AnyRdkitFingerprint],
    fp2: ColumnElement[AnyRdkitFingerprint],
    alpha: float = 0.5,
    beta: float = 0.5,
    **kwargs,
) -> Function[float]:
    """
    Calculate Tversky similarity between two molecular fingerprints.

    Computes the Tversky similarity coefficient between two fingerprints
    using the `tversky_sml` PostgreSQL function. The Tversky index is a
    generalization of the Jaccard index that allows for asymmetric comparisons.

    Parameters
    ----------
    fp1 : ColumnElement[molalchemy.rdkit.types.RdkitBitFingerprint | molalchemy.rdkit.types.RdkitSparseFingerprint]
        The first fingerprint to compare.
    fp2 : ColumnElement[molalchemy.rdkit.types.RdkitBitFingerprint | molalchemy.rdkit.types.RdkitSparseFingerprint]
        The second fingerprint to compare.
    alpha : float, default 0.5
        Weight for features in fp1 but not in fp2. Higher values favor fp1.
    beta : float, default 0.5
        Weight for features in fp2 but not in fp1. Higher values favor fp2.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    Function[float]
        SQLAlchemy function that returns the Tversky similarity coefficient (0.0 to 1.0).

    Notes
    -----
    The Tversky coefficient is calculated as:
    T(A,B) = |A ∩ B| / (|A ∩ B| + α|A - B| + β|B - A|)

    When α = β = 0.5, the Tversky coefficient equals the Tanimoto coefficient.
    When α = β = 1.0, it equals the Dice coefficient.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> # Standard Tversky similarity
    >>> query = select(tversky_sml(mol1.morgan_fp, mol2.morgan_fp))
    >>> # Asymmetric similarity favoring the first fingerprint
    >>> query = select(tversky_sml(mol1.morgan_fp, mol2.morgan_fp, alpha=0.8, beta=0.2))
    """
    return func.tversky_sml(fp1, fp2, alpha, beta, **kwargs)
