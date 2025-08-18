# Format all Python files
format:
    uv run ruff format
    uv run ruff check --fix . */*/*.py

# Run type checking with mypy
mypy:
    uv run mypy */*/*.py

# Run linting with ruff
lint:
    uv run ruff check . */*/*.py

# Run all checks (lint + mypy)
check: lint mypy

# Install dependencies
install:
    uv sync

# Show help
help:
    @just --list