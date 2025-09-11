from chemschema.utils import get_column_name
from sqlalchemy import text
class bingo_func:
    name = 'bingo'
    mol_type_name = 'bingo.molecule'
    fingerprint_type_name = 'bingo.fingerprint'
    @staticmethod
    def substructure(mol_column, query, parameters=''):
        return text(f"{mol_column} @ {query, parameters}::bingo.sub")
    @staticmethod
    def smarts(mol_column, query, parameters=''):
        return text(f"{mol_column} @ {query, parameters}::bingo.smarts")
    @staticmethod
    def equals(mol_column, query, parameters=''):
        mol_column = get_column_name(mol_column)
        return text(f"{mol_column} @ {query, parameters}::bingo.exact")
    @staticmethod
    def similarity(mol_column, query, bottom=0.0, top=1.0, metric='Tanimoto'):
        # get table name if the columnis mapped
        mol_column = get_column_name(mol_column)
        return text(f"{mol_column} @ {bottom, top, query, metric}::bingo.sim")