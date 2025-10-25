"""Auto-generated from `data/rdkit/functions.json`. Do not edit manually.
This file defines public RDKit PostgreSQL function wrappers for use with SQLAlchemy.
"""

from typing import Any

from sqlalchemy import BinaryExpression, Function
from sqlalchemy import types as sqltypes
from sqlalchemy.sql import cast, func
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.expression import Cast
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


def mol_has_substructure(
    mol_column: ColumnElement[RdkitMol], query: str
) -> BinaryExpression:
    """
    Perform substructure search.

    Checks if the molecular structure in the column contains the query
    substructure using the `@>` operator.

    Parameters
    ----------
    mol_column : ColumnElement[molalchemy.rdkit.types.RdkitMol]
        The database column containing the molecular structure to search.
    query : str
        The query substructure as a string (SMILES, SMARTS, or other format).

    Returns
    -------
    BinaryExpression
        SQLAlchemy binary expression for the substructure search.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> query = select(Molecule).where(has_substructure(Molecule.structure, "C=O"))
    """
    return mol_column.op("@>")(query)


def rxn_has_smarts(rxn_column: ColumnElement, pattern: str) -> Function[bool]:
    """
    Perform reaction substructure search.

    Checks if the reaction in the column contains the query pattern
    using the `substruct` PostgreSQL function. This searches for
    reaction substructures within stored reactions.

    Parameters
    ----------
    rxn_column : ColumnElement
        The database column containing the reaction to search in.
    pattern : str
        The reaction SMARTS pattern to search for. Can represent
        partial reaction patterns or transformations.

    Returns
    -------
    Function[bool]
        SQLAlchemy function, that returns `True` if the pattern
        is found in the reaction, `False` otherwise.

    Examples
    --------
    >>> from sqlalchemy import select
    >>> # Search for reactions containing a carbonyl formation
    >>> query = select(Reaction).where(has_smarts(Reaction.rxn, ">>C=O"))
    """
    return func.substruct(rxn_column, reaction_from_smarts(cast(pattern, CString)))


class add(GenericFunction):
    type = RdkitSparseFingerprint()
    inherit_cache = True

    def __init__(
        self, fp_1: RdkitSparseFingerprint, fp_2: RdkitSparseFingerprint, **kwargs: Any
    ) -> None:
        """Calls the rdkit cartridge function `add`.

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
        Function[RdkitSparseFingerprint]
            An sfp formed by the element-wise addition of the two sfp arguments.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class all_values_gt(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, fp: RdkitSparseFingerprint, value: int | sqltypes.Integer, **kwargs: Any
    ) -> None:
        """Returns a boolean indicating whether or not all elements of the sfp argument are greater than the int argument.

        Parameters
        ----------
        fp
            The sparse fingerprint to check.
        value
            The integer value to compare against.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean indicating whether or not all elements of the sfp argument are greater than the int argument.
        """
        super().__init__(fp, value, **kwargs)


class all_values_lt(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, fp: RdkitSparseFingerprint, value: int | sqltypes.Integer, **kwargs: Any
    ) -> None:
        """Returns a boolean indicating whether or not all elements of the sfp argument are less than the int argument.

        Parameters
        ----------
        fp
            The sparse fingerprint (sfp) to check.
        value
            The integer value to compare against the sfp elements.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean indicating whether or not all elements of the sfp argument are less than the int argument.
        """
        super().__init__(fp, value, **kwargs)


class atompair_fp(GenericFunction):
    type = RdkitSparseFingerprint()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns an sfp which is the count-based atom-pair fingerprint for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to generate the fingerprint.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitSparseFingerprint]
            The count-based atom-pair fingerprint (sfp) for the molecule.
        """
        super().__init__(mol, **kwargs)


class atompairbv_fp(GenericFunction):
    type = RdkitBitFingerprint()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns a bit vector atom-pair fingerprint for a molecule.

        Parameters
        ----------
        mol
            The molecule to compute the fingerprint for.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitBitFingerprint]
            A bit vector atom-pair fingerprint.
        """
        super().__init__(mol, **kwargs)


class avalon_fp(GenericFunction):
    type = RdkitBitFingerprint()
    inherit_cache = True

    def __init__(
        self,
        mol: RdkitMol,
        arg_2: sqltypes.Boolean,
        arg_3: int | sqltypes.Integer,
        **kwargs: Any,
    ) -> None:
        """Generates Avalon fingerprints for a molecule.

        Parameters
        ----------
        mol
            The RDKit molecule for which to generate the fingerprint.
        arg_2
            TODO
        arg_3
            TODO
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitBitFingerprint]
            A bit vector fingerprint (bfp).
        """
        super().__init__(mol, arg_2, arg_3, **kwargs)


class bfp_from_binary_text(GenericFunction):
    type = RdkitBitFingerprint()
    inherit_cache = True

    def __init__(self, input: sqltypes.LargeBinary, **kwargs: Any) -> None:
        """Constructs a bit vector fingerprint (bfp) from a binary string representation of the fingerprint.

        Parameters
        ----------
        input
            The binary string representation of the fingerprint.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitBitFingerprint]
            A bit vector fingerprint (bfp).
        """
        super().__init__(input, **kwargs)


class bfp_le(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, fp_1: RdkitBitFingerprint, fp_2: RdkitBitFingerprint, **kwargs: Any
    ) -> None:
        """Returns whether the first bit fingerprint is less than or equal to the second bit fingerprint. Used for operator overloading.

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
            True if the first bit fingerprint is less than or equal to the second bit fingerprint, False otherwise.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class bfp_to_binary_text(GenericFunction):
    type = sqltypes.LargeBinary()
    inherit_cache = True

    def __init__(self, fp: RdkitBitFingerprint, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `bfp_to_binary_text`.

        Parameters
        ----------
        fp
            The bit vector fingerprint (bfp) to convert.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.LargeBinary]
            A bytea with the binary string representation of the fingerprint.
        """
        super().__init__(fp, **kwargs)


class dice_dist(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(
        self, fp_1: RdkitBitFingerprint, fp_2: RdkitBitFingerprint, **kwargs: Any
    ) -> None:
        """Returns the Dice distance between two fingerprints of the same type (either two sfp or two bfp values).

        Parameters
        ----------
        fp_1
            The first fingerprint (bfp) for the distance calculation.
        fp_2
            The second fingerprint (bfp) for the distance calculation.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Dice distance (float) between the two fingerprints.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class dice_sml(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(
        self,
        fp_1: RdkitSparseFingerprint | RdkitBitFingerprint,
        fp_2: RdkitSparseFingerprint | RdkitBitFingerprint,
        **kwargs: Any,
    ) -> None:
        """Returns the Dice similarity between two fingerprints of the same type (either two sparse fingerprints or two bit vector fingerprints).

        Parameters
        ----------
        fp_1
            The first fingerprint (either sparse or bit vector) for comparison.
        fp_2
            The second fingerprint (either sparse or bit vector) for comparison.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Dice similarity between the two fingerprints.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class dice_sml_op(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self,
        arg_1: RdkitSparseFingerprint | RdkitBitFingerprint,
        arg_2: RdkitSparseFingerprint | RdkitBitFingerprint,
        **kwargs: Any,
    ) -> None:
        """Returns the Dice similarity between two fingerprints of the same type (either two sfp or two bfp values).

        Parameters
        ----------
        arg_1
            The first fingerprint.
        arg_2
            The second fingerprint of the same type as the first.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            The Dice similarity between the two fingerprints.
        """
        super().__init__(arg_1, arg_2, **kwargs)


class featmorgan_fp(GenericFunction):
    type = RdkitSparseFingerprint()
    inherit_cache = True

    def __init__(
        self, mol: RdkitMol, radius: int | sqltypes.Integer = 2, **kwargs: Any
    ) -> None:
        """Returns a count-based Morgan fingerprint for a molecule using chemical-feature invariants. This is an FCFP-like fingerprint.

        Parameters
        ----------
        mol
            The molecule for which to generate the fingerprint.
        radius
            The radius for the fingerprint generation. This argument is optional and defaults to 2.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitSparseFingerprint]
            The count-based Morgan fingerprint (sfp) for the molecule.
        """
        super().__init__(mol, radius, **kwargs)


class featmorganbv_fp(GenericFunction):
    type = RdkitBitFingerprint()
    inherit_cache = True

    def __init__(
        self, mol: RdkitMol, radius: int | sqltypes.Integer = 2, **kwargs: Any
    ) -> None:
        """Returns a bit vector Morgan fingerprint for a molecule using chemical-feature invariants. The second argument provides the radius. This is an FCFP-like fingerprint.

        Parameters
        ----------
        mol
            The molecule for which to generate the fingerprint.
        radius
            The radius for the fingerprint generation.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitBitFingerprint]
            The bit vector Morgan fingerprint.
        """
        super().__init__(mol, radius, **kwargs)


class fmcs(GenericFunction):
    type = sqltypes.Text()
    inherit_cache = True

    def __init__(self, mols: RdkitMol | sqltypes.Text, **kwargs: Any) -> None:
        """An aggregation function that calculates the Maximum Common Substructure (MCS) for a set of molecules.

        Parameters
        ----------
        mols
            A set of molecules for which to calculate the MCS.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Text]
            The Maximum Common Substructure (MCS) as a string representation.
        """
        super().__init__(mols, **kwargs)


class fmcs_smiles(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(
        self,
        molecules: sqltypes.Text | CString | Cast[Any],
        json: sqltypes.Text | CString | Cast[Any] | str = "",
        **kwargs: Any,
    ) -> None:
        """Calculates the Maximum Common Substructure (MCS) for a space-separated set of SMILES.

        Parameters
        ----------
        molecules
            A space-separated string of SMILES representations of molecules for which to calculate the MCS.
        json
            An optional JSON string used to provide parameters to the MCS code.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            The Maximum Common Substructure (MCS) for the set of molecules, returned as a SMILES string.
        """
        super().__init__(molecules, json, **kwargs)


class is_valid_ctab(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(self, input: CString, **kwargs: Any) -> None:
        """Returns whether or not a CTAB (mol block) string produces a valid RDKit molecule.

        Parameters
        ----------
        input
            The CTAB (mol block) string to validate.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean indicating whether or not the CTAB string produces a valid RDKit molecule.
        """
        super().__init__(input, **kwargs)


class is_valid_mol_pkl(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(self, input: sqltypes.LargeBinary, **kwargs: Any) -> None:
        """Returns whether or not a binary string (bytea) can be converted into a valid RDKit molecule.

        Parameters
        ----------
        input
            A binary string (bytea) representing a molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean indicating whether or not the binary string can be converted into a valid RDKit molecule.
        """
        super().__init__(input, **kwargs)


class is_valid_smarts(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(self, input: CString, **kwargs: Any) -> None:
        """Returns whether or not a SMARTS string produces a valid RDKit molecule.

        Parameters
        ----------
        input
            The SMARTS string to validate.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean indicating whether the SMARTS string produces a valid RDKit molecule.
        """
        super().__init__(input, **kwargs)


class is_valid_smiles(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(self, input: CString, **kwargs: Any) -> None:
        """Returns whether or not a SMILES string produces a valid RDKit molecule.

        Parameters
        ----------
        input
            The SMILES string to validate.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean indicating whether the SMILES string produces a valid RDKit molecule.
        """
        super().__init__(input, **kwargs)


class layered_fp(GenericFunction):
    type = RdkitBitFingerprint()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns a bit vector which is the layered fingerprint for a molecule. This is an experimental substructure fingerprint using hashed molecular subgraphs.

        Parameters
        ----------
        mol
            The molecule for which to generate the layered fingerprint.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitBitFingerprint]
            The layered fingerprint (bit vector) for the molecule.
        """
        super().__init__(mol, **kwargs)


