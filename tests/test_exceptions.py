"""Tests for molalchemy custom exceptions."""

import pytest

from molalchemy.exceptions import (
    InvalidMoleculeError,
    InvalidReactionError,
    MolAlchemyError,
)


class TestExceptionHierarchy:
    """Test custom exception hierarchy."""

    def test_molalchemy_error_is_exception(self):
        assert issubclass(MolAlchemyError, Exception)

    def test_invalid_molecule_error_is_molalchemy_error(self):
        assert issubclass(InvalidMoleculeError, MolAlchemyError)

    def test_invalid_reaction_error_is_molalchemy_error(self):
        assert issubclass(InvalidReactionError, MolAlchemyError)

    def test_catch_all_with_base_class(self):
        with pytest.raises(MolAlchemyError):
            raise InvalidMoleculeError("bad molecule")

    def test_exception_message(self):
        err = InvalidMoleculeError("bad SMILES")
        assert str(err) == "bad SMILES"


class TestExceptionExports:
    """Test exceptions are importable from top-level package."""

    def test_import_from_top_level(self):
        from molalchemy import (
            InvalidMoleculeError,
            InvalidReactionError,
            MolAlchemyError,
        )

        assert MolAlchemyError is not None
        assert InvalidMoleculeError is not None
        assert InvalidReactionError is not None
