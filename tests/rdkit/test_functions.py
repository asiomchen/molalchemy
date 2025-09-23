"""Tests for RDKit functions."""

from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import select

from molalchemy.rdkit import functions as rdkit_func
from molalchemy.rdkit.types import RdkitBitFingerprint, RdkitMol


class TestRdkitFunc:
    """Test rdkit_func static methods."""

    def setup_method(self):
        """Set up test table and columns."""
        self.metadata = MetaData()
        self.test_table = Table(
            "test_compounds",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("structure", RdkitMol()),
            Column("fingerprint", RdkitBitFingerprint()),
        )
        self.mol_column = self.test_table.c.structure
        self.fp_column = self.test_table.c.fingerprint

    def test_equals_function(self):
        """Test equals function generates correct SQL."""
        query = "CCO"

        result = rdkit_func.mol.equals(self.mol_column, query)

        # Should return a binary expression (column @= operator)
        assert hasattr(result, "left")
        assert hasattr(result, "right")
        assert hasattr(result, "operator")

        # Check the generated SQL string
        sql_str = str(result)
        assert "test_compounds.structure" in sql_str
        assert "@=" in sql_str
        # In non-literal mode, query values are bind parameters
        assert ":structure_" in sql_str

    def test_has_substructure_function(self):
        """Test has_substructure function generates correct SQL."""
        query = "c1ccccc1"

        result = rdkit_func.mol.has_substructure(self.mol_column, query)

        # Should return a binary expression (column @> operator)
        assert hasattr(result, "left")
        assert hasattr(result, "right")
        assert hasattr(result, "operator")

        # Check the generated SQL string
        sql_str = str(result)
        assert "test_compounds.structure" in sql_str
        assert "@>" in sql_str
        # In non-literal mode, query values are bind parameters
        assert ":structure_" in sql_str

    def test_to_binary_function(self):
        """Test to_binary function generates correct SQL."""
        result = rdkit_func.mol.to_binary(self.mol_column)

        # Should return a function call
        sql_str = str(result)
        assert "mol_send" in sql_str
        assert "test_compounds.structure" in sql_str

    def test_mol_from_smiles_function(self):
        """Test mol_from_smiles function generates correct SQL."""
        smiles = "CCO"

        result = rdkit_func.mol.from_smiles(smiles)

        # Should return a function call
        sql_str = str(result)
        assert "mol_from_smiles" in sql_str
        # The SMILES will be cast to cstring
        assert "cstring" in sql_str.lower()

    def test_maccs_fp_function(self):
        """Test maccs_fp function generates correct SQL."""
        result = rdkit_func.mol.maccs_fp(self.mol_column)

        # Should return a function call
        sql_str = str(result)
        assert "maccs_fp" in sql_str
        assert "test_compounds.structure" in sql_str

    def test_tanimoto_function(self):
        """Test tanimoto function generates correct SQL."""
        fp1 = b"fingerprint1"
        fp2 = b"fingerprint2"

        result = rdkit_func.fp.tanimoto_sml(fp1, fp2)

        # Should return a function call
        sql_str = str(result)
        assert "tanimoto_sml" in sql_str
        # Both fingerprints should be present as bind parameters
        assert ":tanimoto_sml_" in sql_str


