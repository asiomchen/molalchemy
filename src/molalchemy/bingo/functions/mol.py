"""
Collection of Bingo PostgreSQL functions for molecular structure search and analysis.

This class provides static methods that wrap Bingo PostgreSQL functions for performing
various chemical structure operations including substructure search, exact matching,
similarity search, and format conversions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from sqlalchemy import text
from sqlalchemy.sql import ColumnElement, func
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.functions import Function

if TYPE_CHECKING:
    from molalchemy.bingo.types import BingoBinaryMol

_WEIGHT_TYPES = Literal["molecular-weight", "most-abundant-mass", "monoisotopic"]


def has_substructure(mol_column: ColumnElement, query: str, parameters: str = ""):
    """
    Perform substructure search on a molecule column.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    query : str
        Query molecule as SMILES, SMARTS, or Molfile string.
    parameters : str, optional
        Search parameters for customizing the matching behavior (default is "").
        Examples: "TAU" for tautomer search, "RES" for resonance search.

    Returns
    -------
    BinaryExpression
        SQLAlchemy expression for substructure matching that can be used in WHERE clauses.

    """
    return mol_column.op("@")(text(f"('{query}', '{parameters}')::bingo.sub"))


def matches_smarts(mol_column: ColumnElement, query: str, parameters: str = ""):
    """
    Perform SMARTS pattern matching on a molecule column.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    query : str
        SMARTS pattern string for matching.
    parameters : str, optional
        Search parameters for customizing the matching behavior (default is "").

    Returns
    -------
    BinaryExpression
        SQLAlchemy expression for SMARTS matching that can be used in WHERE clauses.

    """
    return mol_column.op("@")(text(f"('{query}', '{parameters}')::bingo.smarts"))


def equals(mol_column: ColumnElement, query: str, parameters: str = ""):
    """
    Perform exact structure matching on a molecule column.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    query : str
        Query molecule as SMILES or Molfile string for exact matching.
    parameters : str, optional
        Search parameters for customizing the matching behavior (default is "").
        Examples: "TAU" for tautomer matching, "STE" for stereochemistry.

    Returns
    -------
    BinaryExpression
        SQLAlchemy expression for exact matching that can be used in WHERE clauses.

    """
    return mol_column.op("@")(text(f"('{query}', '{parameters}')::bingo.exact"))


def similarity(
    mol_column: ColumnElement,
    query: str,
    bottom: float = 0.0,
    top: float = 1.0,
    metric: str = "Tanimoto",
) -> BinaryExpression:
    """
    Perform similarity search on a molecule column. This should be used in WHERE clauses, as it
    returns a boolean expression indicating whether the similarity criteria are met.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    query : str
        Query molecule as SMILES or Molfile string for similarity comparison.
    bottom : float, optional
        Minimum similarity threshold (default is 0.0).
    top : float, optional
        Maximum similarity threshold (default is 1.0).
    metric : str, optional
        Similarity metric to use (default is "Tanimoto").
        Other options include "Dice", "Cosine", etc.

    Returns
    -------
    BinaryExpression
        SQLAlchemy expression for similarity matching that can be used in WHERE clauses.

    """
    return mol_column.op("%")(
        text(f"('{query}', {bottom}, {top}, '{metric}')::bingo.sim")
    )


def get_similarity(
    mol_column: ColumnElement,
    query: str,
    metric: str = "Tanimoto",
) -> Function[float]:
    """
    Calculate the similarity score between a molecule column and a query molecule.
    This function returns a float value representing the similarity score.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    query : str
        Query molecule as SMILES or Molfile string for similarity comparison.
    metric : str, optional
        Similarity metric to use (default is "Tanimoto").
        Other options include "Dice", "Cosine", etc.

    Returns
    -------
    Function[float]
        SQLAlchemy function expression returning the similarity score as a float.

    """
    return func.bingo.getsimilarity(mol_column, query, metric)


def has_gross_formula(mol_column: ColumnElement, formula: str):
    """
    Search for molecules with a specific gross formula.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    formula : str
        Gross formula string (e.g., "C6H6" for benzene).

    Returns
    -------
    BinaryExpression
        SQLAlchemy expression for gross formula matching that can be used in WHERE clauses.

    """
    return mol_column.op("@")(text(f"('{formula}')::bingo.gross"))


def get_weight(
    mol_column: ColumnElement, weight_type: _WEIGHT_TYPES = "molecular-weight"
):
    """
    Calculate molecular weight of molecules.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    weight_type : {"molecular-weight", "most-abundant-mass", "monoisotopic"}, optional
        Type of molecular weight to calculate (default is "molecular-weight").

    Returns
    -------
    Function[float]
        SQLAlchemy function expression returning the molecular weight.

    """
    return func.Bingo.getWeight(mol_column, weight_type)


def gross_formula(mol_column: ColumnElement) -> Function[str]:
    """
    Calculate the gross formula of molecules.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).

    Returns
    -------
    Function[str]
        SQLAlchemy function expression returning the gross formula as a string.

    """
    return func.Bingo.Gross(mol_column)


def check_molecule(mol_column: ColumnElement) -> Function[str | None]:
    """
    Check if molecules are valid and return error messages for invalid ones.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).

    Returns
    -------
    Function[str | None]
        SQLAlchemy function expression returning None for valid molecules,
        or an error message string for invalid molecules.

    """
    return func.Bingo.CheckMolecule(mol_column)


def to_canonical(mol_column: ColumnElement) -> Function[str]:
    """
    Convert molecules to canonical SMILES format.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).

    Returns
    -------
    Function[str]
        SQLAlchemy function expression returning canonical SMILES strings.

    """
    return func.Bingo.CanSMILES(mol_column)


def to_inchi(mol_column: ColumnElement) -> Function[str]:
    """
    Convert molecules to InChI format.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).

    Returns
    -------
    Function[str]
        SQLAlchemy function expression returning InChI strings.
    """
    return func.bingo.InChI(mol_column)


def to_inchikey(mol_column: ColumnElement) -> Function[str]:
    """
    Convert molecules to InChIKey format.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).

    Returns
    -------
    Function[str]
        SQLAlchemy function expression returning InChIKey strings.
    """
    return func.Bingo.InChIKey(mol_column)


def to_binary(
    mol_column: ColumnElement, preserve_pos: bool = True
) -> Function[BingoBinaryMol]:
    """
    Convert molecules to Bingo's internal binary format.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    preserve_pos : bool, optional
        Whether to preserve atom positions in the binary format (default is True).
        If False, only connectivity information is stored.

    Returns
    -------
    Function[bytes]
        SQLAlchemy function expression returning binary data.
    """
    return func.Bingo.CompactMolecule(mol_column, preserve_pos)


def to_smiles(mol_column: ColumnElement) -> Function[str]:
    """
    Convert molecules to SMILES format.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).

    Returns
    -------
    Function[str]
        SQLAlchemy function expression returning SMILES strings.

    """
    return func.Bingo.SMILES(mol_column)


def to_molfile(mol_column: ColumnElement) -> Function[str]:
    """
    Convert molecules to Molfile format.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).

    Returns
    -------
    Function[str]
        SQLAlchemy function expression returning Molfile strings with 2D coordinates.

    """
    return func.Bingo.Molfile(mol_column)


def to_cml(mol_column: ColumnElement) -> Function[str]:
    """
    Convert molecules to CML (Chemical Markup Language) format.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).

    Returns
    -------
    Function[str]
        SQLAlchemy function expression returning CML strings.

    """
    return func.Bingo.CML(mol_column)
