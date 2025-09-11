"""Tests for bingo indexes."""

import pytest
from sqlalchemy import Column, Integer, String, MetaData, Table, Index
from sqlalchemy.schema import CreateIndex

from chemschema.bingo.types import BingoMol, BingoBinaryMol
from chemschema.bingo.index import BingoMolIndex, BingoBinaryMolIndex


class TestBingoMolIndex:
    """Test BingoMolIndex class."""
    
    def setup_method(self):
        """Set up test table with BingoMol column."""
        self.metadata = MetaData()
        self.test_table = Table(
            'test_molecules',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(100)),
            Column('structure', BingoMol()),
        )
        self.mol_column = self.test_table.c.structure
    
    def test_bingo_mol_index_creation(self):
        """Test BingoMolIndex can be created."""
        index = BingoMolIndex('idx_mol_structure', self.mol_column)
        
        assert isinstance(index, Index)
        assert index.name == 'idx_mol_structure'
        assert self.mol_column in index.expressions
    
    def test_bingo_mol_index_postgresql_using(self):
        """Test BingoMolIndex uses correct PostgreSQL index type."""
        index = BingoMolIndex('idx_mol_structure', self.mol_column)
        
        # Check that it uses the bingo_idx index type
        assert hasattr(index, 'dialect_options')
        postgresql_options = index.dialect_options.get('postgresql', {})
        assert postgresql_options.get('using') == 'bingo_idx'
    
    def test_bingo_mol_index_postgresql_ops(self):
        """Test BingoMolIndex uses correct PostgreSQL operator class."""
        index = BingoMolIndex('idx_mol_structure', self.mol_column)
        
        postgresql_options = index.dialect_options.get('postgresql', {})
        ops = postgresql_options.get('ops', {})
        assert ops.get(self.mol_column) == 'bingo.molecule'
    
    def test_bingo_mol_index_inheritance(self):
        """Test BingoMolIndex inherits from SQLAlchemy Index."""
        index = BingoMolIndex('idx_mol_structure', self.mol_column)
        
        assert isinstance(index, Index)
        assert hasattr(index, 'expressions')
        assert hasattr(index, 'name')
        assert hasattr(index, 'table')
    
    def test_bingo_mol_index_with_table(self):
        """Test BingoMolIndex works when added to table."""
        index = BingoMolIndex('idx_mol_structure', self.mol_column)
        
        # Add index to table
        self.test_table.append_constraint(index)
        
        # Index should be associated with the table
        assert index.table is self.test_table
        assert index in self.test_table.indexes


class TestBingoBinaryMolIndex:
    """Test BingoBinaryMolIndex class."""
    
    def setup_method(self):
        """Set up test table with BingoBinaryMol column."""
        self.metadata = MetaData()
        self.test_table = Table(
            'test_binary_molecules',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(100)),
            Column('structure', BingoBinaryMol()),
        )
        self.mol_column = self.test_table.c.structure
    
    def test_bingo_binary_mol_index_creation(self):
        """Test BingoBinaryMolIndex can be created."""
        index = BingoBinaryMolIndex('idx_binary_mol_structure', self.mol_column)
        
        assert isinstance(index, Index)
        assert index.name == 'idx_binary_mol_structure'
        assert self.mol_column in index.expressions
    
    def test_bingo_binary_mol_index_postgresql_using(self):
        """Test BingoBinaryMolIndex uses correct PostgreSQL index type."""
        index = BingoBinaryMolIndex('idx_binary_mol_structure', self.mol_column)
        
        postgresql_options = index.dialect_options.get('postgresql', {})
        assert postgresql_options.get('using') == 'bingo_idx'
    
    def test_bingo_binary_mol_index_postgresql_ops(self):
        """Test BingoBinaryMolIndex uses correct PostgreSQL operator class."""
        index = BingoBinaryMolIndex('idx_binary_mol_structure', self.mol_column)
        
        postgresql_options = index.dialect_options.get('postgresql', {})
        ops = postgresql_options.get('ops', {})
        assert ops.get(self.mol_column) == 'bingo.bmolecule'
    
    def test_bingo_binary_mol_index_inheritance(self):
        """Test BingoBinaryMolIndex inherits from SQLAlchemy Index."""
        index = BingoBinaryMolIndex('idx_binary_mol_structure', self.mol_column)
        
        assert isinstance(index, Index)
        assert hasattr(index, 'expressions')
        assert hasattr(index, 'name')
        assert hasattr(index, 'table')
    
    def test_bingo_binary_mol_index_with_table(self):
        """Test BingoBinaryMolIndex works when added to table."""
        index = BingoBinaryMolIndex('idx_binary_mol_structure', self.mol_column)
        
        # Add index to table
        self.test_table.append_constraint(index)
        
        # Index should be associated with the table
        assert index.table is self.test_table
        assert index in self.test_table.indexes


