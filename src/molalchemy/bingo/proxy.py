"""
Proxy classes for Bingo database operations.

This module contains proxy classes that provide stub methods for type hinting
and autocomplete functionality. The actual implementation is delegated to
the corresponding function classes in the functions module.

This file is auto-generated from the comparator classes.
Do not edit manually - use the update_proxy_stubs.py script instead.
"""


class BingoMolProxy:
    """
    Proxy class for molecular operations using Bingo database.

    This class provides stub methods for type hinting and autocomplete functionality.
    The actual implementation is delegated to the corresponding function class.
    """

    @staticmethod
    def has_substructure(query: str, parameters: str = ""):
        """Check if the molecular structure contains a given substructure.

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
        pass

    @staticmethod
    def has_smarts(query: str, parameters: str = ""):
        """Check if the molecular structure matches a SMARTS pattern.

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
        pass

    @staticmethod
    def equals(query: str, parameters: str = ""):
        """Check if the molecular structure exactly matches the given structure.

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
        pass


class BingoRxnProxy:
    """
    Proxy class for chemical reaction operations using Bingo database.

    This class provides stub methods for type hinting and autocomplete functionality.
    The actual implementation is delegated to the corresponding function class.
    """

    @staticmethod
    def has_substructure(query: str, parameters: str = ""):
        """Check if the reaction contains a given substructure pattern.

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
        pass

    @staticmethod
    def has_smarts(query: str, parameters: str = ""):
        """Check if the reaction matches a SMARTS pattern.

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
        pass

    @staticmethod
    def equals(query: str, parameters: str = ""):
        """Check if the reaction exactly matches the given reaction.

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
        pass
