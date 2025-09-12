This project uses uv to manage its dependencies. To activate the virtual environment, run:

```source .venv/bin/activate
```
in the project root directory.

Alternatively, you can use `uv run some_python_script.py` to run a script within the virtual environment without activating it.

When the docstrings are added they should use numpydoc style. See https://numpydoc.readthedocs.io/en/latest/ for details.

To install new dependencies, use `uv add package_name`. To remove dependencies, use `uv remove package_name`.

To install all dependencies listed in the `pyproject.toml` file, run:

```uv sync
```