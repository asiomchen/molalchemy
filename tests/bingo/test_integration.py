"""Integration tests for bingo query structure."""

import re

from sqlalchemy import Column, Integer, MetaData, String, Table, and_, or_, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from molalchemy.bingo import functions as bingo_func
from molalchemy.bingo.index import BingoBinaryMolIndex, BingoMolIndex
from molalchemy.bingo.types import BingoBinaryMol, BingoMol


class TestBingoQueryIntegration:
    """Integration tests for complete bingo query structures."""

    def setup_method(self):
        """Set up test tables and data."""
        self.metadata = MetaData()

        # Core API table
        self.compounds = Table(
            "compounds",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("structure", BingoMol()),
            BingoMolIndex("idx_compounds_structure", "structure"),
        )

        # Binary API table
        self.binary_compounds = Table(
            "binary_compounds",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("structure", BingoBinaryMol()),
            BingoBinaryMolIndex("idx_binary_compounds_structure", "structure"),
        )

    def test_complete_substructure_query(self):
        """Test complete substructure query using both comparator and function."""
        benzene = "c1ccccc1"

        # Query using comparator
        stmt1 = select(self.compounds).where(
            self.compounds.c.structure.has_substructure(benzene)
        )

        # Query using function
        stmt2 = select(self.compounds).where(
            bingo_func.has_substructure(self.compounds.c.structure, benzene)
        )

        # Both should compile successfully
        compiled1 = str(stmt1.compile(compile_kwargs={"literal_binds": True}))
        compiled2 = str(stmt2.compile(compile_kwargs={"literal_binds": True}))

        assert "bingo.sub" in compiled1
        assert "bingo.sub" in compiled2
        assert benzene in compiled1
        assert benzene in compiled2

    def test_complete_similarity_query(self):
        """Test complete similarity query (function only)."""
        ethanol = "CCO"

        stmt = select(self.compounds).where(
            bingo_func.similarity(self.compounds.c.structure, ethanol, 0.7, 1.0)
        )

        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "bingo.sim" in compiled
        assert ethanol in compiled
        assert "0.7" in compiled
        assert "1.0" in compiled

    def test_complex_query_with_multiple_conditions(self):
        """Test complex query with multiple bingo conditions."""
        benzene = "c1ccccc1"
        aspirin_smarts = (
            "[#6]-[#6](=[#8])-[#8]-[#6]1:[#6]:[#6]:[#6]:[#6]:[#6]:1-[#6](=[#8])-[#8]"
        )
        stmt = select(self.compounds).where(
            or_(
                self.compounds.c.structure.has_substructure(benzene),
                self.compounds.c.structure.has_smarts(aspirin_smarts),
            )
        )

        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "bingo.sub" in compiled
        assert "bingo.smarts" in compiled
        assert benzene in compiled
        assert "[#6]1" in compiled or aspirin_smarts in compiled

    def test_query_with_parameters(self):
        """Test query with bingo parameters."""
        query = "c1ccccc1"
        parameters = "max=5"

        stmt = select(self.compounds).where(
            self.compounds.c.structure.has_substructure(query, parameters)
        )

        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert query in compiled
        assert parameters in compiled
        assert "bingo.sub" in compiled
        assert re.search(r"max\s*=\s*5.*\:\:bingo\.sub", compiled)

    def test_binary_mol_query_structure(self):
        """Test query structure with binary molecule type."""
        benzene = "c1ccccc1"

        stmt = select(self.binary_compounds).where(
            self.binary_compounds.c.structure.has_substructure(benzene)
        )

        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "binary_compounds" in compiled
        assert "bingo.sub" in compiled
        assert benzene in compiled

    def test_join_with_bingo_conditions(self):
        """Test joining tables with bingo conditions."""
        # Create another table to join with
        suppliers = Table(
            "suppliers",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("compound_id", Integer),
            Column("name", String(100)),
        )

        benzene = "c1ccccc1"

        stmt = (
            select(self.compounds.c.name, suppliers.c.name.label("supplier_name"))
            .select_from(
                self.compounds.join(
                    suppliers, self.compounds.c.id == suppliers.c.compound_id
                )
            )
            .where(self.compounds.c.structure.has_substructure(benzene))
        )

        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "JOIN suppliers" in compiled
        assert "bingo.sub" in compiled
        assert benzene in compiled


