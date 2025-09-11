from sqlalchemy import text
from sqlalchemy.types import UserDefinedType



class BingoMolComparator(UserDefinedType.Comparator):
    def substructure(self, query, parameters=''):
        return self.expr.op('@')(text(f"('{query}', '{parameters}')::bingo.sub"))
    
    def smarts(self, query, parameters=''):
        return self.expr.op('@')(text(f"('{query}', '{parameters}')::bingo.smarts"))

    def equals(self, query, parameters=''):
        return self.expr.op('@')(text(f"('{query}', '{parameters}')::bingo.exact"))
