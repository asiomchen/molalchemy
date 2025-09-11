from sqlalchemy.schema import Index
 
# @compiles(BingoMolIndex, 'postgresql')
# def compile_bingo_rxn_index(element, compiler, **kw):
#     expr = list(element.expressions)[0]
#     print(expr)
#     return "CREATE INDEX %s ON %s USING bingo_idx (%s bingo.reaction)" % (
#         element.name,
#         compiler.preparer.format_table(expr.table),
#         compiler.process(expr, include_table=False)
#     )
class BingoMolIndex(Index):
    def __init__(self, name, mol_column):
        super().__init__(name, mol_column, postgresql_using='bingo_idx', 
                         postgresql_ops={mol_column: 'bingo.molecule'})
class BingoBinaryMolIndex(Index):
    def __init__(self, name, mol_column):
        super().__init__(name, mol_column, postgresql_using='bingo_idx', 
                         postgresql_ops={mol_column: 'bingo.bmolecule'})