from sqlalchemy import text
from sqlalchemy.sql import ColumnElement
from sqlalchemy.sql import func
from sqlalchemy.sql.functions import Function
from typing import Literal

_WEIGHT_TYPES = Literal["molecular-weight", "most-abundant-mass", "monoisotopic"]
_AAM_STRATEGIES = Literal["CLEAR", "DISCARD", "ALTER", "KEEP"]


class bingo_func:
    """
    Collection of Bingo PostgreSQL functions for molecular structure search and analysis.

    This class provides static methods that wrap Bingo PostgreSQL functions for performing
    various chemical structure operations including substructure search, exact matching,
    similarity search, and format conversions.
    """

    @staticmethod
    def has_substructure(mol_column: ColumnElement, query: str, parameters: str = ""):
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

        Examples
        --------
        >>> # Find molecules containing benzene ring
        >>> session.query(MoleculeTable).filter(
        ...     bingo_func.has_substructure(MoleculeTable.structure, "c1ccccc1")
        ... )
        """
        return mol_column.op("@")(text(f"('{query}', '{parameters}')::bingo.sub"))

    @staticmethod
    def matches_smarts(mol_column: ColumnElement, query: str, parameters: str = ""):
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

        Examples
        --------
        >>> # Find molecules with carbonyl group
        >>> session.query(MoleculeTable).filter(
        ...     bingo_func.matches_smarts(MoleculeTable.structure, "[C]=[O]")
        ... )
        """
        return mol_column.op("@")(text(f"('{query}', '{parameters}')::bingo.smarts"))

    @staticmethod
    def equals(mol_column: ColumnElement, query: str, parameters: str = ""):
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

        Examples
        --------
        >>> # Find exact matches for aspirin
        >>> session.query(MoleculeTable).filter(
        ...     bingo_func.equals(MoleculeTable.structure, "CC(=O)Oc1ccccc1C(=O)O")
        ... )
        """
        return mol_column.op("@")(text(f"('{query}', '{parameters}')::bingo.exact"))

    @staticmethod
    def similarity(
        mol_column: ColumnElement,
        query: str,
        bottom: float = 0.0,
        top: float = 1.0,
        metric: str = "Tanimoto",
    ):
        """
        Perform similarity search on a molecule column.

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

        Examples
        --------
        >>> # Find molecules with Tanimoto similarity >= 0.7 to benzene
        >>> session.query(MoleculeTable).filter(
        ...     bingo_func.similarity(MoleculeTable.structure, "c1ccccc1", bottom=0.7)
        ... )
        """
        return mol_column.op("%")(
            text(f"('{query}', {bottom}, {top}, '{metric}')::bingo.sim")
        )

    @staticmethod
    def has_gross_formula(mol_column: ColumnElement, formula: str):
        """
        Search for molecules with a specific gross formula.

        Parameters
        ----------
        mol_column : ColumnElement
            SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
        formula : str
            Gross formula string (e.g., "C6H6" for benzene).

        Returns
        -------
        BinaryExpression
            SQLAlchemy expression for gross formula matching that can be used in WHERE clauses.

        Examples
        --------
        >>> # Find all molecules with formula C6H6
        >>> session.query(MoleculeTable).filter(
        ...     bingo_func.has_gross_formula(MoleculeTable.structure, "C6H6")
        ... )
        """
        return mol_column.op("@")(text(f"('{formula}')::bingo.gross"))

    @staticmethod
    def get_weight(
        mol_column: ColumnElement, weight_type: _WEIGHT_TYPES = "molecular-weight"
    ):
        """
        Calculate molecular weight of molecules.

        Parameters
        ----------
        mol_column : ColumnElement
            SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
        weight_type : {"molecular-weight", "most-abundant-mass", "monoisotopic"}, optional
            Type of molecular weight to calculate (default is "molecular-weight").

        Returns
        -------
        Function[float]
            SQLAlchemy function expression returning the molecular weight.

        Examples
        --------
        >>> # Get molecular weights of all molecules
        >>> session.query(
        ...     MoleculeTable.id,
        ...     bingo_func.get_weight(MoleculeTable.structure)
        ... )
        """
        return func.Bingo.getWeight(mol_column, weight_type)

    @staticmethod
    def gross_formula(mol_column: ColumnElement) -> Function[str]:
        """
        Calculate the gross formula of molecules.

        Parameters
        ----------
        mol_column : ColumnElement
            SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).

        Returns
        -------
        Function[str]
            SQLAlchemy function expression returning the gross formula as a string.

        Examples
        --------
        >>> # Get gross formulas of all molecules
        >>> session.query(
        ...     MoleculeTable.id,
        ...     bingo_func.gross_formula(MoleculeTable.structure)
        ... )
        """
        return func.Bingo.Gross(mol_column)

    @staticmethod
    def check_molecule(mol_column: ColumnElement) -> Function[str | None]:
        """
        Check if molecules are valid and return error messages for invalid ones.

        Parameters
        ----------
        mol_column : ColumnElement
            SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).

        Returns
        -------
        Function[str | None]
            SQLAlchemy function expression returning None for valid molecules,
            or an error message string for invalid molecules.

        Examples
        --------
        >>> # Find invalid molecules in the table
        >>> invalid_mols = session.query(MoleculeTable).filter(
        ...     bingo_func.check_molecule(MoleculeTable.structure).isnot(None)
        ... )
        """
        return func.Bingo.CheckMolecule(mol_column)

    @staticmethod
    def to_canonical(mol_column: ColumnElement) -> Function[str]:
        """
        Convert molecules to canonical SMILES format.

        Parameters
        ----------
        mol_column : ColumnElement
            SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).

        Returns
        -------
        Function[str]
            SQLAlchemy function expression returning canonical SMILES strings.

        Examples
        --------
        >>> # Get canonical SMILES for all molecules
        >>> session.query(
        ...     MoleculeTable.id,
        ...     bingo_func.to_canonical(MoleculeTable.structure)
        ... )
        """
        return func.Bingo.CanSMILES(mol_column)

    @staticmethod
    def to_inchi(mol_column: ColumnElement) -> Function[str]:
        """
        Convert molecules to InChI format.

        Parameters
        ----------
        mol_column : ColumnElement
            SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).

        Returns
        -------
        Function[str]
            SQLAlchemy function expression returning InChI strings.

        Examples
        --------
        >>> # Get InChI for all molecules
        >>> session.query(
        ...     MoleculeTable.id,
        ...     bingo_func.to_inchi(MoleculeTable.structure)
        ... )
        """
        return func.bingo.InChI(mol_column)

    @staticmethod
    def to_inchikey(mol_column: ColumnElement) -> Function[str]:
        """
        Convert molecules to InChIKey format.

        Parameters
        ----------
        mol_column : ColumnElement
            SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).

        Returns
        -------
        Function[str]
            SQLAlchemy function expression returning InChIKey strings.

        Examples
        --------
        >>> # Get InChIKey for all molecules
        >>> session.query(
        ...     MoleculeTable.id,
        ...     bingo_func.to_inchikey(MoleculeTable.structure)
        ... )
        """
        return func.Bingo.InChIKey(mol_column)

    @staticmethod
    def to_binary(
        mol_column: ColumnElement, preserve_pos: bool = True
    ) -> Function[bytes]:
        """
        Convert molecules to Bingo's internal binary format.

        Parameters
        ----------
        mol_column : ColumnElement
            SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).
        preserve_pos : bool, optional
            Whether to preserve atom positions in the binary format (default is True).
            If False, only connectivity information is stored.

        Returns
        -------
        Function[bytes]
            SQLAlchemy function expression returning binary data.

        Examples
        --------
        >>> # Convert molecules to compact binary format
        >>> session.query(
        ...     MoleculeTable.id,
        ...     bingo_func.to_binary(MoleculeTable.structure)
        ... )
        """
        return func.Bingo.CompactMolecule(mol_column, preserve_pos)

    @staticmethod
    def to_smiles(mol_column: ColumnElement) -> Function[str]:
        """
        Convert molecules to SMILES format.

        Parameters
        ----------
        mol_column : ColumnElement
            SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).

        Returns
        -------
        Function[str]
            SQLAlchemy function expression returning SMILES strings.

        Examples
        --------
        >>> # Get SMILES for all molecules
        >>> session.query(
        ...     MoleculeTable.id,
        ...     bingo_func.to_smiles(MoleculeTable.structure)
        ... )
        """
        return func.Bingo.SMILES(mol_column)

    @staticmethod
    def to_molfile(mol_column: ColumnElement) -> Function[str]:
        """
        Convert molecules to Molfile format.

        Parameters
        ----------
        mol_column : ColumnElement
            SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).

        Returns
        -------
        Function[str]
            SQLAlchemy function expression returning Molfile strings with 2D coordinates.

        Examples
        --------
        >>> # Get Molfile for all molecules
        >>> session.query(
        ...     MoleculeTable.id,
        ...     bingo_func.to_molfile(MoleculeTable.structure)
        ... )
        """
        return func.Bingo.Molfile(mol_column)

    @staticmethod
    def to_cml(mol_column: ColumnElement) -> Function[str]:
        """
        Convert molecules to CML (Chemical Markup Language) format.

        Parameters
        ----------
        mol_column : ColumnElement
            SQLAlchemy column containing molecule data (SMILES, Molfile, or binary).

        Returns
        -------
        Function[str]
            SQLAlchemy function expression returning CML strings.

        Examples
        --------
        >>> # Get CML for all molecules
        >>> session.query(
        ...     MoleculeTable.id,
        ...     bingo_func.to_cml(MoleculeTable.structure)
        ... )
        """
        return func.Bingo.CML(mol_column)


class bingo_rxn_func:
    """
    Collection of Bingo PostgreSQL functions for reaction structure search and analysis.

    This class provides static methods that wrap Bingo PostgreSQL functions for performing
    various chemical reaction operations including reaction substructure search, exact matching,
    and format conversions.
    """

    @staticmethod
    def equals(rxn_column: ColumnElement, query: str, parameters: str = ""):
        """
        Perform exact reaction matching on a reaction column.

        Parameters
        ----------
        rxn_column : ColumnElement
            SQLAlchemy column containing reaction data (reaction SMILES, Rxnfile, or binary).
        query : str
            Query reaction as reaction SMILES or Rxnfile string for exact matching.
        parameters : str, optional
            Search parameters for customizing the matching behavior (default is "").

        Returns
        -------
        BinaryExpression
            SQLAlchemy expression for exact reaction matching that can be used in WHERE clauses.

        Examples
        --------
        >>> # Find exact matches for a specific reaction
        >>> session.query(ReactionTable).filter(
        ...     bingo_rxn_func.equals(ReactionTable.structure, "CCO>>CC=O")
        ... )
        """
        return rxn_column.op("@")(text(f"('{query}', '{parameters}')::bingo.rexact"))

    @staticmethod
    def has_reaction_smarts(
        rxn_column: ColumnElement, query: str, parameters: str = ""
    ):
        """
        Perform reaction SMARTS pattern matching on a reaction column.

        Parameters
        ----------
        rxn_column : ColumnElement
            SQLAlchemy column containing reaction data (reaction SMILES, Rxnfile, or binary).
        query : str
            Reaction SMARTS pattern string for matching.
        parameters : str, optional
            Search parameters for customizing the matching behavior (default is "").

        Returns
        -------
        BinaryExpression
            SQLAlchemy expression for reaction SMARTS matching that can be used in WHERE clauses.

        Examples
        --------
        >>> # Find reactions with carbonyl reduction pattern
        >>> session.query(ReactionTable).filter(
        ...     bingo_rxn_func.has_reaction_smarts(ReactionTable.structure, "[C]=[O]>>[C]-[O]")
        ... )
        """
        return rxn_column.op("@")(text(f"('{query}', '{parameters}')::bingo.rsmarts"))

    @staticmethod
    def has_reaction_substructure(
        rxn_column: ColumnElement, query: str, parameters: str = ""
    ):
        """
        Perform reaction substructure search on a reaction column.

        Parameters
        ----------
        rxn_column : ColumnElement
            SQLAlchemy column containing reaction data (reaction SMILES, Rxnfile, or binary).
        query : str
            Query reaction as reaction SMILES or Rxnfile string for substructure matching.
        parameters : str, optional
            Search parameters for customizing the matching behavior (default is "").

        Returns
        -------
        BinaryExpression
            SQLAlchemy expression for reaction substructure matching that can be used in WHERE clauses.

        Examples
        --------
        >>> # Find reactions containing oxidation pattern
        >>> session.query(ReactionTable).filter(
        ...     bingo_rxn_func.has_reaction_substructure(ReactionTable.structure, "CO>>C=O")
        ... )
        """
        return rxn_column.op("@")(text(f"('{query}', '{parameters}')::bingo.rsub"))

    @staticmethod
    def to_binary(
        rxn_column: ColumnElement, preserve_pos: bool = True
    ) -> Function[bytes]:
        """
        Convert reactions to Bingo's internal binary format.

        Parameters
        ----------
        rxn_column : ColumnElement
            SQLAlchemy column containing reaction data (reaction SMILES, Rxnfile, or binary).
        preserve_pos : bool, optional
            Whether to preserve atom positions in the binary format (default is True).
            If False, only connectivity information is stored.

        Returns
        -------
        Function[bytes]
            SQLAlchemy function expression returning binary data.

        Examples
        --------
        >>> # Convert reactions to compact binary format
        >>> session.query(
        ...     ReactionTable.id,
        ...     bingo_rxn_func.to_binary(ReactionTable.structure)
        ... )
        """
        return func.Bingo.CompactReaction(rxn_column, preserve_pos)

    @staticmethod
    def to_smiles(rxn_column: ColumnElement) -> Function[str]:
        """
        Convert reactions to reaction SMILES format.

        Parameters
        ----------
        rxn_column : ColumnElement
            SQLAlchemy column containing reaction data (reaction SMILES, Rxnfile, or binary).

        Returns
        -------
        Function[str]
            SQLAlchemy function expression returning reaction SMILES strings.

        Examples
        --------
        >>> # Get reaction SMILES for all reactions
        >>> session.query(
        ...     ReactionTable.id,
        ...     bingo_rxn_func.to_smiles(ReactionTable.structure)
        ... )
        """
        return func.Bingo.RSMILES(rxn_column)

    @staticmethod
    def to_rxnfile(rxn_column: ColumnElement) -> Function[str]:
        """
        Convert reactions to Rxnfile format.

        Parameters
        ----------
        rxn_column : ColumnElement
            SQLAlchemy column containing reaction data (reaction SMILES, Rxnfile, or binary).

        Returns
        -------
        Function[str]
            SQLAlchemy function expression returning Rxnfile strings with 2D coordinates.

        Examples
        --------
        >>> # Get Rxnfile for all reactions
        >>> session.query(
        ...     ReactionTable.id,
        ...     bingo_rxn_func.to_rxnfile(ReactionTable.structure)
        ... )
        """
        return func.Bingo.Rxnfile(rxn_column)

    @staticmethod
    def to_cml(rxn_column: ColumnElement) -> Function[str]:
        """
        Convert reactions to CML (Chemical Markup Language) format.

        Parameters
        ----------
        rxn_column : ColumnElement
            SQLAlchemy column containing reaction data (reaction SMILES, Rxnfile, or binary).

        Returns
        -------
        Function[str]
            SQLAlchemy function expression returning CML strings.

        Examples
        --------
        >>> # Get CML for all reactions
        >>> session.query(
        ...     ReactionTable.id,
        ...     bingo_rxn_func.to_cml(ReactionTable.structure)
        ... )
        """
        return func.Bingo.RCML(rxn_column)

    @staticmethod
    def map_atoms(
        rxn_column: ColumnElement, strategy: _AAM_STRATEGIES = "KEEP"
    ) -> Function[str]:
        """
        Perform automatic atom-to-atom mapping (AAM) on reactions.

        Parameters
        ----------
        rxn_column : ColumnElement
            SQLAlchemy column containing reaction data (reaction SMILES, Rxnfile, or binary).
        strategy : {"CLEAR", "DISCARD", "ALTER", "KEEP"}, optional
            Strategy for handling existing atom mapping (default is "KEEP").
            - "CLEAR": Remove all existing mappings and compute new ones
            - "DISCARD": Remove all mappings without computing new ones
            - "ALTER": Modify existing mappings
            - "KEEP": Keep existing mappings and map unmapped atoms

        Returns
        -------
        Function[str]
            SQLAlchemy function expression returning reaction with atom mapping.

        Examples
        --------
        >>> # Add atom mapping to reactions
        >>> session.query(
        ...     ReactionTable.id,
        ...     bingo_rxn_func.map_atoms(ReactionTable.structure, "CLEAR")
        ... )
        """
        return func.Bingo.AAM(rxn_column, strategy)
