"""RDKit PostgreSQL cartridge settings helpers."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, fields
from threading import RLock
from typing import TYPE_CHECKING, Any
from weakref import WeakKeyDictionary

from sqlalchemy import event, text
from sqlalchemy.engine import Engine

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

    from sqlalchemy.orm import Session


_GUC_NAMES = {
    "tanimoto_threshold": "rdkit.tanimoto_threshold",
    "dice_threshold": "rdkit.dice_threshold",
    "do_chiral_sss": "rdkit.do_chiral_sss",
    "do_enhanced_stereo_sss": "rdkit.do_enhanced_stereo_sss",
    "sss_fp_size": "rdkit.sss_fp_size",
    "morgan_fp_size": "rdkit.morgan_fp_size",
    "featmorgan_fp_size": "rdkit.featmorgan_fp_size",
    "layered_fp_size": "rdkit.layered_fp_size",
    "rdkit_fp_size": "rdkit.rdkit_fp_size",
    "torsion_fp_size": "rdkit.torsion_fp_size",
    "atompair_fp_size": "rdkit.atompair_fp_size",
    "avalon_fp_size": "rdkit.avalon_fp_size",
}
_THRESHOLD_FIELDS = frozenset(("tanimoto_threshold", "dice_threshold"))
_BOOLEAN_FIELDS = frozenset(("do_chiral_sss", "do_enhanced_stereo_sss"))
_SIZE_FIELDS = frozenset(_GUC_NAMES) - _THRESHOLD_FIELDS - _BOOLEAN_FIELDS


def _validate_threshold(value: float, name: str = "threshold") -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a float, got {type(value).__name__}")
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0, got {value}")


@dataclass(frozen=True, slots=True)
class RdkitSettings:
    """Baseline RDKit cartridge settings for SQLAlchemy engine connections.

    Every field corresponds to a PostgreSQL GUC documented by the RDKit
    cartridge. ``None`` means that the server or connection's existing value
    is left unchanged. Thresholds must be between 0 and 1, fingerprint sizes
    must be positive integers, and substructure-search flags must be booleans.

    Use :func:`configure_engine` to apply an instance to an engine's pooled
    connections on every checkout.
    """

    tanimoto_threshold: float | None = None
    dice_threshold: float | None = None
    do_chiral_sss: bool | None = None
    do_enhanced_stereo_sss: bool | None = None
    sss_fp_size: int | None = None
    morgan_fp_size: int | None = None
    featmorgan_fp_size: int | None = None
    layered_fp_size: int | None = None
    rdkit_fp_size: int | None = None
    torsion_fp_size: int | None = None
    atompair_fp_size: int | None = None
    avalon_fp_size: int | None = None

    def __post_init__(self) -> None:
        for field in fields(self):
            value = getattr(self, field.name)
            if value is None:
                continue
            if field.name in _THRESHOLD_FIELDS:
                _validate_threshold(value, field.name)
            elif field.name in _BOOLEAN_FIELDS:
                if type(value) is not bool:
                    raise TypeError(
                        f"{field.name} must be a bool, got {type(value).__name__}"
                    )
            elif field.name in _SIZE_FIELDS:
                if type(value) is not int:
                    raise TypeError(
                        f"{field.name} must be an int, got {type(value).__name__}"
                    )
                if value <= 0:
                    raise ValueError(
                        f"{field.name} must be greater than 0, got {value}"
                    )

    def _guc_values(self) -> tuple[tuple[str, str], ...]:
        values: list[tuple[str, str]] = []
        for field in fields(self):
            value = getattr(self, field.name)
            if value is None:
                continue
            if field.name in _BOOLEAN_FIELDS:
                serialized = "on" if value else "off"
            elif field.name in _THRESHOLD_FIELDS:
                serialized = str(float(value))
            else:
                serialized = str(value)
            values.append((_GUC_NAMES[field.name], serialized))
        return tuple(values)


if TYPE_CHECKING:
    _CheckoutListener = Callable[[Any, Any, Any], None]
else:
    _CheckoutListener = Any

_engine_listeners: WeakKeyDictionary[Engine, _CheckoutListener] = WeakKeyDictionary()
_engine_listeners_lock = RLock()


def _make_checkout_listener(
    values: tuple[tuple[str, str], ...],
) -> _CheckoutListener:
    placeholders = ", ".join("set_config(%s, %s, false)" for _ in values)
    statement = f"SELECT {placeholders}"
    parameters = tuple(item for pair in values for item in pair)

    def apply_settings(dbapi_connection: Any, _record: Any, _proxy: Any) -> None:
        previous_autocommit = dbapi_connection.autocommit
        cursor = None
        try:
            dbapi_connection.autocommit = True
            cursor = dbapi_connection.cursor()
            cursor.execute(statement, parameters)
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            finally:
                dbapi_connection.autocommit = previous_autocommit

    return apply_settings


def configure_engine(engine: Engine, settings: RdkitSettings | None = None) -> Engine:
    """Apply an RDKit settings baseline whenever a pooled connection is checked out.

    Calling this function again for the same engine replaces its previous
    molalchemy listener. Passing an empty :class:`RdkitSettings` removes any
    previous listener. Reconfiguration disposes the existing pool so that idle
    connections cannot retain settings from the previous baseline. The engine
    itself is returned for convenient assignment.

    Parameters
    ----------
    engine
        A synchronous SQLAlchemy PostgreSQL engine.
    settings
        Validated RDKit cartridge settings. Fields set to ``None`` are not sent
        to PostgreSQL.
    """
    if not isinstance(engine, Engine):
        raise TypeError(f"engine must be an Engine, got {type(engine).__name__}")
    if engine.dialect.name != "postgresql":
        raise ValueError("RDKit cartridge settings require a PostgreSQL engine")
    if not isinstance(settings, RdkitSettings) and settings is not None:
        raise TypeError(
            f"settings must be RdkitSettings, got {type(settings).__name__}"
        )
    if settings is None:
        return engine
    values = settings._guc_values()
    listener = _make_checkout_listener(values) if values else None

    with _engine_listeners_lock:
        previous_listener = _engine_listeners.pop(engine, None)
        if previous_listener is not None:
            event.remove(engine, "checkout", previous_listener)
        if listener is not None:
            event.listen(engine, "checkout", listener)
            _engine_listeners[engine] = listener
        if previous_listener is not None:
            engine.dispose()

    return engine


def set_tanimoto_threshold(session: Session, threshold: float) -> None:
    """Set the rdkit.tanimoto_threshold GUC variable for a session."""
    _validate_threshold(threshold)
    session.execute(text(f"SET rdkit.tanimoto_threshold = {float(threshold)}"))


def set_dice_threshold(session: Session, threshold: float) -> None:
    """Set the rdkit.dice_threshold GUC variable for a session."""
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
    """Temporarily set and then restore session similarity thresholds."""
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
