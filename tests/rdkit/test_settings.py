"""Tests for RDKit similarity threshold settings helpers."""

from unittest.mock import Mock

import pytest

from molalchemy.rdkit.settings import (
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
