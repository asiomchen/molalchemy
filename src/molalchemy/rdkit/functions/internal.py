"""
Auto-generated from `data/rdkit/functions.json`. Do not edit manually.
This file defines internal RDKit PostgreSQL function wrappers for use with SQLAlchemy. You probably don't want to use these directly.
"""

from typing import Any

from sqlalchemy import types as sqltypes
from sqlalchemy.sql.functions import GenericFunction

from molalchemy.rdkit.types import (
    RdkitBitFingerprint,
    RdkitMol,
    RdkitQMol,
    RdkitReaction,
    RdkitSparseFingerprint,
    RdkitXQMol,
)
from molalchemy.types import CString


class bfp_cmp(GenericFunction):
    inherit_cache = True

    def __init__(
        self, fp_1: RdkitBitFingerprint, fp_2: RdkitBitFingerprint, **kwargs: Any
    ) -> None:
        """Calls the rdkit cartridge function `bfp_cmp`.

        Parameters
        ----------
        fp_1
            The first RDKit bit fingerprint for comparison.
        fp_2
            The second RDKit bit fingerprint for comparison.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            An integer representing the comparison result between the two bit fingerprints. Typically, 0 indicates equality, a negative value indicates the first fingerprint is 'less than' the second, and a positive value indicates the first is 'greater than' the second.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class bfp_eq(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, fp_1: RdkitBitFingerprint, fp_2: RdkitBitFingerprint, **kwargs: Any
    ) -> None:
        """Checks if two bit vector fingerprints are equal. Used for operator overloading.

        Parameters
        ----------
        fp_1
            The first bit vector fingerprint for comparison.
        fp_2
            The second bit vector fingerprint for comparison.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            True if the two bit vector fingerprints are equal, False otherwise.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class bfp_ge(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, fp_1: RdkitBitFingerprint, fp_2: RdkitBitFingerprint, **kwargs: Any
    ) -> None:
        """Returns whether the first bit fingerprint is greater than or equal to the second bit fingerprint. Used for operator overloading.

        Parameters
        ----------
        fp_1
            The first bit fingerprint.
        fp_2
            The second bit fingerprint.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean value indicating if the first fingerprint is greater than or equal to the second.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class bfp_gt(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, fp_1: RdkitBitFingerprint, fp_2: RdkitBitFingerprint, **kwargs: Any
    ) -> None:
        """Returns whether the first bit vector fingerprint is 'greater than' the second bit vector fingerprint. Used internally for operator overloading.

        Parameters
        ----------
        fp_1
            The first bit vector fingerprint.
        fp_2
            The second bit vector fingerprint for comparison.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean indicating if the first fingerprint is 'greater than' the second.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class bfp_in(GenericFunction):
    type = RdkitBitFingerprint()
    inherit_cache = True

    def __init__(self, input: CString, **kwargs: Any) -> None:
        """Converts a string representation into an RDKit bit fingerprint. Used for input conversion from the client.

        Parameters
        ----------
        input
            The string representation of the bit fingerprint.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitBitFingerprint]
            The RDKit bit fingerprint object.
        """
        super().__init__(input, **kwargs)


