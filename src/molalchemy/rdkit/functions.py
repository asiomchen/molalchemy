from sqlalchemy.sql import func, cast
from sqlalchemy.sql.elements import ClauseElement, ColumnElement


class rdkit_func:
    @staticmethod
    def equals(mol_column: ColumnElement, query: str) -> ClauseElement:
        return mol_column.op("@=")(query)

    @staticmethod
    def has_substructure(mol_column: ColumnElement, query: str) -> ClauseElement:
        return mol_column.op("@>")(query)

    @staticmethod
    def to_binary(mol: ColumnElement, **kwargs) -> ClauseElement:
        return func.mol_send(mol, **kwargs)

    @staticmethod
    def mol_from_smiles(smiles: str, **kwargs) -> ClauseElement:
        # Import CString here to avoid circular import
        from .types import CString

        return func.mol_from_smiles(cast(smiles, CString), **kwargs)

    @staticmethod
    def maccs_fp(mol: ColumnElement, **kwargs) -> ClauseElement:
        return func.maccs_fp(mol, **kwargs)

    @staticmethod
    def tanimoto(fp1: ColumnElement, fp2: ColumnElement) -> ClauseElement:
        return func.tanimoto_sml(fp1, fp2)
