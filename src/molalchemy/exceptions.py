"""Custom exceptions for molalchemy."""

__all__ = [
    "InvalidMoleculeError",
    "InvalidReactionError",
    "MolAlchemyError",
]


class MolAlchemyError(Exception):
    """Base exception for all molalchemy errors."""


class InvalidMoleculeError(MolAlchemyError, ValueError):
    """Raised when an invalid molecule representation is encountered."""


class InvalidReactionError(MolAlchemyError, ValueError):
    """Raised when an invalid reaction representation is encountered."""
