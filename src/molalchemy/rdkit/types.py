from sqlalchemy.types import UserDefinedType
from molalchemy.rdkit.comparators import RdkitMolComparator, RdkitFPComparator
from . import functions as rdkit_func
from typing import Literal


class RdkitMol(UserDefinedType):
    impl = bytes
    cache_ok = True

    def get_col_spec(self):
        return "mol"

    comparator_factory = RdkitMolComparator

    def __init__(self, return_type: Literal["smiles", "bytes", "mol"] = "smiles"):
        super().__init__()
        self.return_type = return_type

    def column_expression(self, colexpr):
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
    impl = bytes
    cache_ok = True

    def get_col_spec(self):
        return "bfp"

    comparator_factory = RdkitFPComparator


class RdkitSparseFingerprint(UserDefinedType):
    impl = bytes
    cache_ok = True

    def get_col_spec(self):
        return "sfp"

    comparator_factory = RdkitFPComparator


class RdkitReaction(UserDefinedType):
    impl = bytes
    cache_ok = True

    def get_col_spec(self):
        return "reaction"

    comparator_factory = RdkitMolComparator

    def __init__(self, return_type: Literal["smiles", "bytes", "mol"] = "smiles"):
        super().__init__()
        self.return_type = return_type

    def column_expression(self, colexpr):
        # For mol return type, we want the binary representation
        if self.return_type == "mol":
            return rdkit_func.rxn.to_binary(colexpr, type_=self)
        elif self.return_type == "bytes":
            return rdkit_func.rxn.to_binary(colexpr, type_=self)
        else:  # smiles
            return colexpr

    def process_result_value(self, value, dialect):
        from rdkit import Chem

        del dialect
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
