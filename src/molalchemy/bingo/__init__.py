from importlib import import_module
from types import ModuleType
from typing import TYPE_CHECKING

from .comparators import BingoMolComparator, BingoRxnComparator
from .index import (
    BingoBinaryMolIndex,
    BingoBinaryRxnIndex,
    BingoMolIndex,
    BingoRxnIndex,
)
from .types import BingoBinaryMol, BingoBinaryReaction, BingoMol, BingoReaction

if TYPE_CHECKING:
    from . import functions


def __getattr__(name: str) -> ModuleType:
    if name == "functions":
        return import_module(f"{__name__}.functions")
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "BingoBinaryMol",
    "BingoBinaryMolIndex",
    "BingoBinaryReaction",
    "BingoBinaryRxnIndex",
    "BingoMol",
    "BingoMolComparator",
    "BingoMolIndex",
    "BingoReaction",
    "BingoRxnComparator",
    "BingoRxnIndex",
    "functions",
]
