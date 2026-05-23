"""Shared Bingo search expression helpers."""

from typing import Any

from sqlalchemy import types as sqltypes
from sqlalchemy.sql import operators
from sqlalchemy.sql.elements import BinaryExpression, ColumnElement


class _BingoExactSearchExpression(BinaryExpression[bool]):
    inherit_cache = True

    def __bool__(self) -> bool:
        return self._orig[0] == self._orig[1]


class _BingoSearchType(sqltypes.UserDefinedType):
    """SQLAlchemy type wrapper for casting search tuples to Bingo search types."""

    cache_ok = True
    allowed_types = (
        "bingo.sub",
        "bingo.smarts",
        "bingo.exact",
        "bingo.sim",
        "bingo.rsub",
        "bingo.rsmarts",
        "bingo.rexact",
    )

    def __init__(self, type_name: str) -> None:
        if type_name not in self.allowed_types:
            raise ValueError(
                f"Invalid Bingo search type: {type_name}. Allowed types are: {self.allowed_types}"
            )
        self.type_name = type_name

    def get_col_spec(self, **kw: Any) -> str:
        return self.type_name


def _bingo_search(
    column: ColumnElement[Any],
    query_tuple: Any,
    search_type: str,
) -> ColumnElement[bool]:
    query = query_tuple.cast(_BingoSearchType(search_type))
    if search_type in ("bingo.exact", "bingo.rexact"):
        return _BingoExactSearchExpression(
            column,
            query,
            operators.custom_op("@", is_comparison=True),
            type_=sqltypes.Boolean(),
        )
    return column.op("@")(query)
