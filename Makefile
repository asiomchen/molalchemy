

test:
	@uv run pytest tests/ --cov=src/molalchemy --cov-report=term-missing --cov-report=xml

sync-docs:
	@cp README.md docs/index.md
	@cp CHANGELOG.md docs/
	@cp ROADMAP.md docs/
	@cp CONTRIBUTING.md docs/

update-rdkit-func:
	@uv run python dev_scripts/gen_functions.py rdkit
	@ruff format src/molalchemy/rdkit/functions/
	@ruff check --fix src/molalchemy/rdkit/functions/

update-bingo-func:
	@uv run python dev_scripts/gen_functions.py bingo
	@ruff format src/molalchemy/bingo/functions/
	@ruff check --fix src/molalchemy/bingo/functions/

update-func: update-rdkit-func update-bingo-func