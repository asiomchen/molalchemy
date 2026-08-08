"""Private RDKit search-expression builders."""

from typing import Any, cast

from sqlalchemy import Boolean, Float
from sqlalchemy.sql import cast as sql_cast
from sqlalchemy.sql import func
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.expression import type_coerce

from molalchemy.protocols import (
    RdkitFingerprintOperand,
    RdkitSimilarityBound,
    RdkitSimilarityMetric,
    SqlOperand,
)
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


def _rdkit_similarity_score(
    column: SqlOperand,
    query: RdkitFingerprintOperand,
    metric: RdkitSimilarityMetric,
) -> ColumnElement[float]:
    """Build a metric-specific floating-point fingerprint similarity score."""
    if metric == "Tanimoto":
        function = func.tanimoto_sml
    elif metric == "Dice":
        function = func.dice_sml
    else:
        raise ValueError(f"Unsupported RDKit similarity metric: {metric}")
    return cast(ColumnElement[float], function(column, query, type_=Float()))


def _rdkit_similar_to(
    column: SqlOperand,
    query: RdkitFingerprintOperand,
    minimum: RdkitSimilarityBound,
    maximum: RdkitSimilarityBound,
    metric: RdkitSimilarityMetric,
) -> ColumnElement[bool]:
    """Build an explicit bounded similarity predicate from a score expression."""
    score = _rdkit_similarity_score(column, query, metric)
    if minimum is not None and maximum is not None:
        return type_coerce(score.between(minimum, maximum), Boolean())
    if minimum is not None:
        return score >= minimum
    if maximum is not None:
        return score <= maximum
    return cast(ColumnElement[bool], score.is_not(None))


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