class bfp_lt(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, fp_1: RdkitBitFingerprint, fp_2: RdkitBitFingerprint, **kwargs: Any
    ) -> None:
        """Returns a boolean indicating whether or not the first bit fingerprint is less than the second bit fingerprint. Used internally for operator overloading.

        Parameters
        ----------
        fp_1
            The first bit fingerprint to compare.
        fp_2
            The second bit fingerprint to compare.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean value indicating the result of the 'less than' comparison.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class bfp_ne(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, bfp1: RdkitBitFingerprint, bfp2: RdkitBitFingerprint, **kwargs: Any
    ) -> None:
        """Compares two bit vector fingerprints for inequality. Used internally for operator overloading.

        Parameters
        ----------
        bfp1
            The first bit vector fingerprint.
        bfp2
            The second bit vector fingerprint.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            True if the two bit vector fingerprints are not equal, False otherwise.
        """
        super().__init__(bfp1, bfp2, **kwargs)


class bfp_out(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(self, fp: RdkitBitFingerprint, **kwargs: Any) -> None:
        """Returns a bytea with the binary string representation of the fingerprint. Used internally to return fingerprint values to the client.

        Parameters
        ----------
        fp
            The bit vector fingerprint to convert to a binary string representation.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            A bytea with the binary string representation of the fingerprint.
        """
        super().__init__(fp, **kwargs)


class fmcs_smiles_transition(GenericFunction):
    type = sqltypes.Text()
    inherit_cache = True

    def __init__(
        self, arg_1: sqltypes.Text, arg_2: sqltypes.Text, **kwargs: Any
    ) -> None:
        """TODO

        Parameters
        ----------
        arg_1
            TODO.
        arg_2
            TODO.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Text]
            A string representing the Most Common Substructure (MCS) found among the input molecules.
        """
        super().__init__(arg_1, arg_2, **kwargs)


class mol_cmp(GenericFunction):
    inherit_cache = True

    def __init__(self, mol_1: RdkitMol, mol_2: RdkitMol, **kwargs: Any) -> None:
        """Compares two RDKit molecules.

        Parameters
        ----------
        mol_1
            The first RDKit molecule to compare.
        mol_2
            The second RDKit molecule to compare.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            An integer representing the comparison result. Returns -1 if the first molecule is 'less than' the second, 0 if they are 'equal', and 1 if the first molecule is 'greater than' the second.
        """
        super().__init__(mol_1, mol_2, **kwargs)


class mol_eq(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(self, mol_1: RdkitMol, mol_2: RdkitMol, **kwargs: Any) -> None:
        """Checks if two RDKit molecules are equal. Used internally for operator overloading.

        Parameters
        ----------
        mol_1
            The first RDKit molecule to compare.
        mol_2
            The second RDKit molecule to compare.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            Returns a boolean indicating whether the two molecules are equal.
        """
        super().__init__(mol_1, mol_2, **kwargs)


class mol_ge(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(self, arg_1: RdkitMol, arg_2: RdkitMol, **kwargs: Any) -> None:
        """Checks if the first RDKit molecule is a superstructure of, or identical to, the second RDKit molecule. Used internally for operator overloading.

        Parameters
        ----------
        arg_1
            The RDKit molecule to be checked as the potential superstructure.
        arg_2
            The RDKit molecule to be checked as the potential substructure.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean value: true if the first molecule is a superstructure of or identical to the second, false otherwise.
        """
        super().__init__(arg_1, arg_2, **kwargs)


class mol_gt(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(self, mol_1: RdkitMol, mol_2: RdkitMol, **kwargs: Any) -> None:
        """Compares two RDKit molecules to determine if the first molecule is greater than the second, based on an internal canonical ordering. Used internally for operator overloading.

        Parameters
        ----------
        mol_1
            The first RDKit molecule for comparison.
        mol_2
            The second RDKit molecule for comparison.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            True if the first molecule is greater than the second, False otherwise.
        """
        super().__init__(mol_1, mol_2, **kwargs)


class mol_in(GenericFunction):
    type = RdkitMol()
    inherit_cache = True

    def __init__(self, mol_str: CString, **kwargs: Any) -> None:
        """Internal function used to load the molecule from the client input.

        Parameters
        ----------
        mol_str
            The string representation of the molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitMol]
            An RDKit molecule object.
        """
        super().__init__(mol_str, **kwargs)


class mol_le(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(self, mol_1: RdkitMol, mol_2: RdkitMol, **kwargs: Any) -> None:
        """Compares two RDKit molecules to check if the first is less than or equal to the second. Used internally for operator overloading

        Parameters
        ----------
        mol_1
            The first RDKit molecule for comparison.
        mol_2
            The second RDKit molecule for comparison.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            `True` if the first molecule is less than or equal to the second, `False` otherwise.
        """
        super().__init__(mol_1, mol_2, **kwargs)


class mol_lt(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(self, mol_1: RdkitMol, mol_2: RdkitMol, **kwargs: Any) -> None:
        """Compares two RDKit molecules to determine if the first molecule is less than the second molecule. Used internally for operator overloading

        Parameters
        ----------
        mol_1
            The first RDKit molecule.
        mol_2
            The second RDKit molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            `True` if the first molecule is less than the second molecule, `False` otherwise.
        """
        super().__init__(mol_1, mol_2, **kwargs)


class mol_ne(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(self, mol_1: RdkitMol, mol_2: RdkitMol, **kwargs: Any) -> None:
        """Returns a boolean indicating whether or not two molecules are not equal. Used internally for the operator overloading

        Parameters
        ----------
        mol_1
            The first molecule to compare.
        mol_2
            The second molecule to compare.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean indicating if the two molecules are not equal.
        """
        super().__init__(mol_1, mol_2, **kwargs)


class mol_out(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Calls the RDKit cartridge function `mol_out` to return a string representation of the molecule. Used internally for displaying molecules in query results.

        Parameters
        ----------
        mol
            The RDKit molecule to be converted to a string.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            A string representation of the molecule.
        """
        super().__init__(mol, **kwargs)


class qmol_in(GenericFunction):
    type = RdkitQMol()
    inherit_cache = True

    def __init__(self, mol_str: CString, **kwargs: Any) -> None:
        """Constructs an RDKit query molecule from a string representation. This function is used internally for receiving a query molecule from the client.

        Parameters
        ----------
        mol_str
            The string representation of the query molecule
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitQMol]
            An RDKit query molecule.
        """
        super().__init__(mol_str, **kwargs)


class qmol_out(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(self, mol: RdkitQMol, **kwargs: Any) -> None:
        """Returns the SMARTS string for a query molecule. This function is used internally for sending the result of a query molecule to the client.

        Parameters
        ----------
        mol
            The query molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            The SMARTS string representation of the query molecule.
        """
        super().__init__(mol, **kwargs)


class reaction_eq(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, rxn_1: RdkitReaction, rxn_2: RdkitReaction, **kwargs: Any
    ) -> None:
        """Checks if two RDKit reactions are equivalent. Used internally for the operator overloading.

        Parameters
        ----------
        rxn_1
            The first RDKit reaction.
        rxn_2
            The second RDKit reaction.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            True if the reactions are equivalent, False otherwise.
        """
        super().__init__(rxn_1, rxn_2, **kwargs)


class reaction_in(GenericFunction):
    type = RdkitReaction()
    inherit_cache = True

    def __init__(self, rxn_str: CString, **kwargs: Any) -> None:
        """Converts a string representation of a chemical reaction into an RDKit reaction object.

        Parameters
        ----------
        rxn_str
            The string representation of the chemical reaction, typically in reaction SMILES format.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitReaction]
            An RDKit reaction object representing the parsed chemical reaction.
        """
        super().__init__(rxn_str, **kwargs)


class reaction_ne(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, rxn_1: RdkitReaction, rxn_2: RdkitReaction, **kwargs: Any
    ) -> None:
        """Returns true if the two reactions are not equal. Used internally for the operator overloading

        Parameters
        ----------
        rxn_1
            The first RDKit reaction.
        rxn_2
            The second RDKit reaction.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            True if the reactions are not equal, False otherwise.
        """
        super().__init__(rxn_1, rxn_2, **kwargs)


class reaction_out(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(self, rxn: RdkitReaction, **kwargs: Any) -> None:
        """Internal function: Converts an RDKit reaction object to its string representation.

        Parameters
        ----------
        rxn
            The RDKit reaction object to convert.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            The string representation of the RDKit reaction.
        """
        super().__init__(rxn, **kwargs)


class sfp_cmp(GenericFunction):
    inherit_cache = True

    def __init__(
        self,
        arg_1: RdkitSparseFingerprint,
        arg_2: RdkitSparseFingerprint,
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `sfp_cmp`.

        Parameters
        ----------
        arg_1
            The first sparse fingerprint to compare.
        arg_2
            The second sparse fingerprint to compare.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            TODO
        """
        super().__init__(arg_1, arg_2, **kwargs)


class sfp_eq(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, fp_1: RdkitSparseFingerprint, fp_2: RdkitSparseFingerprint, **kwargs: Any
    ) -> None:
        """Returns a boolean indicating whether or not the two sparse fingerprint arguments are equal. Used for the operator overloading

        Parameters
        ----------
        fp_1
            The first sparse fingerprint.
        fp_2
            The second sparse fingerprint.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean indicating the equality of the two sparse fingerprints.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class sfp_ge(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, fp_1: RdkitSparseFingerprint, fp_2: RdkitSparseFingerprint, **kwargs: Any
    ) -> None:
        """Returns a boolean indicating whether the first sparse fingerprint is element-wise greater than or equal to the second sparse fingerprint. Used for the operator overloading

        Parameters
        ----------
        fp_1
            The first sparse fingerprint (sfp) for comparison.
        fp_2
            The second sparse fingerprint (sfp) for comparison.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean indicating whether the first sparse fingerprint is element-wise greater than or equal to the second sparse fingerprint.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class sfp_gt(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, fp_1: RdkitSparseFingerprint, fp_2: RdkitSparseFingerprint, **kwargs: Any
    ) -> None:
        """Returns a boolean indicating whether all elements of the first sparse fingerprint are greater than the corresponding elements of the second sparse fingerprint. Used for the operator overloading

        Parameters
        ----------
        fp_1
            The first sparse fingerprint for comparison.
        fp_2
            The second sparse fingerprint for comparison.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            `True` if all elements of the first sparse fingerprint are greater than the corresponding elements of the second, False otherwise.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class sfp_in(GenericFunction):
    type = RdkitSparseFingerprint()
    inherit_cache = True

    def __init__(self, fp_string: CString, **kwargs: Any) -> None:
        """Internal function, that constructs an RDKit sparse fingerprint (sfp) from a string representation.

        Parameters
        ----------
        fp_string
            The string representation of the sparse fingerprint.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitSparseFingerprint]
            The RDKit sparse fingerprint (sfp) object.
        """
        super().__init__(fp_string, **kwargs)


class sfp_le(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, fp_1: RdkitSparseFingerprint, fp_2: RdkitSparseFingerprint, **kwargs: Any
    ) -> None:
        """Returns a boolean indicating whether the first sparse fingerprint is element-wise less than or equal to the second sparse fingerprint. Used for the operator overloading

        Parameters
        ----------
        fp_1
            The first RDKit sparse fingerprint.
        fp_2
            The second RDKit sparse fingerprint.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            True if the first sparse fingerprint is element-wise less than or equal to the second; otherwise, False.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class sfp_lt(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, fp_1: RdkitSparseFingerprint, fp_2: RdkitSparseFingerprint, **kwargs: Any
    ) -> None:
        """Returns a boolean indicating whether the first sparse fingerprint is less than the second sparse fingerprint. Used for the operator overloading

        Parameters
        ----------
        fp_1
            The first sparse fingerprint to compare.
        fp_2
            The second sparse fingerprint to compare.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean value (True if the first sparse fingerprint is less than the second, False otherwise).
        """
        super().__init__(fp_1, fp_2, **kwargs)


class sfp_ne(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, fp_1: RdkitSparseFingerprint, fp_2: RdkitSparseFingerprint, **kwargs: Any
    ) -> None:
        """Returns a boolean indicating whether two sparse fingerprints are not equal. Used for the operator overloading

        Parameters
        ----------
        fp_1
            The first sparse fingerprint.
        fp_2
            The second sparse fingerprint.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            `True` if the two sparse fingerprints are not equal, `False` otherwise.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class sfp_out(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(self, fp: RdkitSparseFingerprint, **kwargs: Any) -> None:
        """Internal function, that returns a string representation of a sparse fingerprint.

        Parameters
        ----------
        fp
            The sparse fingerprint to be converted to a string.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            A string representation of the sparse fingerprint.
        """
        super().__init__(fp, **kwargs)


class tanimoto_sml_op(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self,
        fp_1: RdkitSparseFingerprint | RdkitBitFingerprint,
        fp_2: RdkitSparseFingerprint | RdkitBitFingerprint,
        **kwargs: Any,
    ) -> None:
        """Calculates the Tanimoto similarity between two fingerprints of the same type and returns a boolean result. Used internally for operator overloading.

        Parameters
        ----------
        fp_1
            The first fingerprint, which can be either a sparse fingerprint (sfp) or a bit vector fingerprint (bfp).
        fp_2
            The second fingerprint, which must be of the same type as the first fingerprint (either sfp or bfp).
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean value representing the result of the Tanimoto similarity operation.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class xqmol_in(GenericFunction):
    type = RdkitXQMol()
    inherit_cache = True

    def __init__(self, arg_1: CString, **kwargs: Any) -> None:
        """Internal function: Constructs a query molecule from an input string.

        Parameters
        ----------
        arg_1
            The string representation of the query molecule (e.g., SMILES, SMARTS, or CTAB).
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitXQMol]
            A query molecule (RdkitXQMol) object.
        """
        super().__init__(arg_1, **kwargs)


class xqmol_out(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(self, arg_1: RdkitXQMol, **kwargs: Any) -> None:
        """Internal function used to retrieve the string representation of an `RdkitXQMol` object.

        Parameters
        ----------
        arg_1
            The RDKit query molecule to convert to a string.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            TODO
        """
        super().__init__(arg_1, **kwargs)
