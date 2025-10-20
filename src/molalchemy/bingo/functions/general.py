"""Auto-generated from data/bingo_functions.json. Do not edit manually."""

from typing import Any, Literal

from sqlalchemy import types as sqltypes
from sqlalchemy.sql import text
from sqlalchemy.sql.elements import BinaryExpression, ColumnElement
from sqlalchemy.sql.functions import GenericFunction

from molalchemy.bingo.types import BingoBinaryMol, BingoMol

AnyBingoMol = BingoMol | BingoBinaryMol


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


def equals(mol_column: ColumnElement[AnyBingoMol], query: str, parameters: str = ""):
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
    """
    Creates an atom-atom mapping for a reaction.


    Parameters
    ----------
    rxn: str | sqltypes.Text | bytes | sqltypes.LargeBinary
        Input reaction
    strategy: sqltypes.Text | Literal['CLEAR', 'DISCARD', 'ALTER', 'KEEP'] = 'KEEP'
        Strategy for handling existing atom mapping (default is 'KEEP').
                - 'CLEAR': Remove all existing mappings and compute new ones
                - 'DISCARD': Remove all mappings without computing new ones
                - 'ALTER': Modify existing mappings
                - 'KEEP': Keep existing mappings and map unmapped atoms


    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        rxn: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        strategy: sqltypes.Text | Literal["CLEAR", "DISCARD", "ALTER", "KEEP"] = "KEEP",
        **kwargs: Any,
    ) -> None:
        super().__init__(rxn, strategy, **kwargs)


class cansmiles(GenericFunction):
    """
    Generates the canonical SMILES for a molecule.


    Parameters
    ----------
    mol: str | sqltypes.Text | bytes | sqltypes.LargeBinary
        Input molecule in any supported format


    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self, mol: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        super().__init__(mol, **kwargs)


class checkmolecule(GenericFunction):
    """
    Check molecule for validity


    Parameters
    ----------
    mol: str | sqltypes.Text | bytes | sqltypes.LargeBinary
        Input molecule in any supported format


    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self, mol: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        super().__init__(mol, **kwargs)


class checkreaction(GenericFunction):
    """
    Check reaction for validity


    Parameters
    ----------
    rxn: str | sqltypes.Text | bytes | sqltypes.LargeBinary
        Input reaction in any supported format


    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self, rxn: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        super().__init__(rxn, **kwargs)


class cml(GenericFunction):
    """
    Converts a molecule to CML format.


    Parameters
    ----------
    mol: str | sqltypes.Text | bytes | sqltypes.LargeBinary
        Input molecule in any supported format


    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self, mol: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        super().__init__(mol, **kwargs)


class compactmolecule(GenericFunction):
    """
    Calculates the compact representation of a molecule.


    Parameters
    ----------
    mol: str | sqltypes.Text | bytes | sqltypes.LargeBinary
        Input molecule in any supported format
    arg_2: sqltypes.Boolean



    Returns
    -------
    Function[bytes | sqltypes.LargeBinary]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        mol: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_2: sqltypes.Boolean,
        **kwargs: Any,
    ) -> None:
        super().__init__(mol, arg_2, **kwargs)


class compactreaction(GenericFunction):
    """
    Calls the rdkit cartridge function `compactreaction`.


    Parameters
    ----------
    rxn: str | sqltypes.Text | bytes | sqltypes.LargeBinary
        Input reaction in any supported format
    arg_2: sqltypes.Boolean | bool



    Returns
    -------
    Function[bytes | sqltypes.LargeBinary]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        rxn: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_2: sqltypes.Boolean | bool,
        **kwargs: Any,
    ) -> None:
        super().__init__(rxn, arg_2, **kwargs)


class exportrdf(GenericFunction):
    """
    Exports reactions to an RDF format.


    Parameters
    ----------
    arg_1: str | sqltypes.Text

    arg_2: str | sqltypes.Text

    arg_3: str | sqltypes.Text

    arg_4: str | sqltypes.Text



    Returns
    -------
    Function[None | sqltypes.NullType]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text,
        arg_3: str | sqltypes.Text,
        arg_4: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, arg_3, arg_4, **kwargs)