class maccs_fp(GenericFunction):
    type = RdkitBitFingerprint()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns a bit vector which is the MACCS fingerprint for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to generate the MACCS fingerprint.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitBitFingerprint]
            A bit vector (bfp) representing the MACCS fingerprint.
        """
        super().__init__(mol, **kwargs)


class mol_adjust_query_properties(GenericFunction):
    type = RdkitMol()
    inherit_cache = True

    def __init__(
        self,
        mol: RdkitMol | RdkitQMol,
        query_parameters: CString | Cast[Any] = cast("", CString),
        **kwargs: Any,
    ) -> None:
        """Returns a new molecule with additional query information attached.

        Parameters
        ----------
        mol
            The molecule to which additional query information will be attached.
        query_parameters
            A string with additional query parameters (optional)
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitQMol | RdkitMol]
            A new molecule with additional query information attached.
        """
        super().__init__(mol, query_parameters, **kwargs)


class mol_amw(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the AMW for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the AMW.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The AMW (Average Molecular Weight) for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_chi0n(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the Chi0n value for a molecule.

        Parameters
        ----------
        mol
            The RDKit molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Chi0n value for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_chi0v(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the Chi0v value for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the Chi0v value.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Chi0v value for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_chi1n(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, arg_1: RdkitMol, **kwargs: Any) -> None:
        """Returns the Chi1n value for a molecule.

        Parameters
        ----------
        arg_1
            The molecule for which to calculate the Chi1n value.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Chi1n value of the molecule.
        """
        super().__init__(arg_1, **kwargs)


class mol_chi1v(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the Chi1v value for a molecule.

        Parameters
        ----------
        mol
            The RDKit molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Chi1v value for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_chi2n(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the Chi2n value for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the Chi2n value.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Chi2n value for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_chi2v(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the Chi2v value for a molecule.

        Parameters
        ----------
        mol
            The RDKit molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Chi2v value for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_chi3n(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the Chi3n value for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the Chi3n value.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Chi3n value for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_chi3v(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the Chi3v value for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the Chi3v value.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Chi3v value for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_chi4n(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the Chi4n value for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the Chi4n value.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Chi4n value for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_chi4v(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the Chi4v value for a molecule.

        Parameters
        ----------
        mol
            The molecule to calculate the Chi4v value for.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Chi4v value for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_exactmw(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the exact molecular weight for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the exact molecular weight.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The exact molecular weight of the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_formula(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(
        self,
        mol: RdkitMol,
        include_isotopes: bool | sqltypes.Boolean = False,
        use_deuterium_tritium_symbols: bool | sqltypes.Boolean = True,
        **kwargs: Any,
    ) -> None:
        """Returns a string with the molecular formula for a molecule. The second argument controls whether isotope information is included in the formula; the third argument controls whether "D" and "T" are used instead of [2H] and [3H].

        Parameters
        ----------
        mol
            The molecule for which to get the molecular formula.
        include_isotopes
            Controls whether isotope information is included in the formula.
        use_deuterium_tritium_symbols
            Controls whether "D" and "T" are used instead of [2H] and [3H].
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            A string containing the molecular formula.
        """
        super().__init__(mol, include_isotopes, use_deuterium_tritium_symbols, **kwargs)


class mol_fractioncsp3(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the fraction of carbons that are sp3 hybridized in a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the fraction of sp3 hybridized carbons.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The fraction of carbons that are sp3 hybridized in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_from_ctab(GenericFunction):
    type = RdkitMol()
    inherit_cache = True

    def __init__(self, ctab: CString, arg_2: sqltypes.Boolean, **kwargs: Any) -> None:
        """Returns a molecule object from a CTAB (mol block) string, returning NULL if the molecule construction fails.

        Parameters
        ----------
        ctab
            The CTAB (mol block) string from which to create the molecule.
        arg_2
            A boolean indicating whether the molecule's coordinates should be saved.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitMol]
            An RDKit molecule object, or NULL if the molecule construction fails.
        """
        super().__init__(ctab, arg_2, **kwargs)


class mol_from_json(GenericFunction):
    type = RdkitMol()
    inherit_cache = True

    def __init__(self, json_str: CString, **kwargs: Any) -> None:
        """Returns a molecule for a commonchem JSON string, NULL if the molecule construction fails.

        Parameters
        ----------
        json_str
            A commonchem JSON string representing a molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitMol]
            A molecule for a commonchem JSON string, NULL if the molecule construction fails.
        """
        super().__init__(json_str, **kwargs)


class mol_from_pkl(GenericFunction):
    type = RdkitMol()
    inherit_cache = True

    def __init__(self, bytea: sqltypes.LargeBinary, **kwargs: Any) -> None:
        """Returns a molecule for a binary string (bytea), NULL if the molecule construction fails.

        Parameters
        ----------
        bytea
            A binary string representation of the molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitMol]
            A molecule, or NULL if the molecule construction fails.
        """
        super().__init__(bytea, **kwargs)


class mol_from_smiles(GenericFunction):
    type = RdkitMol()
    inherit_cache = True

    def __init__(self, smiles: sqltypes.Text | CString, **kwargs: Any) -> None:
        """Returns a molecule for a SMILES string, NULL if the molecule construction fails.

        Parameters
        ----------
        smiles
            The SMILES string to convert to a molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitMol]
            A molecule object, or NULL if the molecule construction from the SMILES string fails.
        """
        super().__init__(smiles, **kwargs)


class mol_hallkieralpha(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the Hall-Kier alpha value for a molecule.

        Parameters
        ----------
        mol
            The RDKit molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Hall-Kier alpha value for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_hba(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `mol_hba`.

        Parameters
        ----------
        mol
            The molecule for which to calculate the number of Lipinski H-bond acceptors.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of Lipinski H-bond acceptors (i.e., number of Os and Ns) for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_hbd(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of Lipinski H-bond donors (i.e. number of Os and Ns that have at least one H) for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the number of Lipinski H-bond donors.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of Lipinski H-bond donors for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_inchi(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, arg_2: CString, **kwargs: Any) -> None:
        """Returns an InChI (International Chemical Identifier) for the given molecule. This function requires that the RDKit be built with InChI support.

        Parameters
        ----------
        mol
            The RDKit molecule for which to generate the InChI.
        arg_2
            Additional parameters to pass to the generator (TODO)
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            The InChI string representation of the molecule.
        """
        super().__init__(mol, arg_2, **kwargs)


class mol_inchikey(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, arg_2: CString, **kwargs: Any) -> None:
        """Returns an InChI key for the molecule. Requires RDKit to be built with InChI support.

        Parameters
        ----------
        mol
            The RDKit molecule for which to generate the InChI key.
        arg_2
            Additional parameters to pass to the generator  (TODO)
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            An InChI key for the molecule.
        """
        super().__init__(mol, arg_2, **kwargs)


class mol_kappa1(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the kappa1 value for a molecule.

        Parameters
        ----------
        mol
            The RDKit molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The kappa1 value for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_kappa2(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the kappa2 value for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the kappa2 value.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The kappa2 value.
        """
        super().__init__(mol, **kwargs)


