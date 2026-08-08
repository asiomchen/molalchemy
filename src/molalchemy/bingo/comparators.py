"""Bingo SQLAlchemy comparators for chemical structure searching."""

from sqlalchemy import ColumnElement
from sqlalchemy.types import UserDefinedType

from molalchemy.bingo.functions.general import mol_similarity_score
from molalchemy.bingo.search import _bingo_search_values
from molalchemy.protocols import (
    BingoOperand,
    BingoParameters,
    BingoSimilarityBound,
)


def _bingo_search(
    column: ColumnElement[object],
    query: BingoOperand,
    parameters: BingoParameters,
    search_type: str,
) -> ColumnElement[bool]:
    return _bingo_search_values(column, (query, parameters), search_type)


class BingoMolComparator(UserDefinedType.Comparator):
    """
    Comparator class for molecular structure operations using Bingo database.

    This class provides methods for chemical structure searching including
    substructure matching, SMARTS pattern matching, and exact structure matching.
    """

    def has_substructure(
        self, query: BingoOperand, parameters: BingoParameters = ""
    ) -> ColumnElement[bool]:
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

    def has_smarts(
        self, query: BingoOperand, parameters: BingoParameters = ""
    ) -> ColumnElement[bool]:
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

    def equals(
        self, query: BingoOperand, parameters: BingoParameters = ""
    ) -> ColumnElement[bool]:
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

    def not_equals(
        self, query: BingoOperand, parameters: BingoParameters = ""
    ) -> ColumnElement[bool]:
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

    def similar_to(
        self,
        query: BingoOperand,
        minimum: BingoSimilarityBound = 0.0,
        maximum: BingoSimilarityBound = 1.0,
        metric: BingoParameters = "Tanimoto",
    ) -> ColumnElement[bool]:
        """Check whether similarity to `query` is within the requested range."""
        return _bingo_search_values(
            self.expr, (minimum, maximum, query, metric), "bingo.sim"
        )

    def similarity_score(
        self,
        query: BingoOperand,
        metric: BingoParameters = "Tanimoto",
    ) -> ColumnElement[float]:
        """Return the numeric similarity score for `query`."""
        return mol_similarity_score(self.expr, query, metric)


class BingoRxnComparator(UserDefinedType.Comparator):
    """
    Comparator class for chemical reaction operations using Bingo database.

    This class provides methods for chemical reaction searching including
    reaction substructure matching, SMARTS pattern matching, and exact reaction matching.
    """

    def has_substructure(
        self, query: BingoOperand, parameters: BingoParameters = ""
    ) -> ColumnElement[bool]:
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

    def has_smarts(
        self, query: BingoOperand, parameters: BingoParameters = ""
    ) -> ColumnElement[bool]:
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

    def equals(
        self, query: BingoOperand, parameters: BingoParameters = ""
    ) -> ColumnElement[bool]:
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

    def not_equals(
        self, query: BingoOperand, parameters: BingoParameters = ""
    ) -> ColumnElement[bool]:
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
