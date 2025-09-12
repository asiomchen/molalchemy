from sqlalchemy import text
from sqlalchemy.sql import ColumnElement
from sqlalchemy.sql import func
from sqlalchemy.sql.functions import Function
from typing import Literal

_WEIGHT_TYPES = Literal["molecular-weight", "most-abundant-mass", "monoisotopic"]
_AAM_STRATEGIES = Literal["CLEAR", "DISCARD", "ALTER", "KEEP"]


class bingo_func:
    @staticmethod
    def has_substructure(mol_column: ColumnElement, query: str, parameters: str = ""):
        return mol_column.op("@")(text(f"('{query}', '{parameters}')::bingo.sub"))

    @staticmethod
    def matches_smarts(mol_column: ColumnElement, query: str, parameters: str = ""):
        return mol_column.op("@")(text(f"('{query}', '{parameters}')::bingo.smarts"))

    @staticmethod
    def equals(mol_column: ColumnElement, query: str, parameters: str = ""):
        return mol_column.op("@")(text(f"('{query}', '{parameters}')::bingo.exact"))

    @staticmethod
    def similarity(
        mol_column: ColumnElement,
        query: str,
        bottom: float = 0.0,
        top: float = 1.0,
        metric: str = "Tanimoto",
    ):
        return mol_column.op("%")(
            text(f"('{query}', {bottom}, {top}, '{metric}')::bingo.sim")
        )

    @staticmethod
    def has_gross_formula(mol_column: ColumnElement, formula: str):
        return mol_column.op("@")(text(f"('{formula}')::bingo.gross"))

    @staticmethod
    def get_weight(
        mol_column: ColumnElement, weight_type: _WEIGHT_TYPES = "molecular-weight"
    ):
        return func.Bingo.getMass(mol_column)

    @staticmethod
    def gross_formula(mol_column: ColumnElement) -> Function[str]:
        return func.Bingo.Gross(mol_column)

    @staticmethod
    def check_molecule(mol_column: ColumnElement) -> Function[str | None]:
        return func.Bingo.CheckMolecule(mol_column)

    @staticmethod
    def to_canonical(mol_column: ColumnElement) -> Function[str]:
        return func.Bingo.CanSMILES(mol_column)

    @staticmethod
    def to_inchi(mol_column: ColumnElement) -> Function[str]:
        return func.bingo.InChI(mol_column)

    @staticmethod
    def to_inchikey(mol_column: ColumnElement) -> Function[str]:
        return func.Bingo.InChIKey(mol_column)

    @staticmethod
    def to_binary(
        mol_column: ColumnElement, preserve_pos: bool = True
    ) -> Function[bytes]:
        return func.Bingo.CompactMolecule(mol_column, int(preserve_pos))


class bingo_rxn_func:
    @staticmethod
    def equals(rxn_column: ColumnElement, query: str, parameters: str = ""):
        return rxn_column.op("@")(text(f"('{query}', '{parameters}')::bingo.rexact"))

    @staticmethod
    def has_reaction_smarts(
        rxn_column: ColumnElement, query: str, parameters: str = ""
    ):
        return rxn_column.op("@")(text(f"('{query}', '{parameters}')::bingo.rsmarts"))

    @staticmethod
    def has_reaction_substructure(
        rxn_column: ColumnElement, query: str, parameters: str = ""
    ):
        return rxn_column.op("@")(text(f"('{query}', '{parameters}')::bingo.rsub"))

    @staticmethod
    def to_binary(
        rxn_column: ColumnElement, preserve_pos: bool = True
    ) -> Function[bytes]:
        return func.Bingo.CompactReaction(rxn_column, int(preserve_pos))

    @staticmethod
    def to_smiles(rxn_column: ColumnElement) -> Function[str]:
        return func.Bingo.RSMILES(rxn_column)

    @staticmethod
    def to_rxnfile(rxn_column: ColumnElement) -> Function[str]:
        return func.Bingo.Rxnfile(rxn_column)

    @staticmethod
    def to_cml(rxn_column: ColumnElement) -> Function[str]:
        return func.Bingo.RCML(rxn_column)

    @staticmethod
    def map_atoms(
        rxn_column: ColumnElement, strategy: _AAM_STRATEGIES = "KEEP"
    ) -> Function[str]:
        return func.Bingo.AAM(rxn_column, strategy)