class TestRdkitFuncWithORM:
    """Test rdkit_func with ORM models."""

    def setup_method(self):
        """Set up ORM model for testing."""

        class Base(DeclarativeBase):
            pass

        class Compound(Base):
            __tablename__ = "compounds"

            id: Mapped[int] = mapped_column(Integer, primary_key=True)
            name: Mapped[str] = mapped_column(String(100))
            structure: Mapped[str] = mapped_column(RdkitMol())
            fingerprint: Mapped[bytes] = mapped_column(RdkitBitFingerprint())

        self.Compound = Compound

    def test_equals_with_orm_column(self):
        """Test equals function with ORM column."""
        query = "CCO"

        result = rdkit_func.mol.equals(self.Compound.structure, query)
        sql_str = str(result)

        assert "@=" in sql_str
        # In non-literal mode, query values are bind parameters
        assert ":structure_" in sql_str

    def test_has_substructure_with_orm_column(self):
        """Test has_substructure function with ORM column."""
        query = "c1ccccc1"

        result = rdkit_func.mol.has_substructure(self.Compound.structure, query)
        sql_str = str(result)

        assert "@>" in sql_str
        # In non-literal mode, query values are bind parameters
        assert ":structure_" in sql_str

    def test_maccs_fp_with_orm_column(self):
        """Test maccs_fp function with ORM column."""
        result = rdkit_func.mol.maccs_fp(self.Compound.structure)
        sql_str = str(result)

        assert "maccs_fp" in sql_str
        assert "compounds.structure" in sql_str


class TestRdkitFuncIntegration:
    """Test rdkit_func in complete SQL queries."""

    def setup_method(self):
        """Set up test table for integration testing."""
        self.metadata = MetaData()
        self.test_table = Table(
            "test_molecules",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("structure", RdkitMol()),
            Column("fingerprint", RdkitBitFingerprint()),
        )

    def test_has_substructure_in_where_clause(self):
        """Test using has_substructure function in WHERE clause."""
        query = "c1ccccc1"

        # Create a query using the function
        substructure_expr = rdkit_func.mol.has_substructure(
            self.test_table.c.structure, query
        )
        stmt = select(self.test_table).where(substructure_expr)

        # Should compile without errors
        compiled = str(stmt.compile())
        assert "SELECT" in compiled
        assert "@>" in compiled
        assert ":structure_" in compiled

    def test_multiple_functions_in_query(self):
        """Test using multiple rdkit functions in one query."""
        benzene = "c1ccccc1"
        ethanol = "CCO"

        substructure_expr = rdkit_func.mol.has_substructure(
            self.test_table.c.structure, benzene
        )
        equals_expr = rdkit_func.mol.equals(self.test_table.c.structure, ethanol)

        stmt = select(self.test_table).where(substructure_expr | equals_expr)

        compiled = str(stmt.compile())
        assert "SELECT" in compiled
        assert "@>" in compiled  # has_substructure
        assert "@=" in compiled  # equals
        assert ":structure_" in compiled

    def test_mol_conversion_functions(self):
        """Test molecular conversion functions in query."""
        smiles = "CCO"

        mol_expr = rdkit_func.mol.from_smiles(smiles)
        binary_expr = rdkit_func.mol.to_binary(self.test_table.c.structure)
        fp_expr = rdkit_func.mol.maccs_fp(self.test_table.c.structure)

        stmt = select(
            self.test_table.c.id,
            mol_expr.label("mol_from_smiles"),
            binary_expr.label("binary_mol"),
            fp_expr.label("fingerprint"),
        )

        compiled = str(stmt.compile())
        assert "SELECT" in compiled
        assert "mol_from_smiles" in compiled
        assert "mol_send" in compiled
        assert "maccs_fp" in compiled
        # SMILES should be parameterized
        assert ":param_" in compiled

    def test_fingerprint_functions(self):
        """Test fingerprint-related functions."""
        fp1 = b"fingerprint1"
        fp2 = b"fingerprint2"

        tanimoto_expr = rdkit_func.fp.tanimoto_sml(fp1, fp2)
        maccs_expr = rdkit_func.mol.maccs_fp(self.test_table.c.structure)

        stmt = select(
            self.test_table.c.id,
            tanimoto_expr.label("similarity"),
            maccs_expr.label("maccs_fingerprint"),
        )

        compiled = str(stmt.compile())
        assert "SELECT" in compiled
        assert "tanimoto" in compiled
        assert "maccs_fp" in compiled
        # Fingerprints should be parameterized
        assert ":tanimoto_sml_" in compiled
