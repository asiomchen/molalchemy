"""
RDKit PostgreSQL functions for molecular and reaction operations.

This package provides static methods that wrap RDKit PostgreSQL functions for
performing chemical structure operations. It includes three main modules:

- `mol`: Molecular structure operations including search, conversion, fingerprinting,
  and property calculation
- `fp`: Fingerprint similarity and distance calculations for chemical similarity searching
- `rxn`: Chemical reaction operations including reaction search and format conversion

All functions return SQLAlchemy expressions that can be used directly in database
queries and are compatible with the RDKit PostgreSQL cartridge.

Any function not listed here can still be used via `func.<function_name>`.
"""

from sqlalchemy import func

from . import fp, mol, rxn

__all__ = ["fp", "mol", "rdkit_toolkit_version", "rdkit_version", "rxn"]


def rdkit_toolkit_version() -> str:
    """
    Get the version of the RDKit PostgreSQL cartridge.

    Returns
    -------
    str
        The version string of the RDKit PostgreSQL cartridge.
    """
    return func.rdkit_toolkit_version()


def rdkit_version() -> str:
    """
    Get the version of the RDKit library used by the PostgreSQL cartridge.

    Returns
    -------
    str
        The version string of the RDKit library.
    """
    return func.rdkit_version()
