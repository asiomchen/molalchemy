"""RDKit PostgreSQL GUC settings helpers for similarity search thresholds."""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING

from sqlalchemy import text

if TYPE_CHECKING:
    from collections.abc import Generator

    from sqlalchemy.orm import Session


def _validate_threshold(value: float) -> None:
    if not isinstance(value, (int, float)):
        raise TypeError(f"threshold must be a float, got {type(value).__name__}")
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"threshold must be between 0.0 and 1.0, got {value}")


def set_tanimoto_threshold(session: Session, threshold: float) -> None:
    """Set the rdkit.tanimoto_threshold GUC variable."""
    _validate_threshold(threshold)
    session.execute(text(f"SET rdkit.tanimoto_threshold = {float(threshold)}"))


def set_dice_threshold(session: Session, threshold: float) -> None:
    """Set the rdkit.dice_threshold GUC variable."""
    _validate_threshold(threshold)
    session.execute(text(f"SET rdkit.dice_threshold = {float(threshold)}"))


def get_tanimoto_threshold(session: Session) -> float:
    """Get the current rdkit.tanimoto_threshold value."""
    result = session.execute(text("SHOW rdkit.tanimoto_threshold"))
    return float(result.scalar_one())


def get_dice_threshold(session: Session) -> float:
    """Get the current rdkit.dice_threshold value."""
    result = session.execute(text("SHOW rdkit.dice_threshold"))
    return float(result.scalar_one())


@contextmanager
def similarity_threshold(
    session: Session,
    *,
    tanimoto: float | None = None,
    dice: float | None = None,
) -> Generator[None, None, None]:
    """Context manager to temporarily set similarity thresholds.

    Restores original values on exit, even if an exception occurs.

    Parameters
    ----------
    session : Session
        SQLAlchemy session.
    tanimoto : float, optional
        Tanimoto threshold to set (0.0-1.0).
    dice : float, optional
        Dice threshold to set (0.0-1.0).
    """
    old_tanimoto = None
    old_dice = None

    try:
        if tanimoto is not None:
            old_tanimoto = get_tanimoto_threshold(session)
            set_tanimoto_threshold(session, tanimoto)
        if dice is not None:
            old_dice = get_dice_threshold(session)
            set_dice_threshold(session, dice)
        yield
    finally:
        if old_tanimoto is not None:
            set_tanimoto_threshold(session, old_tanimoto)
        if old_dice is not None:
            set_dice_threshold(session, old_dice)