class mol_kappa3(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol_1: RdkitMol, **kwargs: Any) -> None:
        """Returns the kappa3 value for a molecule.

        Parameters
        ----------
        mol_1
            The molecule for which to calculate the kappa3 value.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The kappa3 value for the molecule.
        """
        super().__init__(mol_1, **kwargs)


class mol_labuteasa(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns Labute's approximate surface area (ASA) for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate Labute's approximate surface area.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            Labute's approximate surface area (ASA) for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_logp(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the MolLogP for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the MolLogP.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The MolLogP value for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_murckoscaffold(GenericFunction):
    type = RdkitMol()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the Murcko scaffold for a molecule. The Murcko scaffold consists of all ring systems and the atoms connecting them.

        Parameters
        ----------
        mol
            The RDKit molecule for which to compute the Murcko scaffold.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitMol]
            The RDKit molecule representing the Murcko scaffold.
        """
        super().__init__(mol, **kwargs)


class mol_nm_hash(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(
        self,
        mol: RdkitMol,
        hash_type: CString | Cast[Any] = cast("AnonymousGraph", CString),
        **kwargs: Any,
    ) -> None:
        """Returns a string with a hash for the molecule.

        Parameters
        ----------
        mol
            The molecule for which to generate the hash.
        hash_type
            The type of hash to generate. Legal values are 'AnonymousGraph', 'ElementGraph', 'CanonicalSmiles', 'MurckoScaffold', 'ExtendedMurcko', 'MolFormula', 'AtomBondCounts', 'DegreeVector', 'Mesomer', 'HetAtomTautomer', 'HetAtomProtomer', 'RedoxPair', 'Regioisomer', 'NetCharge', 'SmallWorldIndexBR', 'SmallWorldIndexBRL', 'ArthorSubstructureOrder'. The default is 'AnonymousGraph'.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            A string with the hash for the molecule.
        """
        super().__init__(mol, hash_type, **kwargs)


class mol_numaliphaticcarbocycles(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of aliphatic (at least one non-aromatic bond) carbocycles in a molecule.

        Parameters
        ----------
        mol
            The molecule to analyze.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of aliphatic (at least one non-aromatic bond) carbocycles in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numaliphaticheterocycles(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of aliphatic (at least one non-aromatic bond) heterocycles in a molecule.

        Parameters
        ----------
        mol
            The RDKit molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of aliphatic (at least one non-aromatic bond) heterocycles in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numaliphaticrings(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of aliphatic (at least one non-aromatic bond) rings in a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the number of aliphatic rings.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of aliphatic (at least one non-aromatic bond) rings in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numamidebonds(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of amide bonds in a molecule.

        Parameters
        ----------
        mol
            The RDKit molecule for which to calculate the number of amide bonds.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of amide bonds in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numaromaticcarbocycles(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `mol_numaromaticcarbocycles`.

        Parameters
        ----------
        mol
            The RDKit molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of aromatic carbocycles in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numaromaticheterocycles(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of aromatic heterocycles in a molecule.

        Parameters
        ----------
        mol
            The RDKit molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of aromatic heterocycles in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numaromaticrings(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of aromatic rings in a molecule.

        Parameters
        ----------
        mol
            The molecule to analyze.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of aromatic rings in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numatoms(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the total number of atoms in a molecule.

        Parameters
        ----------
        mol
            The RDKit molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The total number of atoms in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numbridgeheadatoms(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of bridgehead atoms in a molecule.

        Parameters
        ----------
        mol
            The molecule to calculate the number of bridgehead atoms for.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of bridgehead atoms in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numheavyatoms(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of heavy atoms in a molecule.

        Parameters
        ----------
        mol
            The molecule to analyze.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of heavy atoms in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numheteroatoms(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of heteroatoms in a molecule.

        Parameters
        ----------
        mol
            The RDKit molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of heteroatoms in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numheterocycles(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of heterocycles in a molecule.

        Parameters
        ----------
        mol
            The molecule for which to count the number of heteroatoms.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of heteroatoms in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numrings(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of rings in a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the number of rings.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of rings in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numrotatablebonds(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of rotatable bonds in a molecule.

        Parameters
        ----------
        mol
            The molecule to calculate the number of rotatable bonds for.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of rotatable bonds in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numsaturatedcarbocycles(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of saturated carbocycles in a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the number of saturated carbocycles.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of saturated carbocycles in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numsaturatedheterocycles(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of saturated heterocycles in a molecule.

        Parameters
        ----------
        mol
            The molecule to analyze.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of saturated heterocycles in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numsaturatedrings(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of saturated rings in a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the number of saturated rings.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of saturated rings in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_numspiroatoms(GenericFunction):
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the number of spiro atoms in a molecule.

        Parameters
        ----------
        mol
            The RDKit molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of spiro atoms in the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_phi(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the Kier Phi value for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the Kier Phi value.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Kier Phi value for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_send(GenericFunction):
    type = sqltypes.LargeBinary()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Serializes an RDKit molecule into a binary string representation.

        Parameters
        ----------
        mol
            The RDKit molecule to be serialized.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.LargeBinary]
            A binary string (bytea) representation of the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_to_ctab(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(
        self,
        mol: RdkitMol,
        arg_2: sqltypes.Boolean | bool = True,
        arg_3: sqltypes.Boolean | bool = False,
        **kwargs: Any,
    ) -> None:
        """Returns a CTAB (mol block) string for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to generate the CTAB string.
        arg_2
        arg_3
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            A CTAB (mol block) string for a molecule.
        """
        super().__init__(mol, arg_2, arg_3, **kwargs)


class mol_to_cxsmarts(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(self, mol: RdkitMol | RdkitQMol, **kwargs: Any) -> None:
        """Returns the CXSMARTS for a molecule.

        Parameters
        ----------
        mol
            The molecule to convert to CXSMARTS.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            The CXSMARTS string for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_to_cxsmiles(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the CXSMILES for a molecule.

        Parameters
        ----------
        mol
            The molecule to convert.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            The CXSMILES string for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_to_json(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(self, mol: RdkitMol | RdkitQMol, **kwargs: Any) -> None:
        """Returns the commonchem JSON for a molecule. (*available from the 2021_09 release*)

        Parameters
        ----------
        mol
            The molecule to convert to commonchem JSON.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            The commonchem JSON string representation of the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_to_pkl(GenericFunction):
    type = sqltypes.LargeBinary()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns a binary string (bytea) for a molecule. This function is available from the Q3 2012 (2012_09) release.

        Parameters
        ----------
        mol
            The RDKit molecule to be converted to a binary string.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.LargeBinary]
            A binary string (bytea) representation of the RDKit molecule.
        """
        super().__init__(mol, **kwargs)


class mol_to_smarts(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(self, mol: RdkitMol | RdkitQMol, **kwargs: Any) -> None:
        """Returns the SMARTS string for a molecule.

        Parameters
        ----------
        mol
            The molecule to convert to a SMARTS string.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            The SMARTS string representation of the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_to_smiles(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(self, mol: RdkitMol | RdkitQMol, **kwargs: Any) -> None:
        """Returns a canonical SMILES string for a molecule.

        Parameters
        ----------
        mol
            The molecule to convert to SMILES.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            The canonical SMILES string for the molecule.
        """
        super().__init__(mol, **kwargs)


class mol_to_svg(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(
        self,
        mol: RdkitMol | RdkitQMol,
        arg_2: CString | Cast[Any] = cast("", CString),
        width: int | sqltypes.Integer = 250,
        height: int | sqltypes.Integer = 200,
        arg_5: CString | Cast[Any] = cast("", CString),
        **kwargs: Any,
    ) -> None:
        """Returns an SVG with a drawing of the molecule. This function is available from the 2016_09 release.

        Parameters
        ----------
        mol
            The molecule to be drawn.
        arg_2
            An optional string to use as the legend for the drawing.
        width
            The optional width of the generated SVG image.
        height
            The optional height of the generated SVG image.
        arg_5
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            An SVG string representing the drawing of the molecule.
        """
        super().__init__(mol, arg_2, width, height, arg_5, **kwargs)


class mol_to_v3kctab(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(
        self,
        mol: RdkitMol,
        create_depiction: sqltypes.Boolean | bool = True,
        **kwargs: Any,
    ) -> None:
        """Returns a CTAB (mol block) string for a molecule. The optional second argument controls whether or not 2D coordinates will be generated for molecules that don’t have coordinates.

        Parameters
        ----------
        mol
            The molecule to convert to a V3000 CTAB string.
        create_depiction
            Controls whether or not 2D coordinates will be generated for molecules that don't have coordinates.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            A CTAB (mol block) string for the molecule.
        """
        super().__init__(mol, create_depiction, **kwargs)


class mol_to_xqmol(GenericFunction):
    type = RdkitXQMol()
    inherit_cache = True

    def __init__(
        self,
        arg_1: RdkitMol,
        arg_2: sqltypes.Boolean,
        arg_3: sqltypes.Boolean,
        arg_4: sqltypes.Boolean,
        arg_5: CString,
        **kwargs: Any,
    ) -> None:
        """Converts an RDKit molecule to an RDKit XQuery molecule. TODO: add docs

        Parameters
        ----------
        arg_1
            The RDKit molecule to be converted.
        arg_2
            A boolean parameter for the conversion process.
        arg_3
            Another boolean parameter for the conversion process.
        arg_4
            A third boolean parameter for the conversion process.
        arg_5
            A string parameter for the conversion process.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitXQMol]
            The RDKit XQuery molecule.
        """
        super().__init__(arg_1, arg_2, arg_3, arg_4, arg_5, **kwargs)


class mol_tpsa(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns the topological polar surface area for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to calculate the topological polar surface area.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The topological polar surface area of the molecule.
        """
        super().__init__(mol, **kwargs)


class morgan_fp(GenericFunction):
    type = RdkitSparseFingerprint()
    inherit_cache = True

    def __init__(
        self, mol: RdkitMol, radius: int | sqltypes.Integer = 2, **kwargs: Any
    ) -> None:
        """Returns a count-based Morgan fingerprint (sfp) for a molecule using connectivity invariants. This is an ECFP-like fingerprint.

        Parameters
        ----------
        mol
            The molecule for which to generate the fingerprint.
        radius
            The radius for the Morgan fingerprint generation. Defaults to 2.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitSparseFingerprint]
            A sparse fingerprint (sfp) which is the count-based Morgan fingerprint.
        """
        super().__init__(mol, radius, **kwargs)


class morganbv_fp(GenericFunction):
    type = RdkitBitFingerprint()
    inherit_cache = True

    def __init__(
        self, mol: RdkitMol, radius: int | sqltypes.Integer = 2, **kwargs: Any
    ) -> None:
        """Returns a bit vector Morgan fingerprint (bfp) for a molecule using connectivity invariants. The second argument provides the radius. This is an ECFP-like fingerprint.

        Parameters
        ----------
        mol
            The molecule for which to generate the fingerprint.
        radius
            The radius for the Morgan fingerprint calculation.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitBitFingerprint]
            A bit vector Morgan fingerprint (bfp) for the molecule.
        """
        super().__init__(mol, radius, **kwargs)


class qmol_from_ctab(GenericFunction):
    type = RdkitQMol()
    inherit_cache = True

    def __init__(
        self, ctab: CString, keep_conformer: sqltypes.Boolean, **kwargs: Any
    ) -> None:
        """Returns a query molecule for a CTAB (mol block) string. TODO: This functions changed between the versions - adding new arg.

        Parameters
        ----------
        ctab
            A CTAB (mol block) string.
        keep_conformer
            Controls whether or not the coordinates are saved.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitQMol]
            A query molecule
        """
        super().__init__(ctab, keep_conformer, **kwargs)


class qmol_from_json(GenericFunction):
    type = RdkitQMol()
    inherit_cache = True

    def __init__(self, json: CString, **kwargs: Any) -> None:
        """Returns a query molecule for a commonchem JSON string.

        Parameters
        ----------
        json
            The commonchem JSON string representing the query molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitQMol]
            A query molecule
        """
        super().__init__(json, **kwargs)


class qmol_from_smarts(GenericFunction):
    type = RdkitQMol()
    inherit_cache = True

    def __init__(self, smarts: CString, **kwargs: Any) -> None:
        """Returns a query molecule for a SMARTS string. Explicit Hs in the SMARTS are converted into query features on the attached atom.

        Parameters
        ----------
        smarts
            The SMARTS string representing the query molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitQMol]
            A query molecule (RdkitQMol) or NULL if the molecule construction fails.
        """
        super().__init__(smarts, **kwargs)


class qmol_from_smiles(GenericFunction):
    type = RdkitQMol()
    inherit_cache = True

    def __init__(self, smiles: CString, **kwargs: Any) -> None:
        """Returns a query molecule for a SMILES string. Explicit Hs in the SMILES are converted into query features on the attached atom.

        Parameters
        ----------
        smiles
            The SMILES string to convert into a query molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitQMol]
            A query molecule for the SMILES string.
        """
        super().__init__(smiles, **kwargs)


class qmol_send(GenericFunction):
    type = sqltypes.LargeBinary()
    inherit_cache = True

    def __init__(self, mol: RdkitQMol, **kwargs: Any) -> None:
        """Returns a binary string (bytea) for a query molecule.

        Parameters
        ----------
        mol
            The query molecule to be converted.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.LargeBinary]
            A binary string representation of the query molecule.
        """
        super().__init__(mol, **kwargs)


class rdkit_fp(GenericFunction):
    type = RdkitBitFingerprint()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns a bit vector fingerprint (bfp) which is the RDKit fingerprint for a molecule. This is a daylight-inspired fingerprint using hashed molecular subgraphs.

        Parameters
        ----------
        mol
            The molecule for which to generate the fingerprint.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitBitFingerprint]
            A bit vector fingerprint (bfp) representing the RDKit fingerprint.
        """
        super().__init__(mol, **kwargs)


class rdkit_toolkit_version(GenericFunction):
    type = sqltypes.Text()
    inherit_cache = True

    def __init__(self, **kwargs: Any) -> None:
        """Returns the version of the RDKit toolkit being used.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Text]
            The version of the RDKit toolkit as a string.
        """
        super().__init__(**kwargs)


class rdkit_version(GenericFunction):
    type = sqltypes.Text()
    inherit_cache = True

    def __init__(self, **kwargs: Any) -> None:
        """Returns the RDKit cartridge version.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Text]
            Returns the RDKit version as text.
        """
        super().__init__(**kwargs)


class reaction_difference_fp(GenericFunction):
    type = RdkitSparseFingerprint()
    inherit_cache = True

    def __init__(
        self, rxn_1: RdkitReaction, fp_type: int | sqltypes.Integer, **kwargs: Any
    ) -> None:
        """Calculates a sparse fingerprint representing the difference between reactants and products in an RDKit reaction.

        Parameters
        ----------
        rxn_1
            The RDKit reaction object.
        fp_type
            Integer denoting the fingerprint type. Likely 1 (AtomPairFP), 2 (TopologicalTorsionFP), or 3 (MorganFP).
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitSparseFingerprint]
            A sparse fingerprint (sfp) representing the reaction difference.
        """
        super().__init__(rxn_1, fp_type, **kwargs)


class reaction_from_ctab(GenericFunction):
    type = RdkitReaction()
    inherit_cache = True

    def __init__(self, rxn_str: CString, **kwargs: Any) -> None:
        """Returns a reaction for a CTAB (reaction block) string.

        Parameters
        ----------
        rxn_str
            The CTAB (reaction block) string representing the reaction.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitReaction]
            An RDKit reaction object, or NULL if the reaction construction fails.
        """
        super().__init__(rxn_str, **kwargs)


class reaction_from_smarts(GenericFunction):
    type = RdkitReaction()
    inherit_cache = True

    def __init__(self, rxn_str: CString | Cast[Any], **kwargs: Any) -> None:
        """Returns a reaction object for a SMARTS string.

        Parameters
        ----------
        rxn_str
            The SMARTS string representing the reaction.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitReaction]
            The RDKit reaction object.
        """
        super().__init__(rxn_str, **kwargs)


class reaction_from_smiles(GenericFunction):
    type = RdkitReaction()
    inherit_cache = True

    def __init__(self, rxn_str: CString, **kwargs: Any) -> None:
        """Returns a reaction object for a reaction SMILES string. Returns NULL if the reaction construction fails.

        Parameters
        ----------
        rxn_str
            The reaction SMILES string to convert into an RDKit reaction object.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitReaction]
            An RDKit reaction object, or NULL if the conversion from the reaction SMILES string fails.
        """
        super().__init__(rxn_str, **kwargs)


class reaction_numagents(GenericFunction):
    inherit_cache = True

    def __init__(self, rxn: RdkitReaction, **kwargs: Any) -> None:
        """Returns the number of agents in an RDKit reaction.

        Parameters
        ----------
        rxn
            The RDKit reaction molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of agents in the RDKit reaction.
        """
        super().__init__(rxn, **kwargs)


class reaction_numproducts(GenericFunction):
    inherit_cache = True

    def __init__(self, rxn: RdkitReaction, **kwargs: Any) -> None:
        """Returns the number of products in an RDKit reaction.

        Parameters
        ----------
        rxn
            The RDKit reaction object.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of products in the reaction.
        """
        super().__init__(rxn, **kwargs)


class reaction_numreactants(GenericFunction):
    inherit_cache = True

    def __init__(self, rxn: RdkitReaction, **kwargs: Any) -> None:
        """Returns the number of reactants in an RDKit reaction.

        Parameters
        ----------
        rxn
            The RDKit reaction object.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of reactants in the RDKit reaction.
        """
        super().__init__(rxn, **kwargs)


class reaction_send(GenericFunction):
    type = sqltypes.LargeBinary()
    inherit_cache = True

    def __init__(self, rxn: RdkitReaction, **kwargs: Any) -> None:
        """Serializes an RDKit reaction into a binary representation.

        Parameters
        ----------
        rxn
            The RDKit reaction object to be sent.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.LargeBinary]
            The binary representation of the RDKit reaction.
        """
        super().__init__(rxn, **kwargs)


class reaction_structural_bfp(GenericFunction):
    type = RdkitBitFingerprint()
    inherit_cache = True

    def __init__(
        self, rxn: RdkitReaction, radius: int | sqltypes.Integer, **kwargs: Any
    ) -> None:
        """Returns a bit vector fingerprint (bfp) representing the structural features of a chemical reaction. The second argument provides the radius for the fingerprint generation.

        Parameters
        ----------
        rxn
            The RDKit reaction object.
        radius
            The radius to use for the fingerprint generation.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitBitFingerprint]
            A bit vector fingerprint (bfp) representing the structural features of the reaction.
        """
        super().__init__(rxn, radius, **kwargs)


class reaction_to_ctab(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(self, reaction: RdkitReaction, **kwargs: Any) -> None:
        """Returns a CTAB (mol block) string for a reaction.

        Parameters
        ----------
        reaction
            The RDKit reaction object to convert.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            The CTAB (mol block) string representation of the reaction.
        """
        super().__init__(reaction, **kwargs)


class reaction_to_smarts(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(self, rxn: RdkitReaction, **kwargs: Any) -> None:
        """Returns the SMARTS string for a reaction.

        Parameters
        ----------
        rxn
            The RDKit reaction object to convert.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            The SMARTS string representation of the reaction.
        """
        super().__init__(rxn, **kwargs)


class reaction_to_smiles(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(self, rxn: RdkitReaction, **kwargs: Any) -> None:
        """Returns the SMILES string for a reaction.

        Parameters
        ----------
        rxn
            The RDKit reaction object.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            The SMILES string representation of the reaction.
        """
        super().__init__(rxn, **kwargs)


class reaction_to_svg(GenericFunction):
    type = CString()
    inherit_cache = True

    def __init__(
        self,
        rxn: RdkitReaction,
        highlight_reactants: sqltypes.Boolean,
        width: int | sqltypes.Integer,
        height: int | sqltypes.Integer,
        params: CString,
        **kwargs: Any,
    ) -> None:
        """Returns an SVG (Scalable Vector Graphics) drawing of the provided RDKit reaction. This function is quite slow

        Parameters
        ----------
        rxn
            The RDKit reaction object to be drawn.
        highlight_reactants
            If true, highlights the reactants in the SVG drawing.
        width
            The desired width of the SVG image.
        height
            The desired height of the SVG image.
        params
            An optional string for other drawing parameters? [TODO]
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            A string containing the SVG representation of the reaction.
        """
        super().__init__(rxn, highlight_reactants, width, height, params, **kwargs)


class rsubstruct(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self,
        mol: RdkitQMol | RdkitMol | RdkitXQMol | RdkitReaction,
        query: RdkitMol | RdkitReaction,
        **kwargs: Any,
    ) -> None:
        """Returns whether or not the second molecule (or reaction) is a substructure of the first molecule (or query molecule/reaction). Doesn't use chirality in the matching.

        Parameters
        ----------
        mol
            The molecule (or query molecule/reaction) to be searched within.
        query
            The molecule (or reaction) to check as a substructure.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean indicating whether the second molecule (`arg_2`) is a substructure of the first molecule (`arg_1`).
        """
        super().__init__(mol, query, **kwargs)


class rsubstruct_chiral(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, query_mol: RdkitMol, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `rsubstruct_chiral`. This function returns whether or not the second molecule is a substructure of the first, considering chirality.

        Parameters
        ----------
        mol
            The molecule to search within.
        query_mol
            The molecule to search for as a substructure.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean indicating whether the second molecule is a chiral substructure of the first.
        """
        super().__init__(mol, query_mol, **kwargs)


