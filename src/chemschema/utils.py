from sqlalchemy.sql import ColumnElement
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.schema import Column
from typing import Union


def get_column_name(mol_column: Union[InstrumentedAttribute, Column, ColumnElement, str]) -> str:
        """Helper to get column name regardless of input type"""
        if hasattr(mol_column, 'table'):
            # Handle ORM attributes
            table_name = mol_column.table.name
            column_name = mol_column.name
            return f"{table_name}.{column_name}"
        elif hasattr(mol_column, 'name'):
             # Handle Table columns
            return mol_column.name
        return str(mol_column)