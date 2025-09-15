from sqlalchemy.sql import func, cast
from sqlalchemy.sql.elements import ClauseElement, ColumnElement
from molalchemy.types import CString


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
        return func.mol_from_smiles(cast(smiles, CString), **kwargs)

    @staticmethod
    def maccs_fp(mol: ColumnElement, **kwargs) -> ClauseElement:
        return func.maccs_fp(mol, **kwargs)

    @staticmethod
    def tanimoto(fp1: ColumnElement, fp2: ColumnElement) -> ClauseElement:
        return func.tanimoto_sml(fp1, fp2)


class rdkit_rxn_func:
    @staticmethod
    def reaction_from_smarts(smarts: str) -> ClauseElement:
        return func.reaction_from_smarts(cast(smarts, CString))

    @staticmethod
    def has_smarts(rxn_column: ColumnElement, pattern: str) -> ColumnElement[bool]:
        return func.substruct(rxn_column, rdkit_rxn_func.reaction_from_smarts(pattern))

    @staticmethod
    def equals(rxn_column: ColumnElement, smarts_query: str) -> ColumnElement[bool]:
        return func.reaction_eq(
            rxn_column, rdkit_rxn_func.reaction_from_smarts(smarts_query)
        )

    @staticmethod
    def to_binary(rxn_column: ColumnElement, **kwargs) -> ClauseElement:
        return func.reaction_send(rxn_column, **kwargs)
