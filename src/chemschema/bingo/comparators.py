"""Bingo SQLAlchemy comparators for chemical structure searching."""

from sqlalchemy import text
from sqlalchemy.types import UserDefinedType


class BingoMolComparator(UserDefinedType.Comparator):
    """
    Comparator class for molecular structure operations using Bingo database.

    This class provides methods for chemical structure searching including
    substructure matching, SMARTS pattern matching, and exact structure matching.
    """

    def __eq__(self, other: str):
        return self.equals(other)

    def has_substructure(self, query: str, parameters: str = ""):
        """
        Check if the molecular structure contains a given substructure.

        Parameters
        ----------
        query : str
            The substructure query as a SMILES or MOL string.
        parameters : str, optional
            Additional parameters for the substructure search, by default "".

        Returns
        -------
        sqlalchemy expression
            A SQLAlchemy expression for the substructure match operation.

        Examples
        --------
        >>> mol_column.has_substructure('c1ccccc1')  # benzene ring
        """
        return self.expr.op("@")(text(f"('{query}', '{parameters}')::bingo.sub"))

    def has_smarts(self, query: str, parameters: str = ""):
        """
        Check if the molecular structure matches a SMARTS pattern.

        Parameters
        ----------
        query : str
            The SMARTS pattern string for pattern matching.
        parameters : str, optional
            Additional parameters for the SMARTS search, by default "".

        Returns
        -------
        sqlalchemy expression
            A SQLAlchemy expression for the SMARTS pattern match operation.

        Examples
        --------
        >>> mol_column.has_smarts('[#6]1:[#6]:[#6]:[#6]:[#6]:[#6]:1')  # aromatic ring
        """
        return self.expr.op("@")(text(f"('{query}', '{parameters}')::bingo.smarts"))

    def equals(self, query: str, parameters: str = ""):
        """
        Check if the molecular structure exactly matches the given structure.

        Parameters
        ----------
        query : str
            The molecular structure query as a SMILES or MOL string.
        parameters : str, optional
            Additional parameters for the exact match search, by default "".

        Returns
        -------
        sqlalchemy expression
            A SQLAlchemy expression for the exact structure match operation.

        Examples
        --------
        >>> mol_column.equals('CCO')  # ethanol exact match
        """
        return self.expr.op("@")(text(f"('{query}', '{parameters}')::bingo.exact"))


class BingoRxnComparator(UserDefinedType.Comparator):
    """
    Comparator class for chemical reaction operations using Bingo database.

    This class provides methods for chemical reaction searching including
    reaction substructure matching, SMARTS pattern matching, and exact reaction matching.
    """

    def has_substructure(self, query: str, parameters: str = ""):
        """
        Check if the reaction contains a given substructure pattern.

        Parameters
        ----------
        query : str
            The reaction substructure query as a reaction SMILES or RXN string.
        parameters : str, optional
            Additional parameters for the reaction substructure search, by default "".

        Returns
        -------
        sqlalchemy expression
            A SQLAlchemy expression for the reaction substructure match operation.

        Examples
        --------
        >>> rxn_column.has_substructure('c1ccccc1>>c1ccc(O)cc1')  # phenol formation
        """
        return self.expr.op("@")(text(f"('{query}', '{parameters}')::bingo.rsub"))

    def has_smarts(self, query: str, parameters: str = ""):
        """
        Check if the reaction matches a SMARTS pattern.

        Parameters
        ----------
        query : str
            The reaction SMARTS pattern string for pattern matching.
        parameters : str, optional
            Additional parameters for the reaction SMARTS search, by default "".

        Returns
        -------
        sqlalchemy expression
            A SQLAlchemy expression for the reaction SMARTS pattern match operation.

        Examples
        --------
        >>> rxn_column.has_smarts('[C:1]>>[C:1][O]')  # C-O bond formation
        """
        return self.expr.op("@")(text(f"('{query}', '{parameters}')::bingo.rsmarts"))

    def equals(self, query: str, parameters: str = ""):
        """
        Check if the reaction exactly matches the given reaction.

        Parameters
        ----------
        query : str
            The reaction query as a reaction SMILES or RXN string.
        parameters : str, optional
            Additional parameters for the exact reaction match search, by default "".

        Returns
        -------
        sqlalchemy expression
            A SQLAlchemy expression for the exact reaction match operation.

        Examples
        --------
        >>> rxn_column.has_equals('CCO>>CC=O')  # ethanol to acetaldehyde exact match
        """
        return self.expr.op("@")(text(f"('{query}', '{parameters}')::bingo.rexact"))
