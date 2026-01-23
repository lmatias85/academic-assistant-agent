.PHONY: help format lint typecheck check

help:
	@echo "Available commands:"
	@echo "  make format     -> Format code with black"
	@echo "  make lint       -> Lint code with flake8"
	@echo "  make typecheck  -> Run mypy type checks"
	@echo "  make check      -> Run all quality checks"

format:
	black .

lint:
	flake8 .

typecheck:
	mypy .

check: format lint typecheck