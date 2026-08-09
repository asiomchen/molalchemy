from importlib import import_module
from types import ModuleType
from typing import TYPE_CHECKING

from .comparators import RdkitFPComparator, RdkitMolComparator, RdkitReactionComparator
from .index import RdkitIndex
from .settings import (
    RdkitSettings,
    configure_engine,
    get_dice_threshold,
    get_tanimoto_threshold,
    set_dice_threshold,
    set_tanimoto_threshold,
    similarity_threshold,
)
from .types import (
    RdkitBitFingerprint,
    RdkitMol,
    RdkitQMol,
    RdkitReaction,
    RdkitSparseFingerprint,
    RdkitXQMol,
)

if TYPE_CHECKING:
    from . import functions


def __getattr__(name: str) -> ModuleType:
    if name == "functions":
        return import_module(f"{__name__}.functions")
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "RdkitBitFingerprint",
    "RdkitFPComparator",
    "RdkitIndex",
    "RdkitMol",
    "RdkitMolComparator",
    "RdkitQMol",
    "RdkitReaction",
    "RdkitReactionComparator",
    "RdkitSettings",
    "RdkitSparseFingerprint",
    "RdkitXQMol",
    "configure_engine",
    "functions",
    "get_dice_threshold",
    "get_tanimoto_threshold",
    "set_dice_threshold",
    "set_tanimoto_threshold",
    "similarity_threshold",
]
