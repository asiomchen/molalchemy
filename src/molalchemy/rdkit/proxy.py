"""
Proxy classes for RDKit database operations.

This module contains proxy classes that provide stub methods for type hinting
and autocomplete functionality. The actual implementation is delegated to
the corresponding function classes in the functions module.

This file is auto-generated from the comparator classes.
Do not edit manually - use the update_proxy_stubs.py script instead.
"""


class RdkitMolProxy:
    """
    Proxy class for molecular operations using RDKit database.

    This class provides stub methods for type hinting and autocomplete functionality.
    The actual implementation is delegated to the corresponding function class.
    """

    @staticmethod
    def has_substructure(query: str):
        """Check if this molecule contains `query` as a substructure (@>)."""
        pass

    @staticmethod
    def has_smarts(query: str):
        """Check if this molecule contains SMARTS pattern `query`."""
        pass

    @staticmethod
    def is_substructure_of(query: str):
        """Check if this molecule is a substructure of `query` (<@)."""
        pass

    @staticmethod
    def equals(query: str):
        """Check if this molecule is equal to `query` (@=)."""
        pass

    @staticmethod
    def not_equals(query: str):
        """Check if this molecule is not equal to `query` (@<>)."""
        pass

    @staticmethod
    def has_query_substructure(query: str):
        """Check if this molecule contains a query substructure `query` (@>>)."""
        pass

    @staticmethod
    def is_query_substructure_of(query: str):
        """Check if query structure `query` contains this molecule (<<@)."""
        pass


class RdkitRxnProxy:
    """
    Proxy class for chemical reaction operations using RDKit database.

    This class provides stub methods for type hinting and autocomplete functionality.
    The actual implementation is delegated to the corresponding function class.
    """

    @staticmethod
    def has_substructure(query: str):
        """Check if this reaction contains `query` as a substructure (@>)."""
        pass

    @staticmethod
    def is_substructure_of(query: str):
        """Check if this reaction is a substructure of `query` (<@)."""
        pass

    @staticmethod
    def equals(query: str):
        """Check if this reaction is equal to `query` (@=)."""
        pass

    @staticmethod
    def not_equals(query: str):
        """Check if this reaction is not equal to `query` (@<>)."""
        pass

    @staticmethod
    def has_smarts(query: str):
        """Check if this reaction contains SMARTS pattern `query`."""
        pass

    @staticmethod
    def has_substructure_fp(query: str):
        """Check if this reaction matches `query` via substructure fingerprints (?>)."""
        pass

    @staticmethod
    def is_substructure_fp_of(query: str):
        """Check if this reaction is fingerprint-substructure of `query` (?<)."""
        pass
