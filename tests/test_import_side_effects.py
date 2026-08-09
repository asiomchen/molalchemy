"""Tests for package import behavior."""

import subprocess
import sys
import textwrap


def test_plain_import_does_not_register_cartridge_functions():
    script = textwrap.dedent(
        """
        import sys

        from sqlalchemy import func
        from sqlalchemy.sql.functions import Function, _registry
        from sqlalchemy.sql.sqltypes import NullType

        registry_before = {
            package: dict(functions) for package, functions in _registry.items()
        }

        import molalchemy
        import molalchemy.bingo as bingo
        import molalchemy.rdkit as rdkit

        registry_after = {
            package: dict(functions) for package, functions in _registry.items()
        }
        assert registry_after == registry_before
        assert "molalchemy.bingo.functions" not in sys.modules
        assert "molalchemy.rdkit.functions" not in sys.modules

        smiles = func.smiles("x")
        add = func.add("x", "y")
        assert type(smiles) is Function
        assert type(add) is Function
        assert smiles.packagenames == ()
        assert add.packagenames == ()
        assert isinstance(smiles.type, NullType)
        assert isinstance(add.type, NullType)

        from molalchemy.bingo import functions as bingo_functions
        from molalchemy.rdkit import functions as rdkit_functions

        assert bingo.functions is bingo_functions
        assert rdkit.functions is rdkit_functions
        assert bingo_functions.__name__ == "molalchemy.bingo.functions"
        assert rdkit_functions.__name__ == "molalchemy.rdkit.functions"
        """
    )

    subprocess.run([sys.executable, "-c", script], check=True)
