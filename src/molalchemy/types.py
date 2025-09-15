from sqlalchemy.types import UserDefinedType


class CString(UserDefinedType):
    """Custom type for C-style strings (null-terminated)."""

    impl = str
    cache_ok = True

    def get_col_spec(self):
        return "cstring"
