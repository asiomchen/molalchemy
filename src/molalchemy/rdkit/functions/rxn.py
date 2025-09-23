"""
Collection of RDKit PostgreSQL functions for reaction structure search and analysis.

This module provides static methods that wrap RDKit PostgreSQL functions for performing
various chemical reaction operations including reaction substructure search, exact matching,
and format conversions.
"""

from sqlalchemy.sql import cast, func
from sqlalchemy.sql.elements import ClauseElement, ColumnElement
from sqlalchemy.sql.functions import Function

from molalchemy.rdkit.types import RdkitReaction
from molalchemy.types import CString


def has_smarts(rxn_column: ColumnElement, pattern: str) -> ColumnElement[bool]:
    """
    Perform reaction substructure search.

    Checks if the reaction in the column contains the query pattern
    using the `substruct` PostgreSQL function. This searches for
    reaction substructures within stored reactions.

    Parameters
    ----------
    rxn_column : ColumnElement
        The database column containing the reaction to search in.
    pattern : str
        The reaction SMARTS pattern to search for. Can represent
        partial reaction patterns or transformations.

    Returns
    -------
    ColumnElement[bool]
        SQLAlchemy column element that returns `True` if the pattern
        is found in the reaction, `False` otherwise.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> # Search for reactions containing a carbonyl formation
    >>> query = select(Reaction).where(has_smarts(Reaction.rxn, ">>C=O"))
    """
    return func.substruct(rxn_column, reaction_from_smarts(pattern))


def equals(rxn_column: ColumnElement, smarts_query: str) -> ColumnElement[bool]:
    """
    Perform exact reaction matching.

    Checks if the reaction in the column exactly matches the query
    reaction using the `reaction_eq` PostgreSQL function.

    Parameters
    ----------
    rxn_column : ColumnElement
        The database column containing the reaction to compare.
    smarts_query : str
        The reaction SMARTS string to match against. Must represent
        a complete reaction with reactants and products.

    Returns
    -------
    ColumnElement[bool]
        SQLAlchemy column element that returns `True` if the reactions
        are identical, `False` otherwise.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> # Find exact matches for a specific reaction
    >>> query = select(Reaction).where(equals(Reaction.rxn, "C.[Cl][Cl]>>C[Cl].[H][Cl]"))
    """
    return func.reaction_eq(rxn_column, reaction_from_smarts(smarts_query))


def reaction_from_smarts(smarts: ColumnElement[str]) -> Function[RdkitReaction]:
    """
    Parse a chemical reaction from SMARTS format.

    Converts a reaction SMARTS string to a reaction object using the
    `reaction_from_smarts` PostgreSQL function. Reaction SMARTS represents
    chemical transformations with reactants, products, and optional agents.

    Parameters
    ----------
    smarts : ColumnElement[str]
        The reaction SMARTS string to parse. Should follow the format
        `reactants>>products` or `reactants>agents>products`.

    Returns
    -------
    Function[RdkitReaction]
        SQLAlchemy function that returns the parsed reaction object.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> # Simple reaction: methane + chlorine -> methyl chloride + HCl
    >>> rxn = reaction_from_smarts("C.[Cl][Cl]>>C[Cl].[H][Cl]")
    >>> query = select(rxn)
    """
    return func.reaction_from_smarts(cast(smarts, CString))


def reaction_from_smiles(smiles: ColumnElement[str]) -> Function[RdkitReaction]:
    """
    Parse a chemical reaction from SMILES format.

    Converts a reaction SMILES string to a reaction object using the
    `reaction_from_smiles` PostgreSQL function. Reaction SMILES represents
    chemical transformations with reactants, products, and optional agents.

    Parameters
    ----------
    smiles : ColumnElement[str]
        The reaction SMILES string to parse. Should follow the format
        `reactants>>products` or `reactants>agents>products`.

    Returns
    -------
    Function[RdkitReaction]
        SQLAlchemy function that returns the parsed reaction object.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> # Simple reaction: methane + chlorine -> methyl chloride + HCl
    >>> rxn = reaction_from_smiles("C.[Cl][Cl]>>C[Cl].[H][Cl]")
    >>> query = select(rxn)
    """
    return func.reaction_from_smiles(cast(smiles, CString))


def reaction_to_smarts(rxn_column: ColumnElement[RdkitReaction]) -> ColumnElement[str]:
    """
    Convert a reaction to SMARTS format.

    Serializes the reaction to a SMARTS string using the
    `reaction_to_smarts` PostgreSQL function. This is useful for
    exporting or displaying the reaction in a human-readable format.

    Parameters
    ----------
    rxn_column : ColumnElement[RdkitReaction]
        The database column containing the reaction to convert.

    Returns
    -------
    ColumnElement[str]
        SQLAlchemy column element that returns the SMARTS representation
        of the reaction.
    """
    return func.reaction_to_smarts(rxn_column)


def reaction_to_smiles(rxn_column: ColumnElement[RdkitReaction]) -> ColumnElement[str]:
    """
    Convert a reaction to SMILES format.

    Serializes the reaction to a SMILES string using the
    `reaction_to_smiles` PostgreSQL function. This is useful for
    exporting or displaying the reaction in a compact text format.

    Parameters
    ----------
    rxn_column : ColumnElement[RdkitReaction]
        The database column containing the reaction to convert.

    Returns
    -------
    ColumnElement[str]
        SQLAlchemy column element that returns the SMILES representation
        of the reaction.
    """
    return func.reaction_to_smiles(rxn_column)


def to_binary(rxn_column: ColumnElement[RdkitReaction], **kwargs) -> ClauseElement:
    """
    Convert a reaction to binary format.

    Serializes the reaction to a binary representation using the
    `reaction_send` PostgreSQL function. This is useful for storage
    efficiency or network transmission.

    Parameters
    ----------
    rxn_column : ColumnElement[RdkitReaction]
        The database column containing the reaction to convert.
    **kwargs
        Additional keyword arguments passed to the PostgreSQL function.

    Returns
    -------
    ClauseElement
        SQLAlchemy clause element that returns the binary representation
        of the reaction.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(to_binary(Reaction.rxn))
    """
    return func.reaction_send(rxn_column, **kwargs)


def reaction_numproducts(
    rxn_column: ColumnElement[RdkitReaction],
) -> ColumnElement[int]:
    """
    Get the number of products in a reaction.

    Uses the `reaction_numproducts` PostgreSQL function to count
    the number of product molecules defined in the reaction.

    Parameters
    ----------
    rxn_column : ColumnElement[RdkitReaction]
        The database column containing the reaction to analyze.

    Returns
    -------
    ColumnElement[int]
        SQLAlchemy column element that returns the number of products
        in the reaction.
    """
    return func.reaction_numproducts(rxn_column)


def reaction_numreactants(
    rxn_column: ColumnElement[RdkitReaction],
) -> ColumnElement[int]:
    """
    Get the number of reactants in a reaction.

    Uses the `reaction_numreactants` PostgreSQL function to count
    the number of reactant molecules defined in the reaction.

    Parameters
    ----------
    rxn_column : ColumnElement[RdkitReaction]
        The database column containing the reaction to analyze.

    Returns
    -------
    ColumnElement[int]
        SQLAlchemy column element that returns the number of reactants
        in the reaction.
    """
    return func.reaction_numreactants(rxn_column)