class rsubstruct_query(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, mol_1: RdkitMol | RdkitXQMol | RdkitQMol, mol_2: RdkitMol, **kwargs: Any
    ) -> None:
        """Returns whether or not the second molecule is a substructure of the first molecule. Doesn't use chirality in the matching.

        Parameters
        ----------
        mol_1
            The molecule to be searched within.
        mol_2
            The substructure molecule to search for.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean indicating whether the second molecule is a substructure of the first.
        """
        super().__init__(mol_1, mol_2, **kwargs)


class rsubstructfp(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, rxn_1: RdkitReaction, rxn_2: RdkitReaction, **kwargs: Any
    ) -> None:
        """Returns whether or not the second RDKit reaction is a substructure of the first.

        Parameters
        ----------
        rxn_1
            The first RDKit reaction.
        rxn_2
            The second RDKit reaction, which is checked as a substructure.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            `True` if the second reaction is a substructure of the first, `False` otherwise.
        """
        super().__init__(rxn_1, rxn_2, **kwargs)


class size(GenericFunction):
    inherit_cache = True

    def __init__(self, bfp: RdkitBitFingerprint, **kwargs: Any) -> None:
        """Returns the length of (number of bits in) a bit vector fingerprint.

        Parameters
        ----------
        bfp
            The bit vector fingerprint.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The length of (number of bits in) the bit vector fingerprint.
        """
        super().__init__(bfp, **kwargs)


