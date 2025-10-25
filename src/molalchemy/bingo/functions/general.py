"""Auto-generated from `data/bingo/functions.json`. Do not edit manually.
This file defines public Bingo PostgreSQL function wrappers for use with SQLAlchemy.
"""

from typing import Any, Literal

from sqlalchemy import types as sqltypes
from sqlalchemy.sql import text
from sqlalchemy.sql.elements import BinaryExpression, ColumnElement
from sqlalchemy.sql.functions import GenericFunction

from molalchemy.bingo.types import (
    BingoBinaryMol,
    BingoBinaryReaction,
    BingoMol,
    BingoReaction,
)

AnyBingoMol = BingoMol | BingoBinaryMol

AnyBingoReaction = BingoReaction | BingoBinaryReaction


def has_substructure(
    mol_column: ColumnElement[AnyBingoMol], query: str, parameters: str = ""
):
    """
    Perform substructure search on a molecule column.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    query : str
        Query molecule as SMILES, SMARTS, or Molfile string.
    parameters : str, optional
        Search parameters for customizing the matching behavior (default is "").
        Examples: "TAU" for tautomer search, "RES" for resonance search.

    Returns
    -------
    BinaryExpression
        SQLAlchemy expression for substructure matching that can be used in WHERE clauses.

    """
    return mol_column.op("@")(text(f"('{query}', '{parameters}')::bingo.sub"))


def matches_smarts(
    mol_column: ColumnElement[AnyBingoMol], query: str, parameters: str = ""
):
    """
    Perform SMARTS pattern matching on a molecule column.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    query : str
        SMARTS pattern string for matching.
    parameters : str, optional
        Search parameters for customizing the matching behavior (default is "").

    Returns
    -------
    BinaryExpression
        SQLAlchemy expression for SMARTS matching that can be used in WHERE clauses.

    """
    return mol_column.op("@")(text(f"('{query}', '{parameters}')::bingo.smarts"))


def mol_equals(
    mol_column: ColumnElement[AnyBingoMol], query: str, parameters: str = ""
):
    """
    Perform exact structure matching on a molecule column.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    query : str
        Query molecule as SMILES or Molfile string for exact matching.
    parameters : str, optional
        Search parameters for customizing the matching behavior (default is "").
        Examples: "TAU" for tautomer matching, "STE" for stereochemistry.

    Returns
    -------
    BinaryExpression
        SQLAlchemy expression for exact matching that can be used in WHERE clauses.

    """
    return mol_column.op("@")(text(f"('{query}', '{parameters}')::bingo.exact"))


def similarity(
    mol_column: ColumnElement[AnyBingoMol],
    query: str,
    bottom: float = 0.0,
    top: float = 1.0,
    metric: str = "Tanimoto",
) -> BinaryExpression:
    """
    Perform similarity search on a molecule column. This should be used in WHERE clauses, as it
    returns a boolean expression indicating whether the similarity criteria are met.

    Parameters
    ----------
    mol_column : ColumnElement
        SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
    query : str
        Query molecule as SMILES or Molfile string for similarity comparison.
    bottom : float, optional
        Minimum similarity threshold (default is 0.0).
    top : float, optional
        Maximum similarity threshold (default is 1.0).
    metric : str, optional
        Similarity metric to use (default is "Tanimoto").
        Other options include "Dice", "Cosine", etc.

    Returns
    -------
    BinaryExpression
        SQLAlchemy expression for similarity matching that can be used in WHERE clauses.

    """
    return mol_column.op("%")(
        text(f"('{query}', {bottom}, {top}, '{metric}')::bingo.sim")
    )


class aam(GenericFunction):
    inherit_cache = True
    name = "aam"

    def __init__(
        self,
        rxn: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        strategy: sqltypes.Text | Literal["CLEAR", "DISCARD", "ALTER", "KEEP"] = "KEEP",
        **kwargs: Any,
    ) -> None:
        """Creates an atom-atom mapping for a reaction.

        Parameters
        ----------
        rxn
            Input reaction
        strategy
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
        self, mol: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        """Generates the canonical SMILES for a molecule.

        Parameters
        ----------
        mol
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
        self, mol: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        """Check molecule for validity

        Parameters
        ----------
        mol
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
        self, rxn: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        """Check reaction for validity

        Parameters
        ----------
        rxn
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
        self, mol: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        """Converts a molecule to CML format.

        Parameters
        ----------
        mol
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
        mol: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        use_pos: sqltypes.Boolean | bool = False,
        **kwargs: Any,
    ) -> None:
        """Calculates the compact representation of a molecule.

        Parameters
        ----------
        mol
            Input molecule in any supported format
        use_pos
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
        rxn: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        use_pos: sqltypes.Boolean | bool = False,
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `compactreaction`.

        Parameters
        ----------
        rxn
            Input reaction in any supported format
        use_pos
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
        arg_1
        arg_2
        arg_3
        arg_4
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
        table
            Name of the table containing the molecules to export
        column
            Name of the column containing the molecules to export
        other_columns
            Space-separated list of other columns to include in the SDF file as SD data fields
        outfile
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
        """Calls the rdkit cartridge function `filetoblob`.

        Parameters
        ----------
        arg_1
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
        """Calls the rdkit cartridge function `filetotext`.

        Parameters
        ----------
        arg_1
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
        """Calls the rdkit cartridge function `fingerprint`.

        Parameters
        ----------
        arg_1
        arg_2
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
        """Calls the rdkit cartridge function `getblockcount`.

        Parameters
        ----------
        arg_1
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
        """Calls the rdkit cartridge function `getindexstructurescount`.

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
        self, arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        """Calls the rdkit cartridge function `getmass`.

        Parameters
        ----------
        arg_1
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

    def __init__(self, arg_1: str | sqltypes.Text, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `getname`.

        Parameters
        ----------
        arg_1
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
        mol: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        query: str | sqltypes.Text,
        metric: str | sqltypes.Text = "tanimoto",
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `getsimilarity`.

        Parameters
        ----------
        mol
            Input molecule or molecular column in any supported format
        query
            Query molecule in any supported format
        metric
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
        """Calls the rdkit cartridge function `getstructurescount`.

        Parameters
        ----------
        arg_1
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
        """Calls the rdkit cartridge function `getversion`.

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
        arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_2: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `getweight`.

        Parameters
        ----------
        arg_1
        arg_2
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[float | sqltypes.Float]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, **kwargs)
        self.packagenames = ("bingo",)


