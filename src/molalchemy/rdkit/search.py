"""Private RDKit search-expression builders."""

from typing import Any, cast

from sqlalchemy import Boolean, Float
from sqlalchemy.sql import cast as sql_cast
from sqlalchemy.sql import func
from sqlalchemy.sql.elements import ColumnElement

from molalchemy.types import CString


def _rdkit_predicate(
    column: ColumnElement[Any], operator: str, query: object
) -> ColumnElement[bool]:
    """Build a Boolean RDKit cartridge operator expression."""
    return cast(ColumnElement[bool], column.bool_op(operator)(query))


def _rdkit_distance(
    column: ColumnElement[Any], operator: str, query: object
) -> ColumnElement[float]:
    """Build a floating-point RDKit KNN distance expression."""
    return cast(ColumnElement[float], column.op(operator, return_type=Float())(query))


def _rdkit_mol_smarts(
    column: ColumnElement[Any], pattern: object
) -> ColumnElement[bool]:
    query = func.qmol_from_smarts(sql_cast(pattern, CString))
    return _rdkit_predicate(column, "@>", query)


def _rdkit_rxn_smarts(
    column: ColumnElement[Any], pattern: object
) -> ColumnElement[bool]:
    return cast(
        ColumnElement[bool],
        func.substruct(
            column,
            func.reaction_from_smarts(sql_cast(pattern, CString)),
            type_=Boolean(),
        ),
    )