class substruct(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self,
        mol: RdkitMol | RdkitReaction,
        query: RdkitMol | RdkitXQMol | RdkitQMol | RdkitReaction,
        **kwargs: Any,
    ) -> None:
        """Returns whether or not the second molecule/reaction is a substructure of the first one.

        Parameters
        ----------
        mol
            The first molecule.
        query
            The second molecule, which is checked as a substructure of the first.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            True if the second molecule is a substructure of the first, False otherwise.
        """
        super().__init__(mol, query, **kwargs)


class substruct_chiral(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, query: RdkitMol, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `substruct_chiral`.

        Parameters
        ----------
        mol
            The molecule to be searched for the substructure.
        query
            The substructure molecule to search for within the first molecule. Chirality is considered.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean indicating whether the second molecule is a substructure of the first, taking chirality into account.
        """
        super().__init__(mol, query, **kwargs)


class substruct_count(GenericFunction):
    inherit_cache = True

    def __init__(
        self,
        mol: RdkitMol,
        query: RdkitMol | RdkitQMol,
        unique: sqltypes.Boolean | bool = True,
        **kwargs: Any,
    ) -> None:
        """Returns the number of substructure matches between the second molecule and the first. Optionally, the matches can be uniquified.

        Parameters
        ----------
        mol
            The molecule to search within.
        query
            The substructure to search for.
        unique
            Toggles whether or not the matches are uniquified.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The number of substructure matches found.
        """
        super().__init__(mol, query, unique, **kwargs)


class substruct_count_chiral(GenericFunction):
    inherit_cache = True

    def __init__(
        self,
        mol: RdkitMol,
        query: RdkitMol | RdkitQMol,
        unique: sqltypes.Boolean,
        **kwargs: Any,
    ) -> None:
        """Returns the number of chiral substructure matches found between a query molecule and a target molecule. This function considers chirality during the matching process.

        Parameters
        ----------
        mol
            The target RDKit molecule to search within.
        query
            The RDKit molecule or query molecule to search for as a chiral substructure.
        unique
            A boolean flag indicating whether to count only unique chiral substructure matches (true) or all matches (false).
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            The total number of chiral substructure matches found.
        """
        super().__init__(mol, query, unique, **kwargs)


class substruct_query(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, mol_1: RdkitMol, mol_2: RdkitMol | RdkitXQMol | RdkitQMol, **kwargs: Any
    ) -> None:
        """Returns whether or not the second molecule is a substructure of the first molecule.

        Parameters
        ----------
        mol_1
            The molecule to search within.
        mol_2
            The molecule or query molecule to search for as a substructure.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean indicating whether the second molecule is a substructure of the first.
        """
        super().__init__(mol_1, mol_2, **kwargs)


class substructfp(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True

    def __init__(
        self, rxn_1: RdkitReaction, rxn_2: RdkitReaction, **kwargs: Any
    ) -> None:
        """Returns whether or not the second RDKit reaction is a substructure of the first.

        Parameters
        ----------
        rxn_1
            The first RDKit reaction.
        rxn_2
            The second RDKit reaction, which is checked as a substructure of the first.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            A boolean indicating whether the second reaction is a substructure of the first.
        """
        super().__init__(rxn_1, rxn_2, **kwargs)


class subtract(GenericFunction):
    type = RdkitSparseFingerprint()
    inherit_cache = True

    def __init__(
        self, fp_1: RdkitSparseFingerprint, fp_2: RdkitSparseFingerprint, **kwargs: Any
    ) -> None:
        """Returns an sfp formed by the element-wise subtraction of the two sfp arguments.

        Parameters
        ----------
        fp_1
            The first sparse fingerprint (sfp).
        fp_2
            The second sparse fingerprint (sfp) to subtract.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitSparseFingerprint]
            The resulting sparse fingerprint (sfp) after subtraction.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class tanimoto_dist(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(
        self, fp_1: RdkitBitFingerprint, fp_2: RdkitBitFingerprint, **kwargs: Any
    ) -> None:
        """Returns the Tanimoto distance between two bit fingerprints.

        Parameters
        ----------
        fp_1
            The first fingerprint to compare.
        fp_2
            The second fingerprint to compare.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Tanimoto distance between the two fingerprints.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class tanimoto_sml(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(
        self,
        fp_1: RdkitSparseFingerprint | RdkitBitFingerprint,
        fp_2: RdkitSparseFingerprint | RdkitBitFingerprint,
        **kwargs: Any,
    ) -> None:
        """Returns the Tanimoto similarity between two fingerprints of the same type (either two sparse fingerprints or two bit vector fingerprints).

        Parameters
        ----------
        fp_1
            The first fingerprint to compare.
        fp_2
            The second fingerprint to compare.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Tanimoto similarity as a float value.
        """
        super().__init__(fp_1, fp_2, **kwargs)


class torsion_fp(GenericFunction):
    type = RdkitSparseFingerprint()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns a sparse vector topological-torsion fingerprint for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to generate the fingerprint.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitSparseFingerprint]
            A count-based topological-torsion fingerprint (sfp) for the molecule.
        """
        super().__init__(mol, **kwargs)


class torsionbv_fp(GenericFunction):
    type = RdkitBitFingerprint()
    inherit_cache = True

    def __init__(self, mol: RdkitMol, **kwargs: Any) -> None:
        """Returns a bit vector topological-torsion fingerprint for a molecule.

        Parameters
        ----------
        mol
            The molecule for which to generate the fingerprint.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[RdkitBitFingerprint]
            A bit vector (bfp) representing the topological-torsion fingerprint of the molecule.
        """
        super().__init__(mol, **kwargs)


class tversky_sml(GenericFunction):
    type = sqltypes.Float()
    inherit_cache = True

    def __init__(
        self,
        fp_1: RdkitBitFingerprint,
        fp_2: RdkitBitFingerprint,
        alpha: float,
        beta: float,
        **kwargs: Any,
    ) -> None:
        """Returns the Tversky similarity between two bit fingerprints. The third and fourth arguments are the alpha and beta parameters for the Tversky similarity.

        Parameters
        ----------
        fp_1
            The first fingerprint.
        fp_2
            The second fingerprint.
        alpha
            The alpha parameter for the Tversky similarity.
        beta
            The beta parameter for the Tversky similarity.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Float]
            The Tversky similarity between the two fingerprints.
        """
        super().__init__(fp_1, fp_2, alpha, beta, **kwargs)


class xqmol_send(GenericFunction):
    type = sqltypes.LargeBinary()
    inherit_cache = True

    def __init__(self, mol: RdkitXQMol, **kwargs: Any) -> None:
        """Converts `RdkitXQMol` to its binary representation.

        Parameters
        ----------
        mol
            An RDKit extended query molecule.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.LargeBinary]
            SQLAlchemy function
        """
        super().__init__(mol, **kwargs)
