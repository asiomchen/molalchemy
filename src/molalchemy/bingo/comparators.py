"""Bingo SQLAlchemy comparators for chemical structure searching."""

from typing import Any

from sqlalchemy import ColumnElement, tuple_
from sqlalchemy.types import UserDefinedType

from molalchemy.bingo.search import _bingo_search as _build_bingo_search


def _bingo_search(
    column: ColumnElement[Any], query: Any, parameters: Any, search_type: str
) -> ColumnElement[bool]:
    return _build_bingo_search(column, tuple_(query, parameters), search_type)


class BingoMolComparator(UserDefinedType.Comparator):
    """
    Comparator class for molecular structure operations using Bingo database.

    This class provides methods for chemical structure searching including
    substructure matching, SMARTS pattern matching, and exact structure matching.
    """

    def __eq__(self, other: Any) -> ColumnElement[bool]:
        if isinstance(other, ColumnElement) and not getattr(
            other, "is_clause_element", False
        ):
            return super().__eq__(other)
        if (
            isinstance(other, ColumnElement)
            and getattr(other, "table", None) is not None
        ):
            return super().__eq__(other)
        return self.equals(other)

    def __ne__(self, other: Any) -> ColumnElement[bool]:
        if isinstance(other, ColumnElement) and not getattr(
            other, "is_clause_element", False
        ):
            return super().__ne__(other)
        if (
            isinstance(other, ColumnElement)
            and getattr(other, "table", None) is not None
        ):
            return super().__ne__(other)
        return self.not_equals(other)

    def has_substructure(self, query: Any, parameters: Any = "") -> ColumnElement[bool]:
        """
        Check if the molecular structure contains a given substructure.

        Parameters
        ----------
        query : Any
            The substructure query as a SMILES or MOL string.
        parameters : Any, optional
            Additional parameters for the substructure search, by default "".

        Returns
        -------
        ColumnElement[bool]
            A SQLAlchemy expression for the substructure match operation.

        Examples
        --------
        >>> mol_column.has_substructure('c1ccccc1')  # benzene ring
        """
        return _bingo_search(self.expr, query, parameters, "bingo.sub")

    def has_smarts(self, query: Any, parameters: Any = "") -> ColumnElement[bool]:
        """
        Check if the molecular structure matches a SMARTS pattern.

        Parameters
        ----------
        query : Any
            The SMARTS pattern string for pattern matching.
        parameters : Any, optional
            Additional parameters for the SMARTS search, by default "".

        Returns
        -------
        ColumnElement[bool]
            A SQLAlchemy expression for the SMARTS pattern match operation.

        Examples
        --------
        >>> mol_column.has_smarts('[#6]1:[#6]:[#6]:[#6]:[#6]:[#6]:1')  # aromatic ring
        """
        return _bingo_search(self.expr, query, parameters, "bingo.smarts")

    def equals(self, query: Any, parameters: Any = "") -> ColumnElement[bool]:
        """
        Check if the molecular structure exactly matches the given structure.

        Parameters
        ----------
        query : Any
            The molecular structure query as a SMILES or MOL string.
        parameters : Any, optional
            Additional parameters for the exact match search, by default "".

        Returns
        -------
        ColumnElement[bool]
            A SQLAlchemy expression for the exact structure match operation.

        Examples
        --------
        >>> mol_column.equals('CCO')  # ethanol exact match
        """
        return _bingo_search(self.expr, query, parameters, "bingo.exact")

    def not_equals(self, query: Any, parameters: Any = "") -> ColumnElement[bool]:
        """
        Check if the molecular structure does not exactly match the given structure.

        Parameters
        ----------
        query : Any
            The molecular structure query as a SMILES or MOL string.
        parameters : Any, optional
            Additional parameters for the exact match search, by default "".

        Returns
        -------
        ColumnElement[bool]
            A SQLAlchemy expression for the negated exact structure match operation.
        """
        return ~self.equals(query, parameters)


class BingoRxnComparator(UserDefinedType.Comparator):
    """
    Comparator class for chemical reaction operations using Bingo database.

    This class provides methods for chemical reaction searching including
    reaction substructure matching, SMARTS pattern matching, and exact reaction matching.
    """

    def __eq__(self, other: Any) -> ColumnElement[bool]:
        if isinstance(other, ColumnElement) and not getattr(
            other, "is_clause_element", False
        ):
            return super().__eq__(other)
        if (
            isinstance(other, ColumnElement)
            and getattr(other, "table", None) is not None
        ):
            return super().__eq__(other)
        return self.equals(other)

    def __ne__(self, other: Any) -> ColumnElement[bool]:
        if isinstance(other, ColumnElement) and not getattr(
            other, "is_clause_element", False
        ):
            return super().__ne__(other)
        if (
            isinstance(other, ColumnElement)
            and getattr(other, "table", None) is not None
        ):
            return super().__ne__(other)
        return self.not_equals(other)

    def has_substructure(self, query: Any, parameters: Any = "") -> ColumnElement[bool]:
        """
        Check if the reaction contains a given substructure pattern.

        Parameters
        ----------
        query : Any
            The reaction substructure query as a reaction SMILES or RXN string.
        parameters : Any, optional
            Additional parameters for the reaction substructure search, by default "".

        Returns
        -------
        ColumnElement[bool]
            A SQLAlchemy expression for the reaction substructure match operation.

        Examples
        --------
        >>> rxn_column.has_substructure('c1ccccc1>>c1ccc(O)cc1')  # phenol formation
        """
        return _bingo_search(self.expr, query, parameters, "bingo.rsub")

    def has_smarts(self, query: Any, parameters: Any = "") -> ColumnElement[bool]:
        """
        Check if the reaction matches a SMARTS pattern.

        Parameters
        ----------
        query : Any
            The reaction SMARTS pattern string for pattern matching.
        parameters : Any, optional
            Additional parameters for the reaction SMARTS search, by default "".

        Returns
        -------
        ColumnElement[bool]
            A SQLAlchemy expression for the reaction SMARTS pattern match operation.

        Examples
        --------
        >>> rxn_column.has_smarts('[C:1]>>[C:1][O]')  # C-O bond formation
        """
        return _bingo_search(self.expr, query, parameters, "bingo.rsmarts")

    def equals(self, query: Any, parameters: Any = "") -> ColumnElement[bool]:
        """
        Check if the reaction exactly matches the given reaction.

        Parameters
        ----------
        query : Any
            The reaction query as a reaction SMILES or RXN string.
        parameters : Any, optional
            Additional parameters for the exact reaction match search, by default "".

        Returns
        -------
        ColumnElement[bool]
            A SQLAlchemy expression for the exact reaction match operation.

        Examples
        --------
        >>> rxn_column.has_equals('CCO>>CC=O')  # ethanol to acetaldehyde exact match
        """
        return _bingo_search(self.expr, query, parameters, "bingo.rexact")

    def not_equals(self, query: Any, parameters: Any = "") -> ColumnElement[bool]:
        """
        Check if the reaction does not exactly match the given reaction.

        Parameters
        ----------
        query : Any
            The reaction query as a reaction SMILES or RXN string.
        parameters : Any, optional
            Additional parameters for the exact reaction match search, by default "".

        Returns
        -------
        ColumnElement[bool]
            A SQLAlchemy expression for the negated exact reaction match operation.
        """
        return ~self.equals(query, parameters)
