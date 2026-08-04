"""Auto-generated from `data/bingo/functions.json`. Do not edit manually.
This file defines public Bingo PostgreSQL function wrappers for use with SQLAlchemy.
"""

from typing import Any, Literal

from sqlalchemy import types as sqltypes
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.functions import GenericFunction

from molalchemy.bingo.search import _bingo_search_values

from ._types import (
    AnyBingoBinaryMolLike,
    AnyBingoBinaryReactionLike,
    AnyBingoMolLike,
    AnyBingoMolLikeCombined,
    AnyBingoReactionLike,
    AnyBingoReactionLikeCombined,
    TextLike,
)

# Backward compatibility aliases
AnyBingoMol = AnyBingoMolLikeCombined
AnyBingoReaction = AnyBingoReactionLikeCombined


def mol_has_substructure(
    mol: ColumnElement[AnyBingoMol], query: TextLike, parameters: TextLike = ""
) -> ColumnElement[bool]:
    """
    Perform substructure search on a molecule column.

    Parameters
    ----------
    mol : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    query : TextLike
        Query molecule as SMILES, SMARTS, or Molfile string.
    parameters : TextLike, optional
        Search parameters for customizing the matching behavior (default is "").
        Examples: "TAU" for tautomer search, "RES" for resonance search.

    Returns
    -------
    ColumnElement[bool]
        SQLAlchemy expression for substructure matching that can be used in WHERE clauses.

    """
    return _bingo_search_values(mol, (query, parameters), "bingo.sub")


def mol_has_smarts(
    mol: ColumnElement[AnyBingoMol], query: TextLike, parameters: TextLike = ""
) -> ColumnElement[bool]:
    """
    Perform SMARTS pattern matching on a molecule column.

    Parameters
    ----------
    mol : ColumnElement[AnyBingoMol]
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    query : TextLike
        SMARTS pattern string for matching.
    parameters : TextLike, optional
        Search parameters for customizing the matching behavior (default is "").

    Returns
    -------
    ColumnElement[bool]
        SQLAlchemy expression for SMARTS matching that can be used in WHERE clauses.

    """
    return _bingo_search_values(mol, (query, parameters), "bingo.smarts")


def mol_equals(
    mol: ColumnElement[AnyBingoMol], query: TextLike, parameters: TextLike = ""
) -> ColumnElement[bool]:
    """
    Perform exact structure matching on a molecule column.

    Parameters
    ----------
    mol : ColumnElement[AnyBingoMol]
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    query : TextLike
        Query molecule as SMILES or Molfile string for exact matching.
    parameters : TextLike, optional
        Search parameters for customizing the matching behavior (default is "").
        Examples: "TAU" for tautomer matching, "STE" for stereochemistry.

    Returns
    -------
    ColumnElement[bool]
        SQLAlchemy expression for exact matching that can be used in WHERE clauses.

    """
    return _bingo_search_values(mol, (query, parameters), "bingo.exact")


def mol_similarity(
    mol: ColumnElement[AnyBingoMol],
    query: TextLike,
    bottom: float = 0.0,
    top: float = 1.0,
    metric: TextLike = "Tanimoto",
) -> ColumnElement[bool]:
    """
    Perform similarity search on a molecule column. This should be used in WHERE clauses, as it
    returns a boolean expression indicating whether the similarity criteria are met.

    Parameters
    ----------
    mol : AnyBingoMolLike | AnyBingoBinaryMolLike
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    query : TextLike
        Query molecule as SMILES or Molfile string for similarity comparison.
    bottom : float, optional
        Minimum similarity threshold (default is 0.0).
    top : float, optional
        Maximum similarity threshold (default is 1.0).
    metric : TextLike, optional
        Similarity metric to use (default is "Tanimoto").
        Other options include "Dice", "Cosine", etc.

    Returns
    -------
    ColumnElement[bool]
        SQLAlchemy expression for similarity matching that can be used in WHERE clauses.

    """
    return _bingo_search_values(mol, (bottom, top, query, metric), "bingo.sim")


