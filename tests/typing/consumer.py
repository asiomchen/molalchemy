"""Static consumer contract for MolAlchemy's shipped typing surface."""

from rdkit import Chem
from rdkit.Chem.rdChemReactions import ChemicalReaction
from sqlalchemy import Column, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import ColumnElement
from typing_extensions import assert_type

from molalchemy.bingo.functions import (
    getsimilarity,
    mol_has_substructure as bingo_has_substructure,
)
from molalchemy.bingo.types import (
    BingoBinaryMol,
    BingoBinaryReaction,
    BingoMol,
    BingoReaction,
)
from molalchemy.rdkit.functions import (
    mol_from_smiles,
    mol_has_substructure as rdkit_has_substructure,
    morganbv_fp,
    reaction_from_smarts,
)
from molalchemy.rdkit.types import (
    RdkitBitFingerprint,
    RdkitMol,
    RdkitQMol,
    RdkitReaction,
    RdkitSparseFingerprint,
    RdkitXQMol,
)
from molalchemy.types import CString


assert_type(RdkitMol(), RdkitMol[str])
assert_type(RdkitMol(return_type="smiles"), RdkitMol[str])
assert_type(RdkitMol(return_type="bytes"), RdkitMol[bytes])
assert_type(RdkitMol(return_type="mol"), RdkitMol[Chem.Mol])
assert_type(RdkitReaction(), RdkitReaction[str])
assert_type(RdkitReaction(return_type="bytes"), RdkitReaction[bytes])
assert_type(
    RdkitReaction(return_type="mol"), RdkitReaction[ChemicalReaction]
)
assert_type(BingoBinaryMol(), BingoBinaryMol[str])
assert_type(BingoBinaryMol(return_type="molfile"), BingoBinaryMol[str])
assert_type(BingoBinaryMol(return_type="bytes"), BingoBinaryMol[bytes])

assert_type(Column(CString()), Column[str])
assert_type(Column(RdkitBitFingerprint()), Column[bytes])
assert_type(Column(RdkitSparseFingerprint()), Column[bytes])
assert_type(Column(RdkitQMol()), Column[str])
assert_type(Column(RdkitXQMol()), Column[str])
assert_type(Column(BingoMol()), Column[str])
assert_type(Column(BingoReaction()), Column[str])
assert_type(Column(BingoBinaryReaction()), Column[bytes])
assert_type(select(Column(RdkitMol())), Select[tuple[str]])
assert_type(
    select(Column(RdkitMol(return_type="mol"))), Select[tuple[Chem.Mol]]
)


class Base(DeclarativeBase):
    pass


class Molecule(Base):
    __tablename__ = "typing_molecule"

    id: Mapped[int] = mapped_column(primary_key=True)
    rdkit_mol: Mapped[str] = mapped_column(RdkitMol())
    bingo_mol: Mapped[str] = mapped_column(BingoMol())


assert_type(
    rdkit_has_substructure(Molecule.rdkit_mol, "c1ccccc1"), ColumnElement[bool]
)
assert_type(
    bingo_has_substructure(Molecule.bingo_mol, "c1ccccc1"), ColumnElement[bool]
)
assert_type(select(mol_from_smiles("CCO")), Select[tuple[str]])
assert_type(select(morganbv_fp(Molecule.rdkit_mol)), Select[tuple[bytes]])
assert_type(select(reaction_from_smarts("CCO>>CC=O")), Select[tuple[str]])
assert_type(
    select(getsimilarity(Molecule.bingo_mol, "CCO")), Select[tuple[float]]
)
