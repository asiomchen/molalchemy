"""Tests for RDKit similarity threshold settings helpers."""

from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine

import molalchemy.rdkit.settings as settings_module
from molalchemy.rdkit.settings import (
    RdkitSettings,
    configure_engine,
    get_dice_threshold,
    get_tanimoto_threshold,
    set_dice_threshold,
    set_tanimoto_threshold,
    similarity_threshold,
)


@pytest.fixture
def session():
    mock = Mock()
    mock.execute.return_value.scalar_one.return_value = "0.5"
    return mock


@pytest.fixture
def postgres_engine(monkeypatch):
    engine = create_engine("sqlite://")
    monkeypatch.setattr(engine.dialect, "name", "postgresql")
    yield engine
    settings_module._engine_listeners.pop(engine, None)
    engine.dispose()


class TestRdkitSettings:
    def test_serializes_every_documented_setting(self):
        settings = RdkitSettings(
            tanimoto_threshold=0.7,
            dice_threshold=1,
            do_chiral_sss=True,
            do_enhanced_stereo_sss=False,
            sss_fp_size=1024,
            morgan_fp_size=2048,
            featmorgan_fp_size=2049,
            layered_fp_size=2050,
            rdkit_fp_size=2051,
            torsion_fp_size=2052,
            atompair_fp_size=2053,
            avalon_fp_size=2054,
        )

        assert settings._guc_values() == (
            ("rdkit.tanimoto_threshold", "0.7"),
            ("rdkit.dice_threshold", "1.0"),
            ("rdkit.do_chiral_sss", "on"),
            ("rdkit.do_enhanced_stereo_sss", "off"),
            ("rdkit.sss_fp_size", "1024"),
            ("rdkit.morgan_fp_size", "2048"),
            ("rdkit.featmorgan_fp_size", "2049"),
            ("rdkit.layered_fp_size", "2050"),
            ("rdkit.rdkit_fp_size", "2051"),
            ("rdkit.torsion_fp_size", "2052"),
            ("rdkit.atompair_fp_size", "2053"),
            ("rdkit.avalon_fp_size", "2054"),
        )

    @pytest.mark.parametrize("field", ["tanimoto_threshold", "dice_threshold"])
    @pytest.mark.parametrize("value", [-0.1, 1.1])
    def test_rejects_out_of_range_thresholds(self, field, value):
        with pytest.raises(ValueError, match=field):
            RdkitSettings(**{field: value})

    @pytest.mark.parametrize("field", ["tanimoto_threshold", "dice_threshold"])
    @pytest.mark.parametrize("value", [True, "0.5"])
    def test_rejects_non_numeric_thresholds(self, field, value):
        with pytest.raises(TypeError, match=field):
            RdkitSettings(**{field: value})

    @pytest.mark.parametrize(
        "field", ["do_chiral_sss", "do_enhanced_stereo_sss"]
    )
    @pytest.mark.parametrize("value", [0, 1, "on"])
    def test_rejects_non_boolean_flags(self, field, value):
        with pytest.raises(TypeError, match=field):
            RdkitSettings(**{field: value})

    @pytest.mark.parametrize(
        "field",
        [
            "sss_fp_size",
            "morgan_fp_size",
            "featmorgan_fp_size",
            "layered_fp_size",
            "rdkit_fp_size",
            "torsion_fp_size",
            "atompair_fp_size",
            "avalon_fp_size",
        ],
    )
    @pytest.mark.parametrize("value", [True, 1.5, "2048"])
    def test_rejects_non_integer_fingerprint_sizes(self, field, value):
        with pytest.raises(TypeError, match=field):
            RdkitSettings(**{field: value})

    @pytest.mark.parametrize("value", [0, -1])
    def test_rejects_non_positive_fingerprint_sizes(self, value):
        with pytest.raises(ValueError, match="morgan_fp_size"):
            RdkitSettings(morgan_fp_size=value)


