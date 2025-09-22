

test:
	@uv run pytest tests/ --cov=src/molalchemy --cov-report=term-missing --cov-report=xml

sync-docs:
	@cp README.md docs/index.md
	@cp CHANGELOG.md docs/
	@cp ROADMAP.md docs/
	@cp CONTRIBUTING.md docs/