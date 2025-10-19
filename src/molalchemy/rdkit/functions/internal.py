"""Auto-generated from data/rdkit_functions.json. Do not edit manually."""

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
    """
    Calls the rdkit cartridge function `bfp_cmp`.


    Parameters
    ----------
    fp_1: RdkitBitFingerprint  The first RDKit bit fingerprint for comparison.
    fp_2: RdkitBitFingerprint  The second RDKit bit fingerprint for comparison.


    Returns
    -------
    Function[int | sqltypes.Integer]
        An integer representing the comparison result between the two bit fingerprints. Typically, 0 indicates equality, a negative value indicates the first fingerprint is 'less than' the second, and a positive value indicates the first is 'greater than' the second.
    """

    def __init__(self, fp_1: RdkitBitFingerprint, fp_2: RdkitBitFingerprint):
        super().__init__(fp_1, fp_2)


class bfp_eq(GenericFunction):
    """
    Checks if two bit vector fingerprints are equal. Used for operator overloading.


    Parameters
    ----------
    fp_1: RdkitBitFingerprint  The first bit vector fingerprint for comparison.
    fp_2: RdkitBitFingerprint  The second bit vector fingerprint for comparison.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        True if the two bit vector fingerprints are equal, False otherwise.
    """

    def __init__(self, fp_1: RdkitBitFingerprint, fp_2: RdkitBitFingerprint):
        super().__init__(fp_1, fp_2)


class bfp_ge(GenericFunction):
    """
    Returns whether the first bit fingerprint is greater than or equal to the second bit fingerprint. Used for operator overloading.


    Parameters
    ----------
    fp_1: RdkitBitFingerprint  The first bit fingerprint.
    fp_2: RdkitBitFingerprint  The second bit fingerprint.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        A boolean value indicating if the first fingerprint is greater than or equal to the second.
    """

    def __init__(self, fp_1: RdkitBitFingerprint, fp_2: RdkitBitFingerprint):
        super().__init__(fp_1, fp_2)


class bfp_gt(GenericFunction):
    """
    Returns whether the first bit vector fingerprint is 'greater than' the second bit vector fingerprint. Used internally for operator overloading.


    Parameters
    ----------
    fp_1: RdkitBitFingerprint  The first bit vector fingerprint.
    fp_2: RdkitBitFingerprint  The second bit vector fingerprint for comparison.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        A boolean indicating if the first fingerprint is 'greater than' the second.
    """

    def __init__(self, fp_1: RdkitBitFingerprint, fp_2: RdkitBitFingerprint):
        super().__init__(fp_1, fp_2)


class bfp_in(GenericFunction):
    """
    Converts a string representation into an RDKit bit fingerprint. Used for input conversion from the client.


    Parameters
    ----------
    input: CString  The string representation of the bit fingerprint.


    Returns
    -------
    Function[RdkitBitFingerprint]
        The RDKit bit fingerprint object.
    """

    def __init__(self, input: CString):
        super().__init__(input)


class bfp_lt(GenericFunction):
    """
    Returns a boolean indicating whether or not the first bit fingerprint is less than the second bit fingerprint. Used internally for operator overloading.


    Parameters
    ----------
    fp_1: RdkitBitFingerprint  The first bit fingerprint to compare.
    fp_2: RdkitBitFingerprint  The second bit fingerprint to compare.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        A boolean value indicating the result of the 'less than' comparison.
    """

    def __init__(self, fp_1: RdkitBitFingerprint, fp_2: RdkitBitFingerprint):
        super().__init__(fp_1, fp_2)


class bfp_ne(GenericFunction):
    """
    Compares two bit vector fingerprints for inequality. Used internally for operator overloading.


    Parameters
    ----------
    bfp1: RdkitBitFingerprint  The first bit vector fingerprint.
    bfp2: RdkitBitFingerprint  The second bit vector fingerprint.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        True if the two bit vector fingerprints are not equal, False otherwise.
    """

    def __init__(self, bfp1: RdkitBitFingerprint, bfp2: RdkitBitFingerprint):
        super().__init__(bfp1, bfp2)


class bfp_out(GenericFunction):
    """
    Returns a bytea with the binary string representation of the fingerprint. Used internally to return fingerprint values to the client.


    Parameters
    ----------
    fp: RdkitBitFingerprint  The bit vector fingerprint to convert to a binary string representation.


    Returns
    -------
    Function[CString]
        A bytea with the binary string representation of the fingerprint.
    """

    def __init__(self, fp: RdkitBitFingerprint):
        super().__init__(fp)


class fmcs_smiles_transition(GenericFunction):
    """
    TODO


    Parameters
    ----------
    arg_1: sqltypes.Text  TODO.
    arg_2: sqltypes.Text  TODO.


    Returns
    -------
    Function[sqltypes.Text]
        A string representing the Most Common Substructure (MCS) found among the input molecules.
    """

    def __init__(self, arg_1: sqltypes.Text, arg_2: sqltypes.Text):
        super().__init__(arg_1, arg_2)


class mol_cmp(GenericFunction):
    """
    Compares two RDKit molecules.


    Parameters
    ----------
    mol_1: RdkitMol  The first RDKit molecule to compare.
    mol_2: RdkitMol  The second RDKit molecule to compare.


    Returns
    -------
    Function[int | sqltypes.Integer]
        An integer representing the comparison result. Returns -1 if the first molecule is 'less than' the second, 0 if they are 'equal', and 1 if the first molecule is 'greater than' the second.
    """

    def __init__(self, mol_1: RdkitMol, mol_2: RdkitMol):
        super().__init__(mol_1, mol_2)


class mol_eq(GenericFunction):
    """
    Checks if two RDKit molecules are equal. Used internally for operator overloading.


    Parameters
    ----------
    mol_1: RdkitMol  The first RDKit molecule to compare.
    mol_2: RdkitMol  The second RDKit molecule to compare.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        Returns a boolean indicating whether the two molecules are equal.
    """

    def __init__(self, mol_1: RdkitMol, mol_2: RdkitMol):
        super().__init__(mol_1, mol_2)


class mol_ge(GenericFunction):
    """
    Checks if the first RDKit molecule is a superstructure of, or identical to, the second RDKit molecule. Used internally for operator overloading.


    Parameters
    ----------
    arg_1: RdkitMol  The RDKit molecule to be checked as the potential superstructure.
    arg_2: RdkitMol  The RDKit molecule to be checked as the potential substructure.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        A boolean value: true if the first molecule is a superstructure of or identical to the second, false otherwise.
    """

    def __init__(self, arg_1: RdkitMol, arg_2: RdkitMol):
        super().__init__(arg_1, arg_2)


class mol_gt(GenericFunction):
    """
    Compares two RDKit molecules to determine if the first molecule is greater than the second, based on an internal canonical ordering. Used internally for operator overloading.


    Parameters
    ----------
    mol_1: RdkitMol  The first RDKit molecule for comparison.
    mol_2: RdkitMol  The second RDKit molecule for comparison.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        True if the first molecule is greater than the second, False otherwise.
    """

    def __init__(self, mol_1: RdkitMol, mol_2: RdkitMol):
        super().__init__(mol_1, mol_2)


class mol_in(GenericFunction):
    """
    Internal function used to load the molecule from the client input.


    Parameters
    ----------
    mol_str: CString  The string representation of the molecule.


    Returns
    -------
    Function[RdkitMol]
        An RDKit molecule object.
    """

    def __init__(self, mol_str: CString):
        super().__init__(mol_str)


class mol_le(GenericFunction):
    """
    Compares two RDKit molecules to check if the first is less than or equal to the second. Used internally for operator overloading


    Parameters
    ----------
    mol_1: RdkitMol  The first RDKit molecule for comparison.
    mol_2: RdkitMol  The second RDKit molecule for comparison.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        `True` if the first molecule is less than or equal to the second, `False` otherwise.
    """

    def __init__(self, mol_1: RdkitMol, mol_2: RdkitMol):
        super().__init__(mol_1, mol_2)


class mol_lt(GenericFunction):
    """
    Compares two RDKit molecules to determine if the first molecule is less than the second molecule. Used internally for operator overloading


    Parameters
    ----------
    mol_1: RdkitMol  The first RDKit molecule.
    mol_2: RdkitMol  The second RDKit molecule.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        `True` if the first molecule is less than the second molecule, `False` otherwise.
    """

    def __init__(self, mol_1: RdkitMol, mol_2: RdkitMol):
        super().__init__(mol_1, mol_2)


class mol_ne(GenericFunction):
    """
    Returns a boolean indicating whether or not two molecules are not equal. Used internally for the operator overloading


    Parameters
    ----------
    mol_1: RdkitMol  The first molecule to compare.
    mol_2: RdkitMol  The second molecule to compare.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        A boolean indicating if the two molecules are not equal.
    """

    def __init__(self, mol_1: RdkitMol, mol_2: RdkitMol):
        super().__init__(mol_1, mol_2)


class mol_out(GenericFunction):
    """
    Calls the RDKit cartridge function `mol_out` to return a string representation of the molecule. Used internally for displaying molecules in query results.


    Parameters
    ----------
    mol: RdkitMol  The RDKit molecule to be converted to a string.


    Returns
    -------
    Function[CString]
        A string representation of the molecule.
    """

    def __init__(self, mol: RdkitMol):
        super().__init__(mol)


class qmol_in(GenericFunction):
    """
    Constructs an RDKit query molecule from a string representation. This function is used internally for receiving a query molecule from the client.


    Parameters
    ----------
    mol_str: CString  The string representation of the query molecule


    Returns
    -------
    Function[RdkitQMol]
        An RDKit query molecule.
    """

    def __init__(self, mol_str: CString):
        super().__init__(mol_str)


class qmol_out(GenericFunction):
    """
    Returns the SMARTS string for a query molecule. This function is used internally for sending the result of a query molecule to the client.


    Parameters
    ----------
    mol: RdkitQMol  The query molecule.


    Returns
    -------
    Function[CString]
        The SMARTS string representation of the query molecule.
    """

    def __init__(self, mol: RdkitQMol):
        super().__init__(mol)


class reaction_eq(GenericFunction):
    """
    Checks if two RDKit reactions are equivalent. Used internally for the operator overloading.


    Parameters
    ----------
    rxn_1: RdkitReaction  The first RDKit reaction.
    rxn_2: RdkitReaction  The second RDKit reaction.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        True if the reactions are equivalent, False otherwise.
    """

    def __init__(self, rxn_1: RdkitReaction, rxn_2: RdkitReaction):
        super().__init__(rxn_1, rxn_2)


class reaction_in(GenericFunction):
    """
    Converts a string representation of a chemical reaction into an RDKit reaction object.


    Parameters
    ----------
    rxn_str: CString  The string representation of the chemical reaction, typically in reaction SMILES format.


    Returns
    -------
    Function[RdkitReaction]
        An RDKit reaction object representing the parsed chemical reaction.
    """

    def __init__(self, rxn_str: CString):
        super().__init__(rxn_str)


class reaction_ne(GenericFunction):
    """
    Returns true if the two reactions are not equal. Used internally for the operator overloading


    Parameters
    ----------
    rxn_1: RdkitReaction  The first RDKit reaction.
    rxn_2: RdkitReaction  The second RDKit reaction.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        True if the reactions are not equal, False otherwise.
    """

    def __init__(self, rxn_1: RdkitReaction, rxn_2: RdkitReaction):
        super().__init__(rxn_1, rxn_2)


class reaction_out(GenericFunction):
    """
    Internal function: Converts an RDKit reaction object to its string representation.


    Parameters
    ----------
    rxn: RdkitReaction  The RDKit reaction object to convert.


    Returns
    -------
    Function[CString]
        The string representation of the RDKit reaction.
    """

    def __init__(self, rxn: RdkitReaction):
        super().__init__(rxn)


class sfp_cmp(GenericFunction):
    """
    Calls the rdkit cartridge function `sfp_cmp`.


    Parameters
    ----------
    arg_1: RdkitSparseFingerprint  The first sparse fingerprint to compare.
    arg_2: RdkitSparseFingerprint  The second sparse fingerprint to compare.


    Returns
    -------
    Function[int | sqltypes.Integer]
        TODO
    """

    def __init__(self, arg_1: RdkitSparseFingerprint, arg_2: RdkitSparseFingerprint):
        super().__init__(arg_1, arg_2)


class sfp_eq(GenericFunction):
    """
    Returns a boolean indicating whether or not the two sparse fingerprint arguments are equal. Used for the operator overloading


    Parameters
    ----------
    fp_1: RdkitSparseFingerprint  The first sparse fingerprint.
    fp_2: RdkitSparseFingerprint  The second sparse fingerprint.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        A boolean indicating the equality of the two sparse fingerprints.
    """

    def __init__(self, fp_1: RdkitSparseFingerprint, fp_2: RdkitSparseFingerprint):
        super().__init__(fp_1, fp_2)


class sfp_ge(GenericFunction):
    """
    Returns a boolean indicating whether the first sparse fingerprint is element-wise greater than or equal to the second sparse fingerprint. Used for the operator overloading


    Parameters
    ----------
    fp_1: RdkitSparseFingerprint  The first sparse fingerprint (sfp) for comparison.
    fp_2: RdkitSparseFingerprint  The second sparse fingerprint (sfp) for comparison.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        A boolean indicating whether the first sparse fingerprint is element-wise greater than or equal to the second sparse fingerprint.
    """

    def __init__(self, fp_1: RdkitSparseFingerprint, fp_2: RdkitSparseFingerprint):
        super().__init__(fp_1, fp_2)


class sfp_gt(GenericFunction):
    """
    Returns a boolean indicating whether all elements of the first sparse fingerprint are greater than the corresponding elements of the second sparse fingerprint. Used for the operator overloading


    Parameters
    ----------
    fp_1: RdkitSparseFingerprint  The first sparse fingerprint for comparison.
    fp_2: RdkitSparseFingerprint  The second sparse fingerprint for comparison.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        `True` if all elements of the first sparse fingerprint are greater than the corresponding elements of the second, False otherwise.
    """

    def __init__(self, fp_1: RdkitSparseFingerprint, fp_2: RdkitSparseFingerprint):
        super().__init__(fp_1, fp_2)


