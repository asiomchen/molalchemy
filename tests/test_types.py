from molalchemy.types import CString
from sqlalchemy import Table, Column, Integer, MetaData


class TestCString:
    """Test CString type."""

    def test_cstring_cache_ok(self):
        """Test that CString has cache_ok=True."""
        cstring = CString()
        assert cstring.cache_ok is True

    def test_cstring_col_spec(self):
        """Test that CString returns correct column specification."""
        cstring = CString()
        assert cstring.get_col_spec() == "cstring"

    def test_cstring_in_table_definition(self):
        """Test CString can be used in table definition."""
        metadata = MetaData()
        test_table = Table(
            "test_cstrings",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", CString()),
        )

        # Should not raise any exceptions
        assert test_table.c.name.type.__class__ == CString
        assert isinstance(test_table.c.name.type, CString)
