"""Shared Bingo search expression helpers."""

from typing import Any

from sqlalchemy import tuple_
from sqlalchemy import types as sqltypes
from sqlalchemy.sql import operators
from sqlalchemy.sql.elements import ColumnElement


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
    return column.operate(
        operators.custom_op(
            "@", precedence=5, is_comparison=True, return_type=sqltypes.Boolean()
        ),
        query,
    )


def _bingo_search_values(
    column: ColumnElement[Any], values: tuple[object, ...], search_type: str
) -> ColumnElement[bool]:
    """Build a Bingo predicate using SQLAlchemy's expression coercion.

    ``tuple_`` binds scalar values while honoring ``__clause_element__`` on ORM
    attributes and other SQL expression objects.
    """
    return _bingo_search(
        column,
        tuple_(*values),  # ty: ignore[invalid-argument-type]
        search_type,
    )