class TestBingoORMIntegration:
    """Integration tests using ORM-style definitions."""

    def setup_method(self):
        """Set up ORM models."""

        class Base(DeclarativeBase):
            pass

        class Compound(Base):
            __tablename__ = "compounds"

            id: Mapped[int] = mapped_column(Integer, primary_key=True)
            name: Mapped[str] = mapped_column(String(100))
            structure: Mapped[str] = mapped_column(BingoMol())

            __table_args__ = (BingoMolIndex("idx_compounds_structure", "structure"),)

        class BinaryCompound(Base):
            __tablename__ = "binary_compounds"

            id: Mapped[int] = mapped_column(Integer, primary_key=True)
            name: Mapped[str] = mapped_column(String(100))
            structure: Mapped[bytes] = mapped_column(BingoBinaryMol())

            __table_args__ = (
                BingoBinaryMolIndex("idx_binary_compounds_structure", "structure"),
            )

        self.Base = Base
        self.Compound = Compound
        self.BinaryCompound = BinaryCompound

    def test_orm_substructure_query(self):
        """Test substructure query with ORM."""
        benzene = "c1ccccc1"

        # Using comparator
        stmt1 = select(self.Compound).where(
            self.Compound.structure.has_substructure(benzene)
        )

        # Using function
        stmt2 = select(self.Compound).where(
            bingo_func.has_substructure(self.Compound.structure, benzene)
        )

        compiled1 = str(stmt1.compile(compile_kwargs={"literal_binds": True}))
        compiled2 = str(stmt2.compile(compile_kwargs={"literal_binds": True}))

        assert "bingo.sub" in compiled1
        assert "bingo.sub" in compiled2
        assert benzene in compiled1
        assert benzene in compiled2

    def test_orm_similarity_query(self):
        """Test similarity query with ORM."""
        ethanol = "CCO"

        stmt = select(self.Compound).where(
            bingo_func.similarity(self.Compound.structure, ethanol, 0.8)
        )

        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "bingo.sim" in compiled
        assert ethanol in compiled
        assert "0.8" in compiled

    def test_orm_complex_query(self):
        """Test complex ORM query with multiple conditions."""
        benzene = "c1ccccc1"
        ethanol = "CCO"

        stmt = select(self.Compound).where(
            and_(
                self.Compound.structure.has_substructure(benzene),
                bingo_func.similarity(self.Compound.structure, ethanol, 0.5),
            )
        )

        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "bingo.sub" in compiled
        assert "bingo.sim" in compiled
        assert benzene in compiled
        assert ethanol in compiled

    def test_orm_binary_mol_query(self):
        """Test binary molecule query with ORM."""
        benzene = "c1ccccc1"

        stmt = select(self.BinaryCompound).where(
            self.BinaryCompound.structure.has_substructure(benzene)
        )

        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "binary_compounds" in compiled
        assert "bingo.sub" in compiled
        assert benzene in compiled


class TestBingoQueryVariations:
    """Test various query patterns and edge cases."""

    def setup_method(self):
        """Set up test table."""
        self.metadata = MetaData()
        self.compounds = Table(
            "compounds",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("structure", BingoMol()),
        )

    def test_query_with_special_smiles(self):
        """Test queries with special SMILES characters."""
        special_smiles = [
            "CC(=O)N[C@@H](CC1=CC=CC=C1)C(=O)O",  # Phenylalanine with stereochemistry
            "C[C@H]1CC[C@H](CC1)N(C)C",  # Complex stereochemistry
            "[Na+].[Cl-]",  # Salt
            "CC(C)C[C@H](NC(=O)[C@H](N)CC1=CC=CC=C1)C(=O)O",  # Complex peptide
        ]

        for smiles in special_smiles:
            stmt = select(self.compounds).where(
                self.compounds.c.structure.has_substructure(smiles)
            )

            # Should compile without errors
            compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
            assert "bingo.sub" in compiled
            assert smiles in compiled

    def test_query_with_different_parameters(self):
        """Test queries with various parameter combinations."""
        query = "c1ccccc1"
        parameter_sets = [
            "",
            "max=5",
            "timeout=1000",
            "max=10,timeout=5000",
            "stereochemistry=1",
        ]

        for params in parameter_sets:
            stmt = select(self.compounds).where(
                self.compounds.c.structure.has_substructure(query, params)
            )

            compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
            assert "bingo.sub" in compiled
            assert query in compiled
            if params:
                assert params in compiled

    def test_all_comparator_methods(self):
        """Test all available comparator methods in one query."""
        benzene = "c1ccccc1"
        benzene_smarts = "[#6]1-[#6]-[#6]-[#6]-[#6]-[#6]-1"  # Simplified benzene SMARTS
        ethanol = "CCO"

        stmt = select(self.compounds).where(
            or_(
                self.compounds.c.structure.has_substructure(benzene),
                self.compounds.c.structure.has_smarts(benzene_smarts),
                self.compounds.c.structure.equals(ethanol),
            )
        )

        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "bingo.sub" in compiled
        assert "bingo.smarts" in compiled
        assert "bingo.exact" in compiled
        assert benzene in compiled
        assert "[#6]1" in compiled or benzene_smarts in compiled
        assert ethanol in compiled

    def test_all_function_methods(self):
        """Test all available function methods."""
        benzene = "c1ccccc1"
        benzene_smarts = "[#6]1:[#6]:[#6]:[#6]:[#6]:[#6]:1"
        ethanol = "CCO"

        substructure_expr = bingo_func.has_substructure(
            self.compounds.c.structure, benzene
        )
        smarts_expr = bingo_func.matches_smarts(
            self.compounds.c.structure, benzene_smarts
        )
        equals_expr = bingo_func.equals(self.compounds.c.structure, ethanol)
        similarity_expr = bingo_func.similarity(
            self.compounds.c.structure, ethanol, 0.7
        )

        stmt = select(self.compounds).where(
            or_(substructure_expr, smarts_expr, equals_expr, similarity_expr)
        )

        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "bingo.sub" in compiled
        assert "bingo.smarts" in compiled
        assert "bingo.exact" in compiled
        assert "bingo.sim" in compiled