class gross(GenericFunction):
    inherit_cache = True
    name = "gross"

    def __init__(
        self, arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        """Calls the rdkit cartridge function `gross`.

        Parameters
        ----------
        arg_1
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(arg_1, **kwargs)
        self.packagenames = ("bingo",)


class importrdf(GenericFunction):
    inherit_cache = True
    name = "importrdf"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text,
        arg_3: str | sqltypes.Text,
        arg_4: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `importrdf`.

        Parameters
        ----------
        arg_1
        arg_2
        arg_3
        arg_4
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
        """Calls the rdkit cartridge function `importsdf`.

        Parameters
        ----------
        arg_1
        arg_2
        arg_3
        arg_4
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
        """Calls the rdkit cartridge function `importsmiles`.

        Parameters
        ----------
        arg_1
        arg_2
        arg_3
        arg_4
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
        arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_2: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `inchi`.

        Parameters
        ----------
        arg_1
        arg_2
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, **kwargs)
        self.packagenames = ("bingo",)


class inchikey(GenericFunction):
    inherit_cache = True
    name = "inchikey"

    def __init__(self, arg_1: str | sqltypes.Text, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `inchikey`.

        Parameters
        ----------
        arg_1
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(arg_1, **kwargs)
        self.packagenames = ("bingo",)


class matchexact(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "matchexact"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `matchexact`.

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
        """Calls the rdkit cartridge function `matchgross`.

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
        """Calls the rdkit cartridge function `matchrexact`.

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
        """Calls the rdkit cartridge function `matchrsmarts`.

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
        """Calls the rdkit cartridge function `matchrsub`.

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
        """Calls the rdkit cartridge function `matchsim`.

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
        """Calls the rdkit cartridge function `matchsmarts`.

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
        """Calls the rdkit cartridge function `matchsub`.

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
        self, arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        """Calls the rdkit cartridge function `molfile`.

        Parameters
        ----------
        arg_1
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(arg_1, **kwargs)
        self.packagenames = ("bingo",)


class precachedatabase(GenericFunction):
    inherit_cache = True
    name = "precachedatabase"

    def __init__(
        self, arg_1: str | sqltypes.Text, arg_2: str | sqltypes.Text, **kwargs: Any
    ) -> None:
        """Calls the rdkit cartridge function `precachedatabase`.

        Parameters
        ----------
        arg_1
        arg_2
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
        self, arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        """Calls the rdkit cartridge function `rcml`.

        Parameters
        ----------
        arg_1
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(arg_1, **kwargs)
        self.packagenames = ("bingo",)


class rfingerprint(GenericFunction):
    inherit_cache = True
    name = "rfingerprint"

    def __init__(
        self,
        arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_2: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `rfingerprint`.

        Parameters
        ----------
        arg_1
        arg_2
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[bytes | sqltypes.LargeBinary]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, **kwargs)
        self.packagenames = ("bingo",)


class rsmiles(GenericFunction):
    inherit_cache = True
    name = "rsmiles"

    def __init__(
        self, arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        """Calls the rdkit cartridge function `rsmiles`.

        Parameters
        ----------
        arg_1
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(arg_1, **kwargs)
        self.packagenames = ("bingo",)


class rxnfile(GenericFunction):
    inherit_cache = True
    name = "rxnfile"

    def __init__(
        self, arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        """Calls the rdkit cartridge function `rxnfile`.

        Parameters
        ----------
        arg_1
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(arg_1, **kwargs)
        self.packagenames = ("bingo",)


class smiles(GenericFunction):
    inherit_cache = True
    name = "smiles"

    def __init__(
        self, arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        """Calls the rdkit cartridge function `smiles`.

        Parameters
        ----------
        arg_1
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(arg_1, **kwargs)
        self.packagenames = ("bingo",)


class standardize(GenericFunction):
    inherit_cache = True
    name = "standardize"

    def __init__(
        self,
        arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_2: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `standardize`.

        Parameters
        ----------
        arg_1
        arg_2
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, **kwargs)
        self.packagenames = ("bingo",)
