"""Auto-generated from `data/bingo/functions.json`. Do not edit manually.
This file defines public Bingo PostgreSQL function wrappers for use with SQLAlchemy.
"""

from typing import Any, Literal, cast

from sqlalchemy import types as sqltypes
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.functions import GenericFunction

from molalchemy.bingo.search import _bingo_search_values
from molalchemy.protocols import (
    BingoMolSqlOperand,
    BingoOperand,
    BingoParameters,
    BingoReactionSqlOperand,
    BingoSimilarityBound,
    BooleanOperand,
    SqlOperand,
    TextOperand,
    TextOrBinaryOperand,
)

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
    mol: BingoMolSqlOperand, query: TextLike, parameters: TextLike = ""
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
    mol: BingoMolSqlOperand, query: TextLike, parameters: TextLike = ""
) -> ColumnElement[bool]:
    """
    Perform SMARTS pattern matching on a molecule column.

    Parameters
    ----------
    mol : BingoMolSqlOperand
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
    mol: BingoMolSqlOperand, query: TextLike, parameters: TextLike = ""
) -> ColumnElement[bool]:
    """
    Perform exact structure matching on a molecule column.

    Parameters
    ----------
    mol : BingoMolSqlOperand
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


def mol_not_equals(
    mol: BingoMolSqlOperand, query: TextLike, parameters: TextLike = ""
) -> ColumnElement[bool]:
    """Perform negated exact structure matching on a molecule column."""
    return ~mol_equals(mol, query, parameters)


def mol_similar_to(
    mol: BingoMolSqlOperand,
    query: BingoOperand,
    minimum: BingoSimilarityBound = 0.0,
    maximum: BingoSimilarityBound = 1.0,
    metric: BingoParameters = "Tanimoto",
) -> ColumnElement[bool]:
    """
    Check whether molecular similarity is within the requested range.

    Parameters
    ----------
    mol : SqlOperand
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    query : BingoOperand
        Query molecule as SMILES or Molfile string for similarity comparison.
    minimum : BingoSimilarityBound, optional
        Minimum similarity threshold (default is 0.0).
    maximum : BingoSimilarityBound, optional
        Maximum similarity threshold (default is 1.0).
    metric : BingoParameters, optional
        Similarity metric to use (default is "Tanimoto").
        Other options include "Dice", "Cosine", etc.

    Returns
    -------
    ColumnElement[bool]
        SQLAlchemy expression for similarity matching that can be used in WHERE clauses.

    """
    return _bingo_search_values(mol, (minimum, maximum, query, metric), "bingo.sim")


def mol_similarity(
    mol: BingoMolSqlOperand,
    query: BingoOperand,
    bottom: BingoSimilarityBound = 0.0,
    top: BingoSimilarityBound = 1.0,
    metric: BingoParameters = "Tanimoto",
) -> ColumnElement[bool]:
    """Compatibility spelling for :func:`mol_similar_to`.

    ``bottom`` and ``top`` retain the historical keyword names. New code should
    use :func:`mol_similar_to` with ``minimum`` and ``maximum``.
    """
    return mol_similar_to(mol, query, bottom, top, metric)


def mol_similarity_score(
    mol: BingoMolSqlOperand,
    query: BingoOperand,
    metric: BingoParameters = "Tanimoto",
) -> ColumnElement[float]:
    """Return the numeric molecular similarity score for ``query``."""
    return cast(ColumnElement[float], getsimilarity(mol, query, metric))


def rxn_has_substructure(
    rxn: BingoReactionSqlOperand, query: TextLike, parameters: TextLike = ""
) -> ColumnElement[bool]:
    """
    Perform substructure search on a reaction column.

    Parameters
    ----------
    rxn : BingoReactionSqlOperand
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
    rxn: BingoReactionSqlOperand, query: TextLike, parameters: TextLike = ""
) -> ColumnElement[bool]:
    """
    Perform SMARTS pattern matching on a reaction column.

    Parameters
    ----------
    rxn : BingoReactionSqlOperand
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
    rxn: BingoReactionSqlOperand, query: TextLike, parameters: TextLike = ""
) -> ColumnElement[bool]:
    """
    Perform exact matching on a reaction column.

    Parameters
    ----------
    rxn : BingoReactionSqlOperand
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


def rxn_not_equals(
    rxn: BingoReactionSqlOperand, query: TextLike, parameters: TextLike = ""
) -> ColumnElement[bool]:
    """Perform negated exact matching on a reaction column."""
    return ~rxn_equals(rxn, query, parameters)


class aam(GenericFunction[str]):
    type = sqltypes.Text()
    inherit_cache = True
    name = "aam"

    def __init__(
        self,
        rxn: AnyBingoReactionLike | AnyBingoBinaryReactionLike,
        strategy: Literal["CLEAR", "DISCARD", "ALTER", "KEEP"]
        | SqlOperand[str] = "KEEP",
        **kwargs: Any,
    ) -> None:
        """Creates an atom-atom mapping for a reaction.

        Parameters
        ----------
        rxn : AnyBingoReactionLike | AnyBingoBinaryReactionLike
            Input reaction
        strategy : Literal['CLEAR', 'DISCARD', 'ALTER', 'KEEP'] | SqlOperand[str]
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


