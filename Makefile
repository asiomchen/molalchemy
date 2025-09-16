

test:
	@uv run pytest tests/ --cov=src/molalchemy --cov-report=term-missing --cov-report=xml