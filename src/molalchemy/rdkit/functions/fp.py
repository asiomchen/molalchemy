from sqlalchemy import Function
from sqlalchemy.sql import func
from sqlalchemy.sql.elements import ColumnElement


def tanimoto(fp1: ColumnElement, fp2: ColumnElement) -> Function[float]:
    return func.tanimoto_sml(fp1, fp2)
