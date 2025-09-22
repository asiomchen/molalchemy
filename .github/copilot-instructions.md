This project uses uv to manage its dependencies. To activate the virtual environment, run:

```source .venv/bin/activate
```
in the project root directory.

Alternatively, you can use `uv run some_python_script.py` to run a script within the virtual environment without activating it.

When the docstrings are added they should use numpydoc style. See https://numpydoc.readthedocs.io/en/latest/ for details. When using types or functions from other modules please use full paths, e.g. `molalchemy.bingo.types.BingoMol`. When using literals enclose them in backticks, e.g. `"smiles"`, `42`, or `True`. For SQLAlchemy examples prefer using the typed declarative ORM style.

To install new dependencies, use `uv add package_name`. To remove dependencies, use `uv remove package_name`.

To install all dependencies listed in the `pyproject.toml` file, run:

```uv sync
```

If you need to check bingo cartridge docs look at `docs/bingo-postgres-manual.md`
If you need to check rdkit cartridge docs look at `docs/rdkit-postgres-manual.md`