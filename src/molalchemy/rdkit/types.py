"""SQLAlchemy types for RDKit PostgreSQL cartridge.

This module provides SQLAlchemy UserDefinedType implementations for working with
chemical data stored in PostgreSQL using the RDKit cartridge.
"""

from sqlalchemy.types import UserDefinedType
from molalchemy.rdkit.comparators import RdkitMolComparator, RdkitFPComparator
from typing import Literal


class RdkitMol(UserDefinedType):
    """SQLAlchemy type for RDKit molecule data stored in PostgreSQL.

    This type maps to the PostgreSQL `mol` type provided by the RDKit cartridge.
    It supports different return formats for flexibility in working with molecular data.

    Parameters
    ----------
    return_type : Literal["smiles", "bytes", "mol"], default "smiles"
        The format in which to return molecule data from the database:
        - `"smiles"`: Return as SMILES string
        - `"bytes"`: Return as raw bytes
        - `"mol"`: Return as `rdkit.Chem.Mol` object (currently not functional)
    """

    impl = bytes
    cache_ok = True

    def get_col_spec(self):
        return "mol"

    comparator_factory = RdkitMolComparator

    def __init__(self, return_type: Literal["smiles", "bytes", "mol"] = "smiles"):
        """Initialize the RdkitMol type.

        Parameters
        ----------
        return_type : Literal["smiles", "bytes", "mol"], default "smiles"
            The format in which to return molecule data from the database.
        """
        super().__init__()
        self.return_type = return_type

    def column_expression(self, colexpr):
        from . import functions as rdkit_func

        # For mol return type, we want the binary representation
        if self.return_type == "mol":
            return rdkit_func.mol.to_binary(colexpr, type_=self)
        elif self.return_type == "bytes":
            return rdkit_func.mol.to_binary(colexpr, type_=self)
        else:  # smiles
            return colexpr

    # for some reason process_result_value is not called, even after setting the type in to_binary
    # will need to debug this later to allow return_type='mol' to work
    def process_result_value(self, value, dialect):
        from rdkit import Chem

        del dialect
        print(f"Processing value: {value} of type {type(value)}")
        if value is None:
            return None
        if self.return_type == "mol":
            # If we have bytes from mol_send, create molecule from binary
            if isinstance(value, (bytes, memoryview)):
                return Chem.Mol(bytes(value))
            # If we have a string (shouldn't happen with mol_send but just in case)
            else:
                return Chem.MolFromSmiles(str(value))
        elif self.return_type == "bytes":
            return bytes(value) if isinstance(value, memoryview) else value
        else:  # smiles
            return str(value)


class RdkitBitFingerprint(UserDefinedType):
    """SQLAlchemy type for RDKit bit fingerprint data stored in PostgreSQL.

    This type maps to the PostgreSQL `bfp` type provided by the RDKit cartridge,
    which represents binary fingerprints as bit strings.
    """

    impl = bytes
    cache_ok = True
    comparator_factory = RdkitFPComparator

    def get_col_spec(self):
        return "bfp"


class RdkitSparseFingerprint(UserDefinedType):
    """SQLAlchemy type for RDKit sparse fingerprint data stored in PostgreSQL.

    This type maps to the PostgreSQL `sfp` type provided by the RDKit cartridge,
    which represents sparse fingerprints that store only the positions of set bits.
    """

    impl = bytes
    cache_ok = True
    comparator_factory = RdkitFPComparator

    def get_col_spec(self):
        return "sfp"


class RdkitReaction(UserDefinedType):
    """SQLAlchemy type for RDKit chemical reaction data stored in PostgreSQL.

    This type maps to the PostgreSQL `reaction` type provided by the RDKit cartridge.
    It supports different return formats for flexibility in working with reaction data.

    Parameters
    ----------
    return_type : Literal["smiles", "bytes", "mol"], default "smiles"
        The format in which to return reaction data from the database:
        - `"smiles"`: Return as reaction SMILES string
        - `"bytes"`: Return as raw bytes
        - `"mol"`: Return as `AllChem.ChemicalReaction` object (currently not functional)
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

        # For mol return type, we want the binary representation
        if self.return_type == "mol":
            return rdkit_func.rxn.to_binary(colexpr, type_=self)
        elif self.return_type == "bytes":
            return rdkit_func.rxn.to_binary(colexpr, type_=self)
        else:  # smiles
            return colexpr

    def process_result_value(self, value, dialect):
        from rdkit.Chem import AllChem

        del dialect
        if value is None:
            return None
        if self.return_type == "mol":
            # If we have bytes from mol_send, create molecule from binary
            if isinstance(value, (bytes, memoryview)):
                return AllChem.ChemicalReaction(bytes(value))
        elif self.return_type == "bytes":
            return bytes(value) if isinstance(value, memoryview) else value
        else:  # smiles
            return str(value)
