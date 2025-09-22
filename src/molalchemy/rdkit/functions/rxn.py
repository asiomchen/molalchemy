"""
Collection of RDKit PostgreSQL functions for reaction structure search and analysis.

This module provides static methods that wrap RDKit PostgreSQL functions for performing
various chemical reaction operations including reaction substructure search, exact matching,
and format conversions.
"""

from sqlalchemy.sql import cast, func
from sqlalchemy.sql.elements import ClauseElement, ColumnElement

from molalchemy.types import CString


def reaction_from_smarts(smarts: str) -> ClauseElement:
    return func.reaction_from_smarts(cast(smarts, CString))


def has_smarts(rxn_column: ColumnElement, pattern: str) -> ColumnElement[bool]:
    return func.substruct(rxn_column, reaction_from_smarts(pattern))


def equals(rxn_column: ColumnElement, smarts_query: str) -> ColumnElement[bool]:
    return func.reaction_eq(rxn_column, reaction_from_smarts(smarts_query))


def to_binary(rxn_column: ColumnElement, **kwargs) -> ClauseElement:
    return func.reaction_send(rxn_column, **kwargs)
