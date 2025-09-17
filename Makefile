

test:
	@uv run pytest tests/ --cov=src/molalchemy --cov-report=term-missing --cov-report=xml

sync-docs:
	@cp README.md docs/index.md
	@cp CHANGELOG.md docs/changelog.md
	@cp ROADMAP.md docs/roadmap.md
	@cp CONTRIBUTING.md docs/contributing.md