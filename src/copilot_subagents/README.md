# Copilot Subagents CLI Tool

A command-line tool for managing GitHub Copilot subagents with tool verification and execution capabilities.

## Features

- **Tool Verification**: Verify allowed and denied tools against a valid tools list
- **Subagent Invocation**: Execute subagents using GitHub Copilot CLI with proper tool restrictions
- **YAML Frontmatter Parsing**: Extract tool configurations from subagent markdown files

## Installation

Install directly from GitHub using `uvx`:

```bash
# Install from main branch
uvx --from git+https://github.com/SheldonGrant/copilot-subagents@main subagents

# Install from specific branch
uvx --from git+https://github.com/SheldonGrant/copilot-subagents@development subagents
```

## Usage

### Basic Commands

```bash
# Verify allowed tools for a subagent
subagents verify_allowed_tools my-subagent

# Verify denied tools for a subagent
subagents verify_denied_tools my-subagent

# Invoke a subagent with GitHub Copilot CLI
subagents invoke my-subagent --prompt "Your task here"
```

### Command Reference

| Command | Description |
|---------|-------------|
| `verify_allowed_tools` | Verify allowed tools against valid tools list |
| `verify_denied_tools` | Verify denied tools against valid tools list |
| `invoke` | Execute subagent with GitHub Copilot CLI |

## Development

```bash
# Install in development mode
uv pip install -e .

# Run tests
uv run pytest

# Format code
uv run black src/ test/
```

## Requirements

- Python 3.8+
- GitHub Copilot CLI installed and configured
- Subagent files in `.github/subagents/` directory