def rxn_has_substructure(
    rxn: ColumnElement[AnyBingoReaction], query: TextLike, parameters: TextLike = ""
) -> ColumnElement[bool]:
    """
    Perform substructure search on a reaction column.

    Parameters
    ----------
    rxn : ColumnElement[AnyBingoReaction]
        SQLAlchemy column containing reaction data (reaction SMILES, RXN, or binary).
    query : TextLike
        Query reaction as reaction SMILES, SMARTS, or RXN string.
    parameters : TextLike, optional
        Search parameters for customizing the matching behavior (default is "").

    Returns
    -------
    ColumnElement[bool]
        SQLAlchemy expression for reaction substructure matching that can be used in WHERE clauses.

    """
    return _bingo_search_values(rxn, (query, parameters), "bingo.rsub")


def rxn_has_smarts(
    rxn: ColumnElement[AnyBingoReaction], query: TextLike, parameters: TextLike = ""
) -> ColumnElement[bool]:
    """
    Perform SMARTS pattern matching on a reaction column.

    Parameters
    ----------
    rxn : ColumnElement[AnyBingoReaction]
        SQLAlchemy column containing reaction data (reaction SMILES, RXN, or binary).
    query : TextLike
        Reaction SMARTS pattern string for matching.
    parameters : TextLike, optional
        Search parameters for customizing the matching behavior (default is "").

    Returns
    -------
    ColumnElement[bool]
        SQLAlchemy expression for reaction SMARTS matching that can be used in WHERE clauses.

    """
    return _bingo_search_values(rxn, (query, parameters), "bingo.rsmarts")


def rxn_equals(
    rxn: ColumnElement[AnyBingoReaction], query: TextLike, parameters: TextLike = ""
) -> ColumnElement[bool]:
    """
    Perform exact matching on a reaction column.

    Parameters
    ----------
    rxn : ColumnElement[AnyBingoReaction]
        SQLAlchemy column containing reaction data (reaction SMILES, RXN, or binary).
    query : TextLike
        Query reaction as reaction SMILES or RXN string for exact matching.
    parameters : TextLike, optional
        Search parameters for customizing the matching behavior (default is "").

    Returns
    -------
    ColumnElement[bool]
        SQLAlchemy expression for exact reaction matching that can be used in WHERE clauses.

    """
    return _bingo_search_values(rxn, (query, parameters), "bingo.rexact")


class aam(GenericFunction):
    inherit_cache = True
    name = "aam"

    def __init__(
        self,
        rxn: AnyBingoReactionLike | AnyBingoBinaryReactionLike,
        strategy: sqltypes.Text | Literal["CLEAR", "DISCARD", "ALTER", "KEEP"] = "KEEP",
        **kwargs: Any,
    ) -> None:
        """Creates an atom-atom mapping for a reaction.

        Parameters
        ----------
        rxn : AnyBingoReactionLike | AnyBingoBinaryReactionLike
            Input reaction
        strategy : sqltypes.Text | Literal['CLEAR', 'DISCARD', 'ALTER', 'KEEP']
            Strategy for handling existing atom mapping (default is 'KEEP').
                - 'CLEAR': Remove all existing mappings and compute new ones
                - 'DISCARD': Remove all mappings without computing new ones
                - 'ALTER': Modify existing mappings
                - 'KEEP': Keep existing mappings and map unmapped atoms
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(rxn, strategy, **kwargs)
        self.packagenames = ("bingo",)


class cansmiles(GenericFunction):
    inherit_cache = True
    name = "cansmiles"

    def __init__(
        self, mol: AnyBingoMolLike | AnyBingoBinaryMolLike, **kwargs: Any
    ) -> None:
        """Generates the canonical SMILES for a molecule.

        Parameters
        ----------
        mol : AnyBingoMolLike | AnyBingoBinaryMolLike
            Input molecule in any supported format
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(mol, **kwargs)
        self.packagenames = ("bingo",)


class checkmolecule(GenericFunction):
    inherit_cache = True
    name = "checkmolecule"

    def __init__(
        self, mol: AnyBingoMolLike | AnyBingoBinaryMolLike, **kwargs: Any
    ) -> None:
        """Check molecule for validity

        Parameters
        ----------
        mol : AnyBingoMolLike | AnyBingoBinaryMolLike
            Input molecule in any supported format
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(mol, **kwargs)
        self.packagenames = ("bingo",)


class checkreaction(GenericFunction):
    inherit_cache = True
    name = "checkreaction"

    def __init__(
        self, rxn: AnyBingoReactionLike | AnyBingoBinaryReactionLike, **kwargs: Any
    ) -> None:
        """Check reaction for validity

        Parameters
        ----------
        rxn : AnyBingoReactionLike | AnyBingoBinaryReactionLike
            Input reaction in any supported format
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(rxn, **kwargs)
        self.packagenames = ("bingo",)


class cml(GenericFunction):
    inherit_cache = True
    name = "cml"

    def __init__(
        self, mol: AnyBingoMolLike | AnyBingoBinaryMolLike, **kwargs: Any
    ) -> None:
        """Converts a molecule to CML format.

        Parameters
        ----------
        mol : AnyBingoMolLike | AnyBingoBinaryMolLike
            Input molecule in any supported format
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(mol, **kwargs)
        self.packagenames = ("bingo",)


class compactmolecule(GenericFunction):
    inherit_cache = True
    name = "compactmolecule"

    def __init__(
        self,
        mol: AnyBingoMolLike | AnyBingoBinaryMolLike,
        use_pos: sqltypes.Boolean | bool = False,
        **kwargs: Any,
    ) -> None:
        """Calculates the compact representation of a molecule.

        Parameters
        ----------
        mol : AnyBingoMolLike | AnyBingoBinaryMolLike
            Input molecule in any supported format
        use_pos : sqltypes.Boolean | bool
            If it is true, the positions of atoms are saved to the binary format. If it is false, the positions are skipped.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[bytes | sqltypes.LargeBinary]
            SQLAlchemy function
        """
        super().__init__(mol, use_pos, **kwargs)
        self.packagenames = ("bingo",)


class compactreaction(GenericFunction):
    inherit_cache = True
    name = "compactreaction"

    def __init__(
        self,
        rxn: AnyBingoReactionLike | AnyBingoBinaryReactionLike,
        use_pos: sqltypes.Boolean | bool = False,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `compactreaction`.

        Parameters
        ----------
        rxn : AnyBingoReactionLike | AnyBingoBinaryReactionLike
            Input reaction in any supported format
        use_pos : sqltypes.Boolean | bool
            If it is true, the positions of atoms are saved to the binary format. If it is false, the positions are skipped.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[bytes | sqltypes.LargeBinary]
            SQLAlchemy function
        """
        super().__init__(rxn, use_pos, **kwargs)
        self.packagenames = ("bingo",)


class exportrdf(GenericFunction):
    inherit_cache = True
    name = "exportrdf"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text,
        arg_3: str | sqltypes.Text,
        arg_4: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Exports reactions to an RDF format.

        Parameters
        ----------
        arg_1 : str | sqltypes.Text
            Undocumented cartridge parameter.
        arg_2 : str | sqltypes.Text
            Undocumented cartridge parameter.
        arg_3 : str | sqltypes.Text
            Undocumented cartridge parameter.
        arg_4 : str | sqltypes.Text
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[None | sqltypes.NullType]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, arg_4, **kwargs)
        self.packagenames = ("bingo",)


