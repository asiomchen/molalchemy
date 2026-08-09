"""Tests for RDKit indexes."""

from sqlalchemy import Column, Integer, MetaData, String, Table, text

from molalchemy.rdkit.index import RdkitIndex
from molalchemy.rdkit.types import RdkitBitFingerprint, RdkitMol, RdkitSparseFingerprint


class TestRdkitIndex:
    """Test RdkitIndex creation and properties."""

    def test_rdkit_index_creation(self):
        """Test basic RdkitIndex creation."""
        metadata = MetaData()
        test_table = Table(
            "test_molecules",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("mol", RdkitMol()),
        )

        # Create index
        index = RdkitIndex("idx_test_molecules_mol", test_table.c.mol)

        # Should not raise any exceptions
        assert index.name == "idx_test_molecules_mol"
        assert test_table.c.mol in index.expressions

    def test_rdkit_index_postgresql_using(self):
        """Test that RdkitIndex uses GIST."""
        metadata = MetaData()
        test_table = Table(
            "test_molecules",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("mol", RdkitMol()),
        )

        index = RdkitIndex("idx_molecules_mol", test_table.c.mol)

        # Check that it uses GIST
        assert index.kwargs.get("postgresql_using") == "gist"

    def test_rdkit_index_with_bit_fingerprint(self):
        """Test RdkitIndex with bit fingerprint column."""
        metadata = MetaData()
        test_table = Table(
            "test_fingerprints",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("fingerprint", RdkitBitFingerprint()),
        )

        index = RdkitIndex("idx_fingerprints_fp", test_table.c.fingerprint)

        assert index.name == "idx_fingerprints_fp"
        assert test_table.c.fingerprint in index.expressions
        assert index.kwargs.get("postgresql_using") == "gist"

    def test_rdkit_index_with_sparse_fingerprint(self):
        """Test RdkitIndex with sparse fingerprint column."""
        metadata = MetaData()
        test_table = Table(
            "test_sparse_fingerprints",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("fingerprint", RdkitSparseFingerprint()),
        )

        index = RdkitIndex("idx_sparse_fp", test_table.c.fingerprint)

        assert index.name == "idx_sparse_fp"
        assert test_table.c.fingerprint in index.expressions
        assert index.kwargs.get("postgresql_using") == "gist"

    def test_rdkit_index_with_multiple_columns(self):
        """Test RdkitIndex with multiple columns."""
        metadata = MetaData()
        test_table = Table(
            "test_compounds",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("mol", RdkitMol()),
            Column("fingerprint", RdkitBitFingerprint()),
        )

        index = RdkitIndex(
            "idx_compounds_mol_fp", test_table.c.mol, test_table.c.fingerprint
        )

        assert index.name == "idx_compounds_mol_fp"
        assert test_table.c.mol in index.expressions
        assert test_table.c.fingerprint in index.expressions
        assert index.kwargs.get("postgresql_using") == "gist"

    def test_rdkit_index_with_table_definition(self):
        """Test RdkitIndex can be included in table definition."""
        metadata = MetaData()
        test_table = Table(
            "test_molecules",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100)),
            Column("mol", RdkitMol()),
            RdkitIndex("idx_molecules_mol", "mol"),
        )

        # Should not raise any exceptions
        assert test_table.c.mol.type.__class__ == RdkitMol
        # Check that the index was added
        assert len(test_table.indexes) == 1
        index = list(test_table.indexes)[0]
        assert index.name == "idx_molecules_mol"
        assert index.kwargs.get("postgresql_using") == "gist"

    def test_rdkit_index_inheritance(self):
        """Test that RdkitIndex inherits from Index."""
        from sqlalchemy import Index

        metadata = MetaData()
        test_table = Table(
            "test_molecules",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("mol", RdkitMol()),
        )

        index = RdkitIndex("idx_molecules_mol", test_table.c.mol)

        assert isinstance(index, Index)

    def test_rdkit_index_with_additional_kwargs(self):
        """Test RdkitIndex with additional keyword arguments."""
        metadata = MetaData()
        test_table = Table(
            "test_molecules",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("mol", RdkitMol()),
        )

        index = RdkitIndex(
            "idx_molecules_mol", test_table.c.mol, postgresql_with={"fastupdate": "off"}
        )

        assert index.kwargs.get("postgresql_using") == "gist"
        assert index.kwargs.get("postgresql_with") == {"fastupdate": "off"}

    def test_standard_options_remain_on_index(self):
        """Standard options remain available on the SQLAlchemy index."""
        index = RdkitIndex(
            "idx_molecules_mol",
            "mol",
            unique=True,
            quote=True,
            info={"purpose": "chemical search"},
            postgresql_where=text("mol IS NOT NULL"),
            postgresql_with={"fillfactor": 70},
            postgresql_tablespace="fastspace",
            postgresql_concurrently=True,
        )

        assert index.unique is True
        assert index.name.quote is True
        assert index.info == {"purpose": "chemical search"}
        assert index.kwargs["postgresql_using"] == "gist"
        assert index.kwargs["postgresql_with"] == {"fillfactor": 70}
        assert str(index.kwargs["postgresql_where"]) == "mol IS NOT NULL"
        assert index.kwargs["postgresql_tablespace"] == "fastspace"
        assert index.kwargs["postgresql_concurrently"] is True

    def test_postgresql_using_cannot_override_gist(self):
        """The GiST access method cannot be overridden."""
        index = RdkitIndex(
            "idx_molecules_mol",
            "mol",
            postgresql_using="gin",
        )

        assert index.kwargs["postgresql_using"] == "gist"


class TestRdkitIndexCreation:
    """Test index creation scenarios."""

    def test_index_creation_with_multiple_tables(self):
        """Test creating indexes for multiple tables."""
        metadata = MetaData()

        molecules_table = Table(
            "molecules",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("structure", RdkitMol()),
        )

        fingerprints_table = Table(
            "fingerprints",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("mol_id", Integer),
            Column("fp", RdkitBitFingerprint()),
        )

        mol_index = RdkitIndex("idx_molecules_structure", molecules_table.c.structure)
        fp_index = RdkitIndex("idx_fingerprints_fp", fingerprints_table.c.fp)

        # Both should be valid indexes
        assert mol_index.name == "idx_molecules_structure"
        assert fp_index.name == "idx_fingerprints_fp"
        assert mol_index.kwargs.get("postgresql_using") == "gist"
        assert fp_index.kwargs.get("postgresql_using") == "gist"

    def test_index_name_validation(self):
        """Test that index names are properly set."""
        metadata = MetaData()
        test_table = Table(
            "test_table",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("mol", RdkitMol()),
        )

        # Test various index names
        index1 = RdkitIndex("simple_name", test_table.c.mol)
        index2 = RdkitIndex("complex_name_with_underscores", test_table.c.mol)
        index3 = RdkitIndex("idx_table_column", test_table.c.mol)

        assert index1.name == "simple_name"
        assert index2.name == "complex_name_with_underscores"
        assert index3.name == "idx_table_column"
