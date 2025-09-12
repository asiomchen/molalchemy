"""Bingo PostgreSQL types for chemical structures.

This module provides SQLAlchemy UserDefinedType classes for working with
chemical molecules and reactions in PostgreSQL using the Bingo cartridge.
"""

from sqlalchemy.types import UserDefinedType
from chemschema.bingo.comparators import BingoMolComparator, BingoRxnComparator
from .functions import bingo_func
from typing import Literal


class BingoMol(UserDefinedType):
    """SQLAlchemy type for molecule data stored as text (varchar).

    This type represents molecules stored as text in PostgreSQL, typically
    as SMILES strings or Molfiles. It uses varchar as the underlying storage
    type and provides molecular comparison capabilities through BingoMolComparator.

    Attributes
    ----------
    cache_ok : bool
        Indicates that this type can be safely cached.
    comparator_factory : type
        Factory class for creating molecular comparators.
    """

    cache_ok = True
    comparator_factory = BingoMolComparator

    def get_col_spec(self):
        """Get the column specification for this type.

        Returns
        -------
        str
            The PostgreSQL column type specification ("varchar").
        """
        return "varchar"


class BingoBinaryMol(UserDefinedType):
    """SQLAlchemy type for binary molecule data with format conversion.

    This type represents molecules stored in Bingo's internal binary format
    in PostgreSQL. It provides automatic conversion between various molecular
    formats and the binary storage format, with options for preserving
    atomic coordinates and specifying the return format for queries.

    Attributes
    ----------
    cache_ok : bool
        Indicates that this type can be safely cached.
    comparator_factory : type
        Factory class for creating molecular comparators.
    preserve_pos : bool
        Whether to preserve atomic coordinates in the binary format.
    return_type : str
        Format for returning data from the database.
    """

    cache_ok = True
    comparator_factory = BingoMolComparator

    def __init__(
        self,
        preserve_pos: bool = False,
        return_type: Literal["smiles", "molfile", "cml", "bytes"] = "smiles",
    ):
        """Initialize the BingoBinaryMol type.

        Parameters
        ----------
        preserve_pos : bool, default False
            Whether to preserve atomic coordinates when converting to binary format.
            If `True`, coordinates are stored; if `False`, they are discarded.
        return_type : {"smiles", "molfile", "cml", "bytes"}, default `"smiles"`
            The format to return when reading data from the database:
            - "smiles": Return as SMILES string
            - "molfile": Return as MDL Molfile format
            - "cml": Return as Chemical Markup Language format
            - "bytes": Return raw binary data
        """
        self.preserve_pos = preserve_pos
        self.return_type = return_type
        super().__init__()

    def get_col_spec(self):
        """Get the column specification for this type.

        Returns
        -------
        str
            The PostgreSQL column type specification ("bytea").
        """
        return "bytea"

    def bind_expression(self, bindvalue):
        """Convert input value to binary format for database storage.

        Parameters
        ----------
        bindvalue : Any
            The input value to be converted (typically a SMILES string or Molfile).

        Returns
        -------
        Any
            SQL expression that converts the input to Bingo binary format.
        """
        return bingo_func.to_binary(bindvalue, self.preserve_pos)

    def column_expression(self, col):
        """Convert binary column data to the specified return format.

        Parameters
        ----------
        col : Any
            The database column containing binary molecular data.

        Returns
        -------
        Any
            SQL expression that converts the binary data to the specified format.

        Raises
        ------
        ValueError
            If return_type is not one of the supported formats.
        """
        if self.return_type == "smiles":
            return bingo_func.to_smiles(col)
        elif self.return_type == "molfile":
            return bingo_func.to_molfile(col)
        elif self.return_type == "cml":
            return bingo_func.to_cml(col)
        elif self.return_type == "bytes":
            return col
        else:
            raise ValueError(
                f"Invalid return_type: {self.return_type}. Available options are 'smiles', 'molfile', 'cml', 'bytes'."
            )


class BingoReaction(UserDefinedType):
    """SQLAlchemy type for chemical reaction data stored as text (varchar).

    This type represents chemical reactions stored as text in PostgreSQL,
    typically as reaction SMILES or Rxnfiles. It uses varchar as the underlying
    storage type and provides reaction comparison capabilities through
    BingoRxnComparator.

    Attributes
    ----------
    cache_ok : bool
        Indicates that this type can be safely cached.
    comparator_factory : type
        Factory class for creating reaction comparators.
    """

    cache_ok = True
    comparator_factory = BingoRxnComparator

    def get_col_spec(self):
        return "varchar"


class BingoBinaryReaction(UserDefinedType):
    """SQLAlchemy type for binary chemical reaction data.

    This type represents chemical reactions stored in Bingo's internal binary
    format in PostgreSQL. It provides storage efficiency and fast comparison
    operations for reaction data.

    Attributes
    ----------
    cache_ok : bool
        Indicates that this type can be safely cached.
    comparator_factory : type
        Factory class for creating reaction comparators.
    """

    cache_ok = True
    comparator_factory = BingoRxnComparator

    def get_col_spec(self):
        return "bytea"
