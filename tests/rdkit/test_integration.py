"""Integration tests for rdkit query structure."""

from sqlalchemy import (
    Column,
    Computed,
    Integer,
    MetaData,
    String,
    Table,
    and_,
    or_,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from molalchemy.rdkit import functions as rdkit_func
from molalchemy.rdkit.index import RdkitIndex
from molalchemy.rdkit.types import RdkitMol, RdkitSparseFingerprint


class TestRdkitQueryIntegration:
    """Integration tests for complete rdkit query structures."""

    def setup_method(self):
        """Set up test tables."""
        self.metadata = MetaData()

        self.molecules = Table(
            "molecules",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("mol", RdkitMol()),
            Column(
                "morgan_fp",
                RdkitSparseFingerprint(),
                Computed("morganbv_fp(mol)"),
            ),
            RdkitIndex("idx_molecules_mol", "mol"),
        )

    def test_complete_substructure_query(self):
        """Test substructure query compiles with @> operator."""
        benzene = "c1ccccc1"

        stmt = select(self.molecules).where(
            self.molecules.c.mol.has_substructure(benzene)
        )

        compiled = str(stmt.compile())
        assert "@>" in compiled
        assert "mol_from_pkl" in compiled

    def test_exact_match_query(self):
        """Test exact match query compiles with @= operator."""
        ethanol = "CCO"

        stmt = select(self.molecules).where(self.molecules.c.mol.equals(ethanol))

        compiled = str(stmt.compile())
        assert "@=" in compiled
        assert "mol_from_pkl" in compiled

    def test_tanimoto_similarity_query(self):
        """Test tanimoto similarity compiles with % operator."""
        query_fp = "morganbv_fp('CCO'::mol)"

        stmt = select(self.molecules).where(
            self.molecules.c.morgan_fp.tanimoto(query_fp)
        )

        compiled = str(stmt.compile())
        assert "%" in compiled

    def test_dice_similarity_query(self):
        """Test dice similarity compiles with # operator."""
        query_fp = "morganbv_fp('CCO'::mol)"

        stmt = select(self.molecules).where(self.molecules.c.morgan_fp.dice(query_fp))

        compiled = str(stmt.compile())
        assert "#" in compiled

    def test_nearest_neighbors_query(self):
        """Test nearest neighbors compiles with <%> operator."""
        query_fp = "morganbv_fp('CCO'::mol)"

        stmt = select(self.molecules).where(
            self.molecules.c.morgan_fp.nearest_neighbors(query_fp)
        )

        compiled = str(stmt.compile())
        assert "<%>" in compiled

    def test_complex_query_with_multiple_conditions(self):
        """Test complex query with or_/and_ combinations."""
        benzene = "c1ccccc1"
        ethanol = "CCO"

        stmt = select(self.molecules).where(
            or_(
                self.molecules.c.mol.has_substructure(benzene),
                and_(
                    self.molecules.c.mol.equals(ethanol),
                    self.molecules.c.name == "Ethanol",
                ),
            )
        )

        compiled = str(stmt.compile())
        assert "@>" in compiled
        assert "@=" in compiled
        assert "mol_from_pkl" in compiled


class TestRdkitORMIntegration:
    """Integration tests using ORM-style definitions."""

    def setup_method(self):
        """Set up ORM models."""

        class Base(DeclarativeBase):
            pass

        class Molecule(Base):
            __tablename__ = "molecules"

            id: Mapped[int] = mapped_column(Integer, primary_key=True)
            name: Mapped[str] = mapped_column(String(100))
            mol: Mapped[str] = mapped_column(RdkitMol())
            morgan_fp: Mapped[bytes] = mapped_column(
                RdkitSparseFingerprint(),
                Computed("morganbv_fp(mol)"),
            )

            __table_args__ = (RdkitIndex("idx_molecules_mol", "mol"),)

        self.Base = Base
        self.Molecule = Molecule

    def test_orm_substructure_query(self):
        """Test substructure query with ORM."""
        benzene = "c1ccccc1"

        stmt = select(self.Molecule).where(self.Molecule.mol.has_substructure(benzene))

        compiled = str(stmt.compile())
        assert "@>" in compiled
        assert "mol_from_pkl" in compiled

    def test_orm_similarity_query(self):
        """Test similarity query with ORM."""
        query_fp = "morganbv_fp('CCO'::mol)"

        stmt = select(self.Molecule).where(self.Molecule.morgan_fp.tanimoto(query_fp))

        compiled = str(stmt.compile())
        assert "%" in compiled

    def test_orm_tanimoto_sml_function(self):
        """Test tanimoto_sml function in query."""
        stmt = select(
            self.Molecule,
            rdkit_func.tanimoto_sml(
                self.Molecule.morgan_fp,
                rdkit_func.morganbv_fp("CCO"),
            ).label("similarity"),
        )

        compiled = str(stmt.compile())
        assert "tanimoto_sml" in compiled
        assert "morganbv_fp" in compiled
