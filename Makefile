
SMOKE_COMPOSE ?= docker-compose.smoke.yaml
SMOKE_PROJECT ?= molalchemy-smoke
BINGO_SMOKE_PORT ?= 55432
RDKIT_SMOKE_PORT ?= 55433


test:
	@uv run pytest tests/ --cov=src/molalchemy --cov-report=term-missing --cov-report=xml

smoke-up:
	@BINGO_SMOKE_PORT=$(BINGO_SMOKE_PORT) RDKIT_SMOKE_PORT=$(RDKIT_SMOKE_PORT) docker compose -p $(SMOKE_PROJECT) -f $(SMOKE_COMPOSE) up -d

smoke-test:
	@BINGO_DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:$(BINGO_SMOKE_PORT)/postgres uv run python dev_scripts/validate_bingo_helpers.py
	@RDKIT_DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:$(RDKIT_SMOKE_PORT)/postgres uv run python dev_scripts/validate_rdkit_helpers.py

smoke-down:
	@BINGO_SMOKE_PORT=$(BINGO_SMOKE_PORT) RDKIT_SMOKE_PORT=$(RDKIT_SMOKE_PORT) docker compose -p $(SMOKE_PROJECT) -f $(SMOKE_COMPOSE) down -v

smoke:
	@$(MAKE) smoke-up
	@status=0; $(MAKE) smoke-test || status=$$?; $(MAKE) smoke-down; exit $$status


docs-test:
	@JUPYTER_PLATFORM_DIRS=1 uv run mkdocs build --strict --site-dir /tmp/molalchemy-site

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