class exportsdf(GenericFunction):
    """
    Exports molecules to an SDF format.


    Parameters
    ----------
    mol: str | sqltypes.Text
        Input molecule in any supported format
    arg_2: str | sqltypes.Text

    arg_3: str | sqltypes.Text

    arg_4: str | sqltypes.Text



    Returns
    -------
    Function[None | sqltypes.NullType]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        mol: str | sqltypes.Text,
        arg_2: str | sqltypes.Text,
        arg_3: str | sqltypes.Text,
        arg_4: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(mol, arg_2, arg_3, arg_4, **kwargs)


class filetoblob(GenericFunction):
    """
    Calls the rdkit cartridge function `filetoblob`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text



    Returns
    -------
    Function[bytes | sqltypes.LargeBinary]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(self, arg_1: str | sqltypes.Text, **kwargs: Any) -> None:
        super().__init__(arg_1, **kwargs)


class filetotext(GenericFunction):
    """
    Calls the rdkit cartridge function `filetotext`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text



    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(self, arg_1: str | sqltypes.Text, **kwargs: Any) -> None:
        super().__init__(arg_1, **kwargs)


class fingerprint(GenericFunction):
    """
    Calls the rdkit cartridge function `fingerprint`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary

    arg_2: str | sqltypes.Text



    Returns
    -------
    Function[bytes | sqltypes.LargeBinary]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_2: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, **kwargs)


class getblockcount(GenericFunction):
    """
    Calls the rdkit cartridge function `getblockcount`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text



    Returns
    -------
    Function[int | sqltypes.Integer]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(self, arg_1: str | sqltypes.Text, **kwargs: Any) -> None:
        super().__init__(arg_1, **kwargs)


class getindexstructurescount(GenericFunction):
    """
    Calls the rdkit cartridge function `getindexstructurescount`.


    Parameters
    ----------



    Returns
    -------
    Function[int | sqltypes.Integer]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class getmass(GenericFunction):
    """
    Calls the rdkit cartridge function `getmass`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary



    Returns
    -------
    Function[float | sqltypes.Float]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self, arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        super().__init__(arg_1, **kwargs)


class getname(GenericFunction):
    """
    Calls the rdkit cartridge function `getname`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text



    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(self, arg_1: str | sqltypes.Text, **kwargs: Any) -> None:
        super().__init__(arg_1, **kwargs)


class getsimilarity(GenericFunction):
    """
    Calls the rdkit cartridge function `getsimilarity`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary

    arg_2: str | sqltypes.Text

    arg_3: str | sqltypes.Text



    Returns
    -------
    Function[float | sqltypes.Float]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_2: str | sqltypes.Text,
        arg_3: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, arg_3, **kwargs)


class getstructurescount(GenericFunction):
    """
    Calls the rdkit cartridge function `getstructurescount`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text



    Returns
    -------
    Function[int | sqltypes.Integer]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(self, arg_1: str | sqltypes.Text, **kwargs: Any) -> None:
        super().__init__(arg_1, **kwargs)


class getversion(GenericFunction):
    """
    Calls the rdkit cartridge function `getversion`.


    Parameters
    ----------



    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class getweight(GenericFunction):
    """
    Calls the rdkit cartridge function `getweight`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary

    arg_2: str | sqltypes.Text



    Returns
    -------
    Function[float | sqltypes.Float]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_2: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, **kwargs)


class gross(GenericFunction):
    """
    Calls the rdkit cartridge function `gross`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary



    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self, arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        super().__init__(arg_1, **kwargs)


class importrdf(GenericFunction):
    """
    Calls the rdkit cartridge function `importrdf`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text

    arg_2: str | sqltypes.Text

    arg_3: str | sqltypes.Text

    arg_4: str | sqltypes.Text



    Returns
    -------
    Function[None | sqltypes.NullType]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text,
        arg_3: str | sqltypes.Text,
        arg_4: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, arg_3, arg_4, **kwargs)


