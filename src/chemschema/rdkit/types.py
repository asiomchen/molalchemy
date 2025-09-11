from sqlalchemy.types import UserDefinedType

class Mol(UserDefinedType):
    def get_col_spec(self):
        return "mol"