class TestConfigureEngine:
    def test_returns_engine_and_registers_parameterized_checkout_listener(
        self, postgres_engine, monkeypatch
    ):
        registered = []
        monkeypatch.setattr(
            settings_module.event,
            "listen",
            lambda target, name, listener: registered.append((target, name, listener)),
        )

        result = configure_engine(
            postgres_engine,
            RdkitSettings(
                tanimoto_threshold=0.42,
                do_chiral_sss=True,
                morgan_fp_size=1024,
            ),
        )

        assert result is postgres_engine
        assert len(registered) == 1
        assert registered[0][:2] == (postgres_engine, "checkout")

        cursor = Mock()
        dbapi_connection = Mock()
        dbapi_connection.autocommit = False
        dbapi_connection.cursor.return_value = cursor
        registered[0][2](dbapi_connection, Mock(), Mock())

        statement, parameters = cursor.execute.call_args.args
        assert statement.count("set_config(%s, %s, false)") == 3
        assert parameters == (
            "rdkit.tanimoto_threshold",
            "0.42",
            "rdkit.do_chiral_sss",
            "on",
            "rdkit.morgan_fp_size",
            "1024",
        )
        cursor.close.assert_called_once_with()
        assert dbapi_connection.autocommit is False

    def test_reconfiguration_replaces_previous_listener(
        self, postgres_engine, monkeypatch
    ):
        registered = []
        removed = []
        monkeypatch.setattr(
            settings_module.event,
            "listen",
            lambda target, name, listener: registered.append(listener),
        )
        monkeypatch.setattr(
            settings_module.event,
            "remove",
            lambda target, name, listener: removed.append(listener),
        )

        original_pool = postgres_engine.pool
        configure_engine(postgres_engine, RdkitSettings(tanimoto_threshold=0.4))

        assert postgres_engine.pool is original_pool

        configure_engine(postgres_engine, RdkitSettings(dice_threshold=0.6))

        assert len(registered) == 2
        assert removed == [registered[0]]
        assert postgres_engine.pool is not original_pool

    def test_empty_settings_remove_listener_without_registering_another(
        self, postgres_engine, monkeypatch
    ):
        registered = []
        removed = []
        monkeypatch.setattr(
            settings_module.event,
            "listen",
            lambda target, name, listener: registered.append(listener),
        )
        monkeypatch.setattr(
            settings_module.event,
            "remove",
            lambda target, name, listener: removed.append(listener),
        )

        configured_pool = postgres_engine.pool
        configure_engine(postgres_engine, RdkitSettings(dice_threshold=0.6))
        configure_engine(postgres_engine, RdkitSettings())

        assert len(registered) == 1
        assert removed == registered
        assert postgres_engine.pool is not configured_pool

    def test_initial_empty_settings_do_not_replace_pool(self, postgres_engine):
        original_pool = postgres_engine.pool

        configure_engine(postgres_engine, RdkitSettings())

        assert postgres_engine.pool is original_pool

    def test_reconfiguration_survives_engine_dispose(self, postgres_engine):
        configure_engine(
            postgres_engine, RdkitSettings(tanimoto_threshold=0.4)
        )
        original_pool = postgres_engine.pool

        postgres_engine.dispose()

        assert postgres_engine.pool is not original_pool
        configure_engine(postgres_engine, RdkitSettings(tanimoto_threshold=0.6))
        configure_engine(postgres_engine, RdkitSettings())

    def test_listener_restores_connection_state_after_execute_error(
        self, postgres_engine, monkeypatch
    ):
        registered = []
        monkeypatch.setattr(
            settings_module.event,
            "listen",
            lambda target, name, listener: registered.append(listener),
        )
        configure_engine(postgres_engine, RdkitSettings(dice_threshold=0.6))
        cursor = Mock()
        cursor.execute.side_effect = RuntimeError("database error")
        dbapi_connection = Mock()
        dbapi_connection.autocommit = False
        dbapi_connection.cursor.return_value = cursor

        with pytest.raises(RuntimeError, match="database error"):
            registered[0](dbapi_connection, Mock(), Mock())

        cursor.close.assert_called_once_with()
        assert dbapi_connection.autocommit is False

    def test_rejects_non_postgresql_engine(self):
        engine = create_engine("sqlite://")
        try:
            with pytest.raises(ValueError, match="PostgreSQL"):
                configure_engine(engine, RdkitSettings(tanimoto_threshold=0.5))
        finally:
            engine.dispose()


