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