class exportsdf(GenericFunction):
    inherit_cache = True
    name = "exportsdf"

    def __init__(
        self,
        table: str | sqltypes.Text,
        column: str | sqltypes.Text,
        other_columns: str | sqltypes.Text,
        outfile: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Exports molecules to an SDF format.

        Parameters
        ----------
        table : str | sqltypes.Text
            Name of the table containing the molecules to export
        column : str | sqltypes.Text
            Name of the column containing the molecules to export
        other_columns : str | sqltypes.Text
            Space-separated list of other columns to include in the SDF file as SD data fields
        outfile : str | sqltypes.Text
            Path to the output SDF file
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[None | sqltypes.NullType]
            SQLAlchemy function
        """
        super().__init__(table, column, other_columns, outfile, **kwargs)
        self.packagenames = ("bingo",)


class filetoblob(GenericFunction):
    inherit_cache = True
    name = "filetoblob"

    def __init__(self, arg_1: str | sqltypes.Text, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `filetoblob`.

        Parameters
        ----------
        arg_1 : str | sqltypes.Text
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[bytes | sqltypes.LargeBinary]
            SQLAlchemy function
        """
        super().__init__(arg_1, **kwargs)
        self.packagenames = ("bingo",)


class filetotext(GenericFunction):
    inherit_cache = True
    name = "filetotext"

    def __init__(self, arg_1: str | sqltypes.Text, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `filetotext`.

        Parameters
        ----------
        arg_1 : str | sqltypes.Text
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(arg_1, **kwargs)
        self.packagenames = ("bingo",)


class fingerprint(GenericFunction):
    inherit_cache = True
    name = "fingerprint"

    def __init__(
        self,
        arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_2: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `fingerprint`.

        Parameters
        ----------
        arg_1 : str | sqltypes.Text | bytes | sqltypes.LargeBinary
            Undocumented cartridge parameter.
        arg_2 : str | sqltypes.Text
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[bytes | sqltypes.LargeBinary]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, **kwargs)
        self.packagenames = ("bingo",)


class getblockcount(GenericFunction):
    inherit_cache = True
    name = "getblockcount"

    def __init__(self, arg_1: str | sqltypes.Text, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `getblockcount`.

        Parameters
        ----------
        arg_1 : str | sqltypes.Text
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            SQLAlchemy function
        """
        super().__init__(arg_1, **kwargs)
        self.packagenames = ("bingo",)


class getindexstructurescount(GenericFunction):
    inherit_cache = True
    name = "getindexstructurescount"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `getindexstructurescount`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class getmass(GenericFunction):
    inherit_cache = True
    name = "getmass"

    def __init__(
        self, arg_1: AnyBingoMolLike | AnyBingoBinaryMolLike, **kwargs: Any
    ) -> None:
        """Calls the bingo cartridge function `getmass`.

        Parameters
        ----------
        arg_1 : AnyBingoMolLike | AnyBingoBinaryMolLike
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[float | sqltypes.Float]
            SQLAlchemy function
        """
        super().__init__(arg_1, **kwargs)
        self.packagenames = ("bingo",)


class getname(GenericFunction):
    inherit_cache = True
    name = "getname"

    def __init__(self, arg_1: AnyBingoMolLike, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `getname`.

        Parameters
        ----------
        arg_1 : AnyBingoMolLike
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(arg_1, **kwargs)
        self.packagenames = ("bingo",)


class getsimilarity(GenericFunction):
    inherit_cache = True
    name = "getsimilarity"

    def __init__(
        self,
        mol: AnyBingoMolLike | AnyBingoBinaryMolLike,
        query: TextLike,
        metric: TextLike | Literal["tanimoto", "euclid-sub"] = "tanimoto",
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `getsimilarity`.

        Parameters
        ----------
        mol : AnyBingoMolLike | AnyBingoBinaryMolLike
            Input molecule or molecular column in any supported format
        query : TextLike
            Query molecule in any supported format
        metric : TextLike | Literal['tanimoto', 'euclid-sub']
            string specifying the metric to use: `tanimoto` , `tversky`, or `euclid-sub`. In case of Tversky metric, there are optional “alpha” and “beta” parameters: `tversky 0.9 0.1` denotes alpha = 0.9, beta = 0.1. The default is alpha = beta = 0.5 (Dice index).
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[float | sqltypes.Float]
            SQLAlchemy function
        """
        super().__init__(mol, query, metric, **kwargs)
        self.packagenames = ("bingo",)


class getstructurescount(GenericFunction):
    inherit_cache = True
    name = "getstructurescount"

    def __init__(self, arg_1: str | sqltypes.Text, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `getstructurescount`.

        Parameters
        ----------
        arg_1 : str | sqltypes.Text
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            SQLAlchemy function
        """
        super().__init__(arg_1, **kwargs)
        self.packagenames = ("bingo",)


class getversion(GenericFunction):
    inherit_cache = True
    name = "getversion"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `getversion`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class getweight(GenericFunction):
    inherit_cache = True
    name = "getweight"

    def __init__(
        self,
        mol: AnyBingoMolLike | AnyBingoBinaryMolLike,
        arg_2: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `getweight`.

        Parameters
        ----------
        mol : AnyBingoMolLike | AnyBingoBinaryMolLike
            Undocumented cartridge parameter.
        arg_2 : str | sqltypes.Text
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[float | sqltypes.Float]
            SQLAlchemy function
        """
        super().__init__(mol, arg_2, **kwargs)
        self.packagenames = ("bingo",)


class gross(GenericFunction):
    inherit_cache = True
    name = "gross"

    def __init__(
        self, mol: AnyBingoMolLike | AnyBingoBinaryMolLike, **kwargs: Any
    ) -> None:
        """Calls the bingo cartridge function `gross`.

        Parameters
        ----------
        mol : AnyBingoMolLike | AnyBingoBinaryMolLike
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(mol, **kwargs)
        self.packagenames = ("bingo",)


class importrdf(GenericFunction):
    inherit_cache = True
    name = "importrdf"

    def __init__(
        self,
        arg_1: TextLike,
        arg_2: TextLike,
        arg_3: TextLike,
        arg_4: TextLike,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `importrdf`.

        Parameters
        ----------
        arg_1 : TextLike
            Undocumented cartridge parameter.
        arg_2 : TextLike
            Undocumented cartridge parameter.
        arg_3 : TextLike
            Undocumented cartridge parameter.
        arg_4 : TextLike
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[None | sqltypes.NullType]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, arg_4, **kwargs)
        self.packagenames = ("bingo",)


class importsdf(GenericFunction):
    inherit_cache = True
    name = "importsdf"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text,
        arg_3: str | sqltypes.Text,
        arg_4: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `importsdf`.

        Parameters
        ----------
        arg_1 : str | sqltypes.Text
            Undocumented cartridge parameter.
        arg_2 : str | sqltypes.Text
            Undocumented cartridge parameter.
        arg_3 : str | sqltypes.Text
            Undocumented cartridge parameter.
        arg_4 : str | sqltypes.Text
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[None | sqltypes.NullType]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, arg_4, **kwargs)
        self.packagenames = ("bingo",)


class importsmiles(GenericFunction):
    inherit_cache = True
    name = "importsmiles"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text,
        arg_3: str | sqltypes.Text,
        arg_4: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `importsmiles`.

        Parameters
        ----------
        arg_1 : str | sqltypes.Text
            Undocumented cartridge parameter.
        arg_2 : str | sqltypes.Text
            Undocumented cartridge parameter.
        arg_3 : str | sqltypes.Text
            Undocumented cartridge parameter.
        arg_4 : str | sqltypes.Text
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[None | sqltypes.NullType]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, arg_4, **kwargs)
        self.packagenames = ("bingo",)


class inchi(GenericFunction):
    inherit_cache = True
    name = "inchi"

    def __init__(
        self,
        mol: AnyBingoMolLike | AnyBingoBinaryMolLike,
        arg_2: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `inchi`.

        Parameters
        ----------
        mol : AnyBingoMolLike | AnyBingoBinaryMolLike
            Undocumented cartridge parameter.
        arg_2 : str | sqltypes.Text
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(mol, arg_2, **kwargs)
        self.packagenames = ("bingo",)


class inchikey(GenericFunction):
    inherit_cache = True
    name = "inchikey"

    def __init__(self, mol: AnyBingoMolLike, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `inchikey`.

        Parameters
        ----------
        mol : AnyBingoMolLike
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(mol, **kwargs)
        self.packagenames = ("bingo",)


class matchexact(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "matchexact"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `matchexact`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class matchgross(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "matchgross"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `matchgross`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class matchrexact(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "matchrexact"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `matchrexact`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class matchrsmarts(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "matchrsmarts"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `matchrsmarts`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class matchrsub(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "matchrsub"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `matchrsub`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class matchsim(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "matchsim"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `matchsim`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class matchsmarts(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "matchsmarts"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `matchsmarts`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class matchsub(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "matchsub"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `matchsub`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class molfile(GenericFunction):
    inherit_cache = True
    name = "molfile"

    def __init__(
        self, mol: AnyBingoMolLike | AnyBingoBinaryMolLike, **kwargs: Any
    ) -> None:
        """Calls the bingo cartridge function `molfile`.

        Parameters
        ----------
        mol : AnyBingoMolLike | AnyBingoBinaryMolLike
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(mol, **kwargs)
        self.packagenames = ("bingo",)


class precachedatabase(GenericFunction):
    inherit_cache = True
    name = "precachedatabase"

    def __init__(
        self, arg_1: str | sqltypes.Text, arg_2: str | sqltypes.Text, **kwargs: Any
    ) -> None:
        """Calls the bingo cartridge function `precachedatabase`.

        Parameters
        ----------
        arg_1 : str | sqltypes.Text
            Undocumented cartridge parameter.
        arg_2 : str | sqltypes.Text
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, **kwargs)
        self.packagenames = ("bingo",)


class rcml(GenericFunction):
    inherit_cache = True
    name = "rcml"

    def __init__(
        self, rxn: AnyBingoReactionLike | AnyBingoBinaryReactionLike, **kwargs: Any
    ) -> None:
        """Calls the bingo cartridge function `rcml`.

        Parameters
        ----------
        rxn : AnyBingoReactionLike | AnyBingoBinaryReactionLike
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(rxn, **kwargs)
        self.packagenames = ("bingo",)


class rfingerprint(GenericFunction):
    inherit_cache = True
    name = "rfingerprint"

    def __init__(
        self,
        rxn: AnyBingoReactionLike | AnyBingoBinaryReactionLike,
        arg_2: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `rfingerprint`.

        Parameters
        ----------
        rxn : AnyBingoReactionLike | AnyBingoBinaryReactionLike
            Undocumented cartridge parameter.
        arg_2 : str | sqltypes.Text
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[bytes | sqltypes.LargeBinary]
            SQLAlchemy function
        """
        super().__init__(rxn, arg_2, **kwargs)
        self.packagenames = ("bingo",)


class rsmiles(GenericFunction):
    inherit_cache = True
    name = "rsmiles"

    def __init__(
        self, rxn: AnyBingoReactionLike | AnyBingoBinaryReactionLike, **kwargs: Any
    ) -> None:
        """Calls the bingo cartridge function `rsmiles`.

        Parameters
        ----------
        rxn : AnyBingoReactionLike | AnyBingoBinaryReactionLike
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(rxn, **kwargs)
        self.packagenames = ("bingo",)


class rxnfile(GenericFunction):
    inherit_cache = True
    name = "rxnfile"

    def __init__(
        self, rxn: AnyBingoReactionLike | AnyBingoBinaryReactionLike, **kwargs: Any
    ) -> None:
        """Calls the bingo cartridge function `rxnfile`.

        Parameters
        ----------
        rxn : AnyBingoReactionLike | AnyBingoBinaryReactionLike
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(rxn, **kwargs)
        self.packagenames = ("bingo",)


class smiles(GenericFunction):
    inherit_cache = True
    name = "smiles"

    def __init__(
        self, mol: AnyBingoMolLike | AnyBingoBinaryMolLike, **kwargs: Any
    ) -> None:
        """Calls the bingo cartridge function `smiles`.

        Parameters
        ----------
        mol : AnyBingoMolLike | AnyBingoBinaryMolLike
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(mol, **kwargs)
        self.packagenames = ("bingo",)


class standardize(GenericFunction):
    inherit_cache = True
    name = "standardize"

    def __init__(
        self,
        mol: AnyBingoMolLike | AnyBingoBinaryMolLike,
        arg_2: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `standardize`.

        Parameters
        ----------
        mol : AnyBingoMolLike | AnyBingoBinaryMolLike
            Undocumented cartridge parameter.
        arg_2 : str | sqltypes.Text
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(mol, arg_2, **kwargs)
        self.packagenames = ("bingo",)