class TestBingoIndexes:
    """Test both bingo index types together."""
    
    def setup_method(self):
        """Set up test tables with both mol types."""
        self.metadata = MetaData()
        
        self.mol_table = Table(
            'molecules',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('structure', BingoMol()),
        )
        
        self.binary_mol_table = Table(
            'binary_molecules',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('structure', BingoBinaryMol()),
        )
    
    def test_different_operator_classes(self):
        """Test that the two index types use different operator classes."""
        mol_index = BingoMolIndex('idx_mol', self.mol_table.c.structure)
        binary_index = BingoBinaryMolIndex('idx_binary', self.binary_mol_table.c.structure)
        
        mol_ops = mol_index.dialect_options['postgresql']['ops']
        binary_ops = binary_index.dialect_options['postgresql']['ops']
        
        mol_op_class = mol_ops[self.mol_table.c.structure]
        binary_op_class = binary_ops[self.binary_mol_table.c.structure]
        
        assert mol_op_class == 'bingo.molecule'
        assert binary_op_class == 'bingo.bmolecule'
        assert mol_op_class != binary_op_class
    
    def test_same_index_type(self):
        """Test that both index types use the same PostgreSQL index type."""
        mol_index = BingoMolIndex('idx_mol', self.mol_table.c.structure)
        binary_index = BingoBinaryMolIndex('idx_binary', self.binary_mol_table.c.structure)
        
        mol_using = mol_index.dialect_options['postgresql']['using']
        binary_using = binary_index.dialect_options['postgresql']['using']
        
        assert mol_using == 'bingo_idx'
        assert binary_using == 'bingo_idx'
        assert mol_using == binary_using
    
    def test_both_inherit_from_index(self):
        """Test that both index types inherit from SQLAlchemy Index."""
        mol_index = BingoMolIndex('idx_mol', self.mol_table.c.structure)
        binary_index = BingoBinaryMolIndex('idx_binary', self.binary_mol_table.c.structure)
        
        assert isinstance(mol_index, Index)
        assert isinstance(binary_index, Index)
        assert type(mol_index).__bases__ == (Index,)
        assert type(binary_index).__bases__ == (Index,)


class TestBingoIndexCreation:
    """Test index creation scenarios."""
    
    def test_index_creation_with_multiple_tables(self):
        """Test creating indexes on multiple tables."""
        metadata = MetaData()
        
        # Create multiple tables with bingo columns
        compounds = Table(
            'compounds',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(100)),
            Column('structure', BingoMol()),
            BingoMolIndex('idx_compounds_structure', 'structure')
        )
        
        reactions = Table(
            'reactions',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(100)),
            Column('binary_structure', BingoBinaryMol()),
            BingoBinaryMolIndex('idx_reactions_binary_structure', 'binary_structure')
        )
        
        # Both tables should have their indexes
        assert len(compounds.indexes) == 1
        assert len(reactions.indexes) == 1
        
        compounds_index = list(compounds.indexes)[0]
        reactions_index = list(reactions.indexes)[0]
        
        assert compounds_index.name == 'idx_compounds_structure'
        assert reactions_index.name == 'idx_reactions_binary_structure'
    
    def test_index_name_validation(self):
        """Test that index names are properly set."""
        metadata = MetaData()
        test_table = Table(
            'test_table',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('mol', BingoMol()),
        )
        
        # Test various index names
        index1 = BingoMolIndex('my_custom_index', test_table.c.mol)
        index2 = BingoMolIndex('another_index_name', test_table.c.mol)
        
        assert index1.name == 'my_custom_index'
        assert index2.name == 'another_index_name'
        assert index1.name != index2.name
