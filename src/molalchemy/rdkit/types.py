"""SQLAlchemy types for RDKit PostgreSQL cartridge.

This module provides SQLAlchemy UserDefinedType implementations for working with
chemical data stored in PostgreSQL using the RDKit cartridge.
"""

import functools
from typing import Literal

from rdkit import Chem
from sqlalchemy import func
from sqlalchemy.types import UserDefinedType

from molalchemy.rdkit.comparators import RdkitFPComparator, RdkitMolComparator


class RdkitBaseType(UserDefinedType):
    """Base class for RDKit types."""


class RdkitMol(RdkitBaseType):
    """SQLAlchemy type for RDKit molecule data stored in PostgreSQL.

    This type maps to the PostgreSQL `mol` type provided by the RDKit cartridge.
    By default, SMILES strings are used as input, but `Chem.Mol` objects can also be used, all inputs are converted to binary format prior to sending to the database.
    It supports different return formats for flexibility in working with molecular data.

    Parameters
    ----------
    return_type : Literal["smiles", "bytes", "mol"], default "smiles"
        The format in which to return molecule data from the database:
        - `"smiles"`: Return as SMILES string
        - `"bytes"`: Return as raw bytes
        - `"mol"`: Return as `rdkit.Chem.Mol` object
    """

    cache_ok = True

    def get_col_spec(self):
        return "mol"

    comparator_factory = RdkitMolComparator

    def __init__(self, return_type: Literal["smiles", "bytes", "mol"] = "smiles"):
        super().__init__()
        self.return_type = return_type

    def column_expression(self, colexpr):
        from . import functions as rdkit_func

        # For mol return type, we want the binary representation
        if self.return_type == "mol":
            return rdkit_func.mol_send(colexpr, type_=self)
        elif self.return_type == "bytes":
            return rdkit_func.mol_send(colexpr, type_=self)
        else:  # smiles
            return colexpr

    def bind_processor(self, dialect):
        del dialect

        def process(value):
            if value is None:
                return None
            if isinstance(value, str):
                value = Chem.MolFromSmiles(value)
            if not isinstance(value, Chem.Mol):
                raise ValueError("Value must be a SMILES string or an RDKit Mol object")
            return value.ToBinary()

        return process

    def bind_expression(self, bindvalue):
        return func.mol_from_pkl(bindvalue)

    def result_processor(self, dialect, coltype):
        del dialect, coltype

        def process(value, return_type):
            if value is None:
                return None
            if return_type == "mol":
                # If we have bytes from mol_send, create molecule from binary
                if isinstance(value, bytes | memoryview):
                    return Chem.Mol(bytes(value))
                # If we have a string (shouldn't happen with mol_send but just in case)
                else:
                    return Chem.MolFromSmiles(str(value))
            elif return_type == "bytes":
                return bytes(value) if isinstance(value, memoryview) else value
            else:  # smiles
                return str(value)

        return functools.partial(process, return_type=self.return_type)


class RdkitBitFingerprint(RdkitBaseType):
    """SQLAlchemy type for RDKit bit fingerprint data stored in PostgreSQL.

    This type maps to the PostgreSQL `bfp` type provided by the RDKit cartridge,
    which represents binary fingerprints as bit strings.
    """

    impl = bytes
    cache_ok = True
    comparator_factory = RdkitFPComparator

    def get_col_spec(self):
        return "bfp"


class RdkitSparseFingerprint(RdkitBaseType):
    """SQLAlchemy type for RDKit sparse fingerprint data stored in PostgreSQL.

    This type maps to the PostgreSQL `sfp` type provided by the RDKit cartridge,
    which represents sparse fingerprints that store only the positions of set bits.
    """

    impl = bytes
    cache_ok = True
    comparator_factory = RdkitFPComparator

    def get_col_spec(self):
        return "sfp"


class RdkitReaction(RdkitBaseType):
    """SQLAlchemy type for RDKit chemical reaction data stored in PostgreSQL.

    This type maps to the PostgreSQL `reaction` type provided by the RDKit cartridge.
    It supports different return formats for flexibility in working with reaction data.

    Parameters
    ----------
    return_type : Literal["smiles", "bytes", "mol"], default "smiles"
        The format in which to return reaction data from the database:
        - `"smiles"`: Return as reaction SMILES string
        - `"bytes"`: Return as raw bytes
        - `"mol"`: Return as `AllChem.ChemicalReaction` object
    """

    impl = bytes
    cache_ok = True

    def get_col_spec(self):
        return "reaction"

    comparator_factory = RdkitMolComparator

    def __init__(self, return_type: Literal["smiles", "bytes", "mol"] = "smiles"):
        """Initialize the RdkitReaction type.

        Parameters
        ----------
        return_type : Literal["smiles", "bytes", "mol"], default "smiles"
            The format in which to return reaction data from the database.
        """
        super().__init__()
        self.return_type = return_type

    def column_expression(self, colexpr):
        from . import functions as rdkit_func

        if self.return_type == "mol":
            return rdkit_func.rxn.to_binary(colexpr, type_=self)
        elif self.return_type == "bytes":
            return rdkit_func.rxn.to_binary(colexpr, type_=self)
        else:  # smiles
            return colexpr

    def result_processor(self, dialect, coltype):
        del dialect, coltype

        def process(value, return_type):
            from rdkit.Chem import AllChem

            if value is None:
                return None
            if return_type == "mol":
                # If we have bytes from rxn_send, create reaction from binary
                if isinstance(value, bytes | memoryview):
                    return AllChem.ChemicalReaction(bytes(value))
            elif return_type == "bytes":
                return bytes(value) if isinstance(value, memoryview) else value
            else:  # smiles
                return str(value)

        return functools.partial(process, return_type=self.return_type)


class RdkitQMol(RdkitBaseType):
    def get_col_spec(self):
        return "qmol"


class RdkitXQMol(RdkitBaseType):
    def get_col_spec(self):
        return "xqmol"