class cansmiles(GenericFunction[str]):
    type = sqltypes.Text()
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


class checkmolecule(GenericFunction[str]):
    type = sqltypes.Text()
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


class checkreaction(GenericFunction[str]):
    type = sqltypes.Text()
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


class cml(GenericFunction[str]):
    type = sqltypes.Text()
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


class compactmolecule(GenericFunction[bytes]):
    type = sqltypes.LargeBinary()
    inherit_cache = True
    name = "compactmolecule"

    def __init__(
        self,
        mol: AnyBingoMolLike | AnyBingoBinaryMolLike,
        use_pos: BooleanOperand = False,
        **kwargs: Any,
    ) -> None:
        """Calculates the compact representation of a molecule.

        Parameters
        ----------
        mol : AnyBingoMolLike | AnyBingoBinaryMolLike
            Input molecule in any supported format
        use_pos : BooleanOperand
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


class compactreaction(GenericFunction[bytes]):
    type = sqltypes.LargeBinary()
    inherit_cache = True
    name = "compactreaction"

    def __init__(
        self,
        rxn: AnyBingoReactionLike | AnyBingoBinaryReactionLike,
        use_pos: BooleanOperand = False,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `compactreaction`.

        Parameters
        ----------
        rxn : AnyBingoReactionLike | AnyBingoBinaryReactionLike
            Input reaction in any supported format
        use_pos : BooleanOperand
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


class exportrdf(GenericFunction[None]):
    type = sqltypes.NullType()
    inherit_cache = True
    name = "exportrdf"

    def __init__(
        self,
        arg_1: TextOperand,
        arg_2: TextOperand,
        arg_3: TextOperand,
        arg_4: TextOperand,
        **kwargs: Any,
    ) -> None:
        """Exports reactions to an RDF format.

        Parameters
        ----------
        arg_1 : TextOperand
            Undocumented cartridge parameter.
        arg_2 : TextOperand
            Undocumented cartridge parameter.
        arg_3 : TextOperand
            Undocumented cartridge parameter.
        arg_4 : TextOperand
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


class exportsdf(GenericFunction[None]):
    type = sqltypes.NullType()
    inherit_cache = True
    name = "exportsdf"

    def __init__(
        self,
        table: TextOperand,
        column: TextOperand,
        other_columns: TextOperand,
        outfile: TextOperand,
        **kwargs: Any,
    ) -> None:
        """Exports molecules to an SDF format.

        Parameters
        ----------
        table : TextOperand
            Name of the table containing the molecules to export
        column : TextOperand
            Name of the column containing the molecules to export
        other_columns : TextOperand
            Space-separated list of other columns to include in the SDF file as SD data fields
        outfile : TextOperand
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


class filetoblob(GenericFunction[bytes]):
    type = sqltypes.LargeBinary()
    inherit_cache = True
    name = "filetoblob"

    def __init__(self, arg_1: TextOperand, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `filetoblob`.

        Parameters
        ----------
        arg_1 : TextOperand
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


class filetotext(GenericFunction[str]):
    type = sqltypes.Text()
    inherit_cache = True
    name = "filetotext"

    def __init__(self, arg_1: TextOperand, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `filetotext`.

        Parameters
        ----------
        arg_1 : TextOperand
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


class fingerprint(GenericFunction[bytes]):
    type = sqltypes.LargeBinary()
    inherit_cache = True
    name = "fingerprint"

    def __init__(
        self, arg_1: TextOrBinaryOperand, arg_2: TextOperand, **kwargs: Any
    ) -> None:
        """Calls the bingo cartridge function `fingerprint`.

        Parameters
        ----------
        arg_1 : TextOrBinaryOperand
            Undocumented cartridge parameter.
        arg_2 : TextOperand
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


