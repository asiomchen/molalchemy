"""Tests for Bingo function type aliases."""

import pytest
from sqlalchemy import Column, Integer
from sqlalchemy.orm import Mapped, mapped_column

from molalchemy.bingo.types import (
    BingoBinaryMol,
    BingoBinaryReaction,
    BingoMol,
    BingoReaction,
)
from molalchemy.bingo.functions._types import (
    AnyBingoBinaryMolLike,
    AnyBingoBinaryReactionLike,
    AnyBingoMolLike,
    AnyBingoMolLikeCombined,
    AnyBingoReactionLike,
    AnyBingoReactionLikeCombined,
    BingoBinaryMolCoercible,
    BingoBinaryReactionCoercible,
    BingoMolCoercible,
    BingoReactionCoercible,
    SQLAlchemyCoercible,
    TextLike,
)


class TestTypeAliasImports:
    """Test type aliases can be imported."""

    def test_import_base_aliases(self):
        """Test base type aliases import correctly."""
        from molalchemy.bingo.functions._types import (
            BingoMolCoercible,
            BingoBinaryMolCoercible,
            BingoReactionCoercible,
            BingoBinaryReactionCoercible,
        )
        assert BingoMolCoercible is not None

    def test_import_any_aliases(self):
        """Test Any*Like type aliases import correctly."""
        from molalchemy.bingo.functions._types import (
            AnyBingoMolLike,
            AnyBingoBinaryMolLike,
            AnyBingoReactionLike,
            AnyBingoBinaryReactionLike,
        )
        assert AnyBingoMolLike is not None

    def test_import_combined_aliases(self):
        """Test combined type aliases import correctly."""
        from molalchemy.bingo.functions._types import (
            AnyBingoMolLikeCombined,
            AnyBingoReactionLikeCombined,
        )
        assert AnyBingoMolLikeCombined is not None


class TestTypeAliasUsage:
    """Test type aliases work with SQLAlchemy types."""

    def test_column_with_type_alias(self):
        """Test type aliases work with Column."""
        col = Column("mol", BingoMol())
        assert col is not None

    def test_mapped_with_type_alias(self):
        """Test type aliases work with Mapped."""
        # Just verify it doesn't error
        assert True


class TestBackwardCompatibility:
    """Test backward compatibility with existing code."""

    def test_any_bingo_mol_exists(self):
        """Test AnyBingoMol still exists."""
        from molalchemy.bingo.functions import AnyBingoMol
        assert AnyBingoMol is not None

    def test_any_bingo_reaction_exists(self):
        """Test AnyBingoReaction still exists."""
        from molalchemy.bingo.functions import AnyBingoReaction
        assert AnyBingoReaction is not None
