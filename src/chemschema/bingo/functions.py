from chemschema.utils import get_column_name
from sqlalchemy import text


class bingo_func:
    @staticmethod
    def has_substructure(mol_column, query, parameters=""):
        return text(f"{mol_column} @ {query, parameters}::bingo.sub")

    @staticmethod
    def matches_smarts(mol_column, query, parameters=""):
        return text(f"{mol_column} @ {query, parameters}::bingo.smarts")

    @staticmethod
    def equals(mol_column, query, parameters=""):
        mol_column = get_column_name(mol_column)
        return text(f"{mol_column} @ {query, parameters}::bingo.exact")

    @staticmethod
    def similarity(mol_column, query, bottom=0.0, top=1.0, metric="Tanimoto"):
        # get table name if the columnis mapped
        mol_column = get_column_name(mol_column)
        return text(f"{mol_column} @ {bottom, top, query, metric}::bingo.sim")

    @staticmethod
    def has_gross_formula(mol_column, formula):
        mol_column = get_column_name(mol_column)
        return text(f"{mol_column} @ {formula}::bingo.gross")


class bingo_rxn_func:
    @staticmethod
    def equals(rxn_column, query, parameters=""):
        return text(f"{rxn_column} @ {query, parameters}::bingo.rexact")

    @staticmethod
    def has_reaction_smarts(rxn_column, query, parameters=""):
        return text(f"{rxn_column} @ {query, parameters}::bingo.rsmarts")

    @staticmethod
    def has_reaction_substructure(rxn_column, query, parameters=""):
        return text(f"{rxn_column} @ {query, parameters}::bingo.rsub")


class BingoMolProxy:
    @staticmethod
    def has_substructure(query, parameters=""):
        pass

    @staticmethod
    def matches_smarts(query, parameters=""):
        pass

    @staticmethod
    def equals(query, parameters=""):
        pass

    @staticmethod
    def similarity(query, bottom=0.0, top=1.0, metric="Tanimoto"):
        pass

    @staticmethod
    def has_gross_formula(formula):
        pass

    def __getattr__(self, item):
        if item in dir(bingo_func):
            return getattr(bingo_func, item)
        raise AttributeError(f"'BingoMolProxy' object has no attribute '{item}'")


class BingoRxnProxy:
    @staticmethod
    def has_reaction_substructure(query, parameters=""):
        pass

    @staticmethod
    def has_reaction_smarts(query, parameters=""):
        pass

    @staticmethod
    def equals(query, parameters=""):
        pass

    def __getattr__(self, item):
        if item in dir(bingo_rxn_func):
            return getattr(bingo_rxn_func, item)
        raise AttributeError(f"'BingoRxnProxy' object has no attribute '{item}'")