class getblockcount(GenericFunction[int]):
    type = sqltypes.Integer()
    inherit_cache = True
    name = "getblockcount"

    def __init__(self, arg_1: TextOperand, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `getblockcount`.

        Parameters
        ----------
        arg_1 : TextOperand
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


class getindexstructurescount(GenericFunction[int]):
    type = sqltypes.Integer()
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


class getmass(GenericFunction[float]):
    type = sqltypes.Float()
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


class getname(GenericFunction[str]):
    type = sqltypes.Text()
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


class getsimilarity(GenericFunction[float]):
    type = sqltypes.Float()
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
        Function[sqltypes.Float]
            SQLAlchemy function
        """
        super().__init__(mol, query, metric, **kwargs)
        self.packagenames = ("bingo",)


class getstructurescount(GenericFunction[int]):
    type = sqltypes.Integer()
    inherit_cache = True
    name = "getstructurescount"

    def __init__(self, arg_1: TextOperand, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `getstructurescount`.

        Parameters
        ----------
        arg_1 : TextOperand
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


class getversion(GenericFunction[str]):
    type = sqltypes.Text()
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


class getweight(GenericFunction[float]):
    type = sqltypes.Float()
    inherit_cache = True
    name = "getweight"

    def __init__(
        self,
        mol: AnyBingoMolLike | AnyBingoBinaryMolLike,
        arg_2: TextOperand,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `getweight`.

        Parameters
        ----------
        mol : AnyBingoMolLike | AnyBingoBinaryMolLike
            Undocumented cartridge parameter.
        arg_2 : TextOperand
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


class gross(GenericFunction[str]):
    type = sqltypes.Text()
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


class importrdf(GenericFunction[None]):
    type = sqltypes.NullType()
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


class importsdf(GenericFunction[None]):
    type = sqltypes.NullType()
    inherit_cache = True
    name = "importsdf"

    def __init__(
        self,
        arg_1: TextOperand,
        arg_2: TextOperand,
        arg_3: TextOperand,
        arg_4: TextOperand,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `importsdf`.

        Parameters
        ----------
        arg_1 : TextOperand
            Undocumented cartridge parameter.
        arg_2 : TextOperand
            Undocumented cartridge parameter.
        arg_3 : TextOperand
            Undocumented cartridge parameter.
        arg_4 : TextOperand
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


class importsmiles(GenericFunction[None]):
    type = sqltypes.NullType()
    inherit_cache = True
    name = "importsmiles"

    def __init__(
        self,
        arg_1: TextOperand,
        arg_2: TextOperand,
        arg_3: TextOperand,
        arg_4: TextOperand,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `importsmiles`.

        Parameters
        ----------
        arg_1 : TextOperand
            Undocumented cartridge parameter.
        arg_2 : TextOperand
            Undocumented cartridge parameter.
        arg_3 : TextOperand
            Undocumented cartridge parameter.
        arg_4 : TextOperand
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


class inchi(GenericFunction[str]):
    type = sqltypes.Text()
    inherit_cache = True
    name = "inchi"

    def __init__(
        self,
        mol: AnyBingoMolLike | AnyBingoBinaryMolLike,
        arg_2: TextOperand,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `inchi`.

        Parameters
        ----------
        mol : AnyBingoMolLike | AnyBingoBinaryMolLike
            Undocumented cartridge parameter.
        arg_2 : TextOperand
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


class inchikey(GenericFunction[str]):
    type = sqltypes.Text()
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


class matchexact(GenericFunction[bool]):
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


class matchgross(GenericFunction[bool]):
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


class matchrexact(GenericFunction[bool]):
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


class matchrsmarts(GenericFunction[bool]):
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


class matchrsub(GenericFunction[bool]):
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


class matchsim(GenericFunction[bool]):
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


class matchsmarts(GenericFunction[bool]):
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


class matchsub(GenericFunction[bool]):
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


class molfile(GenericFunction[str]):
    type = sqltypes.Text()
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


class precachedatabase(GenericFunction[str]):
    type = sqltypes.Text()
    inherit_cache = True
    name = "precachedatabase"

    def __init__(self, arg_1: TextOperand, arg_2: TextOperand, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `precachedatabase`.

        Parameters
        ----------
        arg_1 : TextOperand
            Undocumented cartridge parameter.
        arg_2 : TextOperand
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


class rcml(GenericFunction[str]):
    type = sqltypes.Text()
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


class rfingerprint(GenericFunction[bytes]):
    type = sqltypes.LargeBinary()
    inherit_cache = True
    name = "rfingerprint"

    def __init__(
        self,
        rxn: AnyBingoReactionLike | AnyBingoBinaryReactionLike,
        arg_2: TextOperand,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `rfingerprint`.

        Parameters
        ----------
        rxn : AnyBingoReactionLike | AnyBingoBinaryReactionLike
            Undocumented cartridge parameter.
        arg_2 : TextOperand
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


class rsmiles(GenericFunction[str]):
    type = sqltypes.Text()
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


class rxnfile(GenericFunction[str]):
    type = sqltypes.Text()
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


class smiles(GenericFunction[str]):
    type = sqltypes.Text()
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


class standardize(GenericFunction[str]):
    type = sqltypes.Text()
    inherit_cache = True
    name = "standardize"

    def __init__(
        self,
        mol: AnyBingoMolLike | AnyBingoBinaryMolLike,
        arg_2: TextOperand,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `standardize`.

        Parameters
        ----------
        mol : AnyBingoMolLike | AnyBingoBinaryMolLike
            Undocumented cartridge parameter.
        arg_2 : TextOperand
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
