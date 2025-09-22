"""
Collection of Bingo PostgreSQL functions for reaction structure search and analysis.

This class provides static methods that wrap Bingo PostgreSQL functions for performing
various chemical reaction operations including reaction substructure search, exact matching,
and format conversions.
"""

from typing import Literal

from sqlalchemy import text
from sqlalchemy.sql import ColumnElement, func
from sqlalchemy.sql.functions import Function

_AAM_STRATEGIES = Literal["CLEAR", "DISCARD", "ALTER", "KEEP"]


def equals(rxn_column: ColumnElement, query: str, parameters: str = ""):
    """
    Perform exact reaction matching on a reaction column.

    Parameters
    ----------
    rxn_column : ColumnElement
        SQLAlchemy column containing reaction data (reaction SMILES, Rxnfile, or binary).
    query : str
        Query reaction as reaction SMILES or Rxnfile string for exact matching.
    parameters : str, optional
        Search parameters for customizing the matching behavior (default is "").

    Returns
    -------
    BinaryExpression
        SQLAlchemy expression for exact reaction matching that can be used in WHERE clauses.

    Examples
    --------
    >>> # Find exact matches for a specific reaction
    >>> session.query(ReactionTable).filter(
    ...     bingo_rxn_func.equals(ReactionTable.structure, "CCO>>CC=O")
    ... )
    """
    return rxn_column.op("@")(text(f"('{query}', '{parameters}')::bingo.rexact"))


def has_reaction_smarts(rxn_column: ColumnElement, query: str, parameters: str = ""):
    """
    Perform reaction SMARTS pattern matching on a reaction column.

    Parameters
    ----------
    rxn_column : ColumnElement
        SQLAlchemy column containing reaction data (reaction SMILES, Rxnfile, or binary).
    query : str
        Reaction SMARTS pattern string for matching.
    parameters : str, optional
        Search parameters for customizing the matching behavior (default is "").

    Returns
    -------
    BinaryExpression
        SQLAlchemy expression for reaction SMARTS matching that can be used in WHERE clauses.

    Examples
    --------
    >>> # Find reactions with carbonyl reduction pattern
    >>> session.query(ReactionTable).filter(
    ...     bingo_rxn_func.has_reaction_smarts(ReactionTable.structure, "[C]=[O]>>[C]-[O]")
    ... )
    """
    return rxn_column.op("@")(text(f"('{query}', '{parameters}')::bingo.rsmarts"))


def has_reaction_substructure(
    rxn_column: ColumnElement, query: str, parameters: str = ""
):
    """
    Perform reaction substructure search on a reaction column.

    Parameters
    ----------
    rxn_column : ColumnElement
        SQLAlchemy column containing reaction data (reaction SMILES, Rxnfile, or binary).
    query : str
        Query reaction as reaction SMILES or Rxnfile string for substructure matching.
    parameters : str, optional
        Search parameters for customizing the matching behavior (default is "").

    Returns
    -------
    BinaryExpression
        SQLAlchemy expression for reaction substructure matching that can be used in WHERE clauses.

    Examples
    --------
    >>> # Find reactions containing oxidation pattern
    >>> session.query(ReactionTable).filter(
    ...     bingo_rxn_func.has_reaction_substructure(ReactionTable.structure, "CO>>C=O")
    ... )
    """
    return rxn_column.op("@")(text(f"('{query}', '{parameters}')::bingo.rsub"))


def to_binary(rxn_column: ColumnElement, preserve_pos: bool = True) -> Function[bytes]:
    """
    Convert reactions to Bingo's internal binary format.

    Parameters
    ----------
    rxn_column : ColumnElement
        SQLAlchemy column containing reaction data (reaction SMILES, Rxnfile, or binary).
    preserve_pos : bool, optional
        Whether to preserve atom positions in the binary format (default is True).
        If False, only connectivity information is stored.

    Returns
    -------
    Function[bytes]
        SQLAlchemy function expression returning binary data.

    Examples
    --------
    >>> # Convert reactions to compact binary format
    >>> session.query(
    ...     ReactionTable.id,
    ...     bingo_rxn_func.to_binary(ReactionTable.structure)
    ... )
    """
    return func.Bingo.CompactReaction(rxn_column, preserve_pos)


def to_smiles(rxn_column: ColumnElement) -> Function[str]:
    """
    Convert reactions to reaction SMILES format.

    Parameters
    ----------
    rxn_column : ColumnElement
        SQLAlchemy column containing reaction data (reaction SMILES, Rxnfile, or binary).

    Returns
    -------
    Function[str]
        SQLAlchemy function expression returning reaction SMILES strings.

    Examples
    --------
    >>> # Get reaction SMILES for all reactions
    >>> session.query(
    ...     ReactionTable.id,
    ...     bingo_rxn_func.to_smiles(ReactionTable.structure)
    ... )
    """
    return func.Bingo.RSMILES(rxn_column)


def to_rxnfile(rxn_column: ColumnElement) -> Function[str]:
    """
    Convert reactions to Rxnfile format.

    Parameters
    ----------
    rxn_column : ColumnElement
        SQLAlchemy column containing reaction data (reaction SMILES, Rxnfile, or binary).

    Returns
    -------
    Function[str]
        SQLAlchemy function expression returning Rxnfile strings with 2D coordinates.

    Examples
    --------
    >>> # Get Rxnfile for all reactions
    >>> session.query(
    ...     ReactionTable.id,
    ...     bingo_rxn_func.to_rxnfile(ReactionTable.structure)
    ... )
    """
    return func.Bingo.Rxnfile(rxn_column)


def to_cml(rxn_column: ColumnElement) -> Function[str]:
    """
    Convert reactions to CML (Chemical Markup Language) format.

    Parameters
    ----------
    rxn_column : ColumnElement
        SQLAlchemy column containing reaction data (reaction SMILES, Rxnfile, or binary).

    Returns
    -------
    Function[str]
        SQLAlchemy function expression returning CML strings.

    Examples
    --------
    >>> # Get CML for all reactions
    >>> session.query(
    ...     ReactionTable.id,
    ...     bingo_rxn_func.to_cml(ReactionTable.structure)
    ... )
    """
    return func.Bingo.RCML(rxn_column)


def map_atoms(
    rxn_column: ColumnElement, strategy: _AAM_STRATEGIES = "KEEP"
) -> Function[str]:
    """
    Perform automatic atom-to-atom mapping (AAM) on reactions.

    Parameters
    ----------
    rxn_column : ColumnElement
        SQLAlchemy column containing reaction data (reaction SMILES, Rxnfile, or binary).
    strategy : {"CLEAR", "DISCARD", "ALTER", "KEEP"}, optional
        Strategy for handling existing atom mapping (default is "KEEP").
        - "CLEAR": Remove all existing mappings and compute new ones
        - "DISCARD": Remove all mappings without computing new ones
        - "ALTER": Modify existing mappings
        - "KEEP": Keep existing mappings and map unmapped atoms

    Returns
    -------
    Function[str]
        SQLAlchemy function expression returning reaction with atom mapping.

    Examples
    --------
    >>> # Add atom mapping to reactions
    >>> session.query(
    ...     ReactionTable.id,
    ...     bingo_rxn_func.map_atoms(ReactionTable.structure, "CLEAR")
    ... )
    """
    return func.Bingo.AAM(rxn_column, strategy)