class importsdf(GenericFunction):
    """
    Calls the rdkit cartridge function `importsdf`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text

    arg_2: str | sqltypes.Text

    arg_3: str | sqltypes.Text

    arg_4: str | sqltypes.Text



    Returns
    -------
    Function[None | sqltypes.NullType]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text,
        arg_3: str | sqltypes.Text,
        arg_4: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, arg_3, arg_4, **kwargs)


class importsmiles(GenericFunction):
    """
    Calls the rdkit cartridge function `importsmiles`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text

    arg_2: str | sqltypes.Text

    arg_3: str | sqltypes.Text

    arg_4: str | sqltypes.Text



    Returns
    -------
    Function[None | sqltypes.NullType]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text,
        arg_3: str | sqltypes.Text,
        arg_4: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, arg_3, arg_4, **kwargs)


class inchi(GenericFunction):
    """
    Calls the rdkit cartridge function `inchi`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary

    arg_2: str | sqltypes.Text



    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_2: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, **kwargs)


class inchikey(GenericFunction):
    """
    Calls the rdkit cartridge function `inchikey`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text



    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(self, arg_1: str | sqltypes.Text, **kwargs: Any) -> None:
        super().__init__(arg_1, **kwargs)


class matchexact(GenericFunction):
    """
    Calls the rdkit cartridge function `matchexact`.


    Parameters
    ----------



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class matchgross(GenericFunction):
    """
    Calls the rdkit cartridge function `matchgross`.


    Parameters
    ----------



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class matchrexact(GenericFunction):
    """
    Calls the rdkit cartridge function `matchrexact`.


    Parameters
    ----------



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class matchrsmarts(GenericFunction):
    """
    Calls the rdkit cartridge function `matchrsmarts`.


    Parameters
    ----------



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class matchrsub(GenericFunction):
    """
    Calls the rdkit cartridge function `matchrsub`.


    Parameters
    ----------



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class matchsim(GenericFunction):
    """
    Calls the rdkit cartridge function `matchsim`.


    Parameters
    ----------



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class matchsmarts(GenericFunction):
    """
    Calls the rdkit cartridge function `matchsmarts`.


    Parameters
    ----------



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class matchsub(GenericFunction):
    """
    Calls the rdkit cartridge function `matchsub`.


    Parameters
    ----------



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class molfile(GenericFunction):
    """
    Calls the rdkit cartridge function `molfile`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary



    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self, arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        super().__init__(arg_1, **kwargs)


class precachedatabase(GenericFunction):
    """
    Calls the rdkit cartridge function `precachedatabase`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text

    arg_2: str | sqltypes.Text



    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self, arg_1: str | sqltypes.Text, arg_2: str | sqltypes.Text, **kwargs: Any
    ) -> None:
        super().__init__(arg_1, arg_2, **kwargs)


class rcml(GenericFunction):
    """
    Calls the rdkit cartridge function `rcml`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary



    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self, arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        super().__init__(arg_1, **kwargs)


class rfingerprint(GenericFunction):
    """
    Calls the rdkit cartridge function `rfingerprint`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary

    arg_2: str | sqltypes.Text



    Returns
    -------
    Function[bytes | sqltypes.LargeBinary]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_2: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, **kwargs)


class rsmiles(GenericFunction):
    """
    Calls the rdkit cartridge function `rsmiles`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary



    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self, arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        super().__init__(arg_1, **kwargs)


class rxnfile(GenericFunction):
    """
    Calls the rdkit cartridge function `rxnfile`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary



    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self, arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        super().__init__(arg_1, **kwargs)


class smiles(GenericFunction):
    """
    Calls the rdkit cartridge function `smiles`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary



    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self, arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary, **kwargs: Any
    ) -> None:
        super().__init__(arg_1, **kwargs)


class standardize(GenericFunction):
    """
    Calls the rdkit cartridge function `standardize`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary

    arg_2: str | sqltypes.Text



    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_2: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, **kwargs)