class TestSetTanimotoThreshold:
    def test_sets_threshold(self, session):
        set_tanimoto_threshold(session, 0.7)
        session.execute.assert_called_once()
        args = session.execute.call_args
        assert "rdkit.tanimoto_threshold" in str(args[0][0])
        assert "0.7" in str(args[0][0])

    def test_rejects_negative(self, session):
        with pytest.raises(ValueError, match=r"between 0\.0 and 1\.0"):
            set_tanimoto_threshold(session, -0.1)

    def test_rejects_above_one(self, session):
        with pytest.raises(ValueError, match=r"between 0\.0 and 1\.0"):
            set_tanimoto_threshold(session, 1.1)

    def test_rejects_non_numeric(self, session):
        with pytest.raises(TypeError, match="must be a float"):
            set_tanimoto_threshold(session, "0.5")

    def test_accepts_zero(self, session):
        set_tanimoto_threshold(session, 0.0)
        session.execute.assert_called_once()

    def test_accepts_one(self, session):
        set_tanimoto_threshold(session, 1.0)
        session.execute.assert_called_once()


class TestSetDiceThreshold:
    def test_sets_threshold(self, session):
        set_dice_threshold(session, 0.6)
        session.execute.assert_called_once()
        args = session.execute.call_args
        assert "rdkit.dice_threshold" in str(args[0][0])
        assert "0.6" in str(args[0][0])

    def test_rejects_invalid(self, session):
        with pytest.raises(ValueError):
            set_dice_threshold(session, 2.0)


class TestGetTanimotoThreshold:
    def test_returns_float(self, session):
        result = get_tanimoto_threshold(session)
        assert result == 0.5
        assert isinstance(result, float)


class TestGetDiceThreshold:
    def test_returns_float(self, session):
        result = get_dice_threshold(session)
        assert result == 0.5
        assert isinstance(result, float)


class TestSimilarityThreshold:
    def test_sets_and_restores_tanimoto(self, session):
        session.execute.return_value.scalar_one.return_value = "0.5"

        with similarity_threshold(session, tanimoto=0.8):
            pass

        # Should have: SHOW (get old), SET 0.8, SET 0.5 (restore)
        assert session.execute.call_count == 3

    def test_sets_and_restores_dice(self, session):
        session.execute.return_value.scalar_one.return_value = "0.6"

        with similarity_threshold(session, dice=0.3):
            pass

        assert session.execute.call_count == 3

    def test_sets_and_restores_both(self, session):
        session.execute.return_value.scalar_one.return_value = "0.5"

        with similarity_threshold(session, tanimoto=0.8, dice=0.3):
            pass

        # SHOW tanimoto, SET tanimoto, SHOW dice, SET dice, SET tanimoto (restore), SET dice (restore)
        assert session.execute.call_count == 6

    def test_restores_on_exception(self, session):
        session.execute.return_value.scalar_one.return_value = "0.5"

        with pytest.raises(RuntimeError):
            with similarity_threshold(session, tanimoto=0.8):
                raise RuntimeError("test error")

        # Should still restore: SHOW, SET 0.8, SET 0.5 (restore)
        assert session.execute.call_count == 3

    def test_noop_when_no_thresholds(self, session):
        with similarity_threshold(session):
            pass

        session.execute.assert_not_called()