class sfp_in(GenericFunction):
    """
    Internal function, that constructs an RDKit sparse fingerprint (sfp) from a string representation.


    Parameters
    ----------
    fp_string: CString  The string representation of the sparse fingerprint.


    Returns
    -------
    Function[RdkitSparseFingerprint]
        The RDKit sparse fingerprint (sfp) object.
    """

    def __init__(self, fp_string: CString):
        super().__init__(fp_string)


class sfp_le(GenericFunction):
    """
    Returns a boolean indicating whether the first sparse fingerprint is element-wise less than or equal to the second sparse fingerprint. Used for the operator overloading


    Parameters
    ----------
    fp_1: RdkitSparseFingerprint  The first RDKit sparse fingerprint.
    fp_2: RdkitSparseFingerprint  The second RDKit sparse fingerprint.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        True if the first sparse fingerprint is element-wise less than or equal to the second; otherwise, False.
    """

    def __init__(self, fp_1: RdkitSparseFingerprint, fp_2: RdkitSparseFingerprint):
        super().__init__(fp_1, fp_2)


class sfp_lt(GenericFunction):
    """
    Returns a boolean indicating whether the first sparse fingerprint is less than the second sparse fingerprint. Used for the operator overloading


    Parameters
    ----------
    fp_1: RdkitSparseFingerprint  The first sparse fingerprint to compare.
    fp_2: RdkitSparseFingerprint  The second sparse fingerprint to compare.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        A boolean value (True if the first sparse fingerprint is less than the second, False otherwise).
    """

    def __init__(self, fp_1: RdkitSparseFingerprint, fp_2: RdkitSparseFingerprint):
        super().__init__(fp_1, fp_2)


class sfp_ne(GenericFunction):
    """
    Returns a boolean indicating whether two sparse fingerprints are not equal. Used for the operator overloading


    Parameters
    ----------
    fp_1: RdkitSparseFingerprint  The first sparse fingerprint.
    fp_2: RdkitSparseFingerprint  The second sparse fingerprint.


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        `True` if the two sparse fingerprints are not equal, `False` otherwise.
    """

    def __init__(self, fp_1: RdkitSparseFingerprint, fp_2: RdkitSparseFingerprint):
        super().__init__(fp_1, fp_2)


class sfp_out(GenericFunction):
    """
    Internal function, that returns a string representation of a sparse fingerprint.


    Parameters
    ----------
    fp: RdkitSparseFingerprint  The sparse fingerprint to be converted to a string.


    Returns
    -------
    Function[CString]
        A string representation of the sparse fingerprint.
    """

    def __init__(self, fp: RdkitSparseFingerprint):
        super().__init__(fp)


class tanimoto_sml_op(GenericFunction):
    """
    Calculates the Tanimoto similarity between two fingerprints of the same type and returns a boolean result. Used internally for operator overloading.


    Parameters
    ----------
    fp_1: RdkitSparseFingerprint | RdkitBitFingerprint  The first fingerprint, which can be either a sparse fingerprint (sfp) or a bit vector fingerprint (bfp).
    fp_2: RdkitSparseFingerprint | RdkitBitFingerprint  The second fingerprint, which must be of the same type as the first fingerprint (either sfp or bfp).


    Returns
    -------
    Function[bool | sqltypes.Boolean]
        A boolean value representing the result of the Tanimoto similarity operation.
    """

    def __init__(
        self,
        fp_1: RdkitSparseFingerprint | RdkitBitFingerprint,
        fp_2: RdkitSparseFingerprint | RdkitBitFingerprint,
    ):
        super().__init__(fp_1, fp_2)


class xqmol_in(GenericFunction):
    """
    Internal function: Constructs a query molecule from an input string.


    Parameters
    ----------
    arg_1: CString  The string representation of the query molecule (e.g., SMILES, SMARTS, or CTAB).


    Returns
    -------
    Function[RdkitXQMol]
        A query molecule (RdkitXQMol) object.
    """

    def __init__(self, arg_1: CString):
        super().__init__(arg_1)


class xqmol_out(GenericFunction):
    """
    Internal function used to retrieve the string representation of an `RdkitXQMol` object.


    Parameters
    ----------
    arg_1: RdkitXQMol  The RDKit query molecule to convert to a string.


    Returns
    -------
    Function[CString]
        TODO
    """

    def __init__(self, arg_1: RdkitXQMol):
        super().__init__(arg_1)
