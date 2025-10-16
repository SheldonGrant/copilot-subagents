# Testing Guide for Copilot Subagents CLI

This directory contains comprehensive tests for the copilot subagents CLI tool.

## Test Structure

- `test_cli.py` - Tests for the main CLI functionality and commands
- `test_core.py` - Tests for core parsing and verification logic

## Running Tests

### Prerequisites

Install the development dependencies:

```bash
cd src/copilot_subagents
uv add --dev pytest black ruff mypy
```

### Execute Tests

```bash
# Run all tests
uv run pytest test/Tests.copilot_subagents/

# Run with verbose output
uv run pytest -v test/Tests.copilot_subagents/

# Run specific test file
uv run pytest test/Tests.copilot_subagents/test_cli.py

# Run with coverage
uv run pytest --cov=src test/Tests.copilot_subagents/
```

### Test Categories

#### CLI Tests (`test_cli.py`)
- Main command group functionality
- Command-line argument parsing
- Help and version information
- Integration with temporary test files

#### Core Tests (`test_core.py`)
- YAML frontmatter parsing
- Tool verification logic
- Subagent file handling
- Error conditions and edge cases

## Test Data

Tests use temporary files and directories to avoid interfering with actual subagent configurations. Each test class creates its own isolated environment.

## Coverage

Aim for comprehensive coverage of:
- Happy path scenarios
- Error conditions
- Edge cases
- Command-line interface
- File parsing logic