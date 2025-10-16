# COLLABORATION GUIDE: Copilot subagents

## Overview

Copilot subagents provides github copilot prompts, instructions to run subagent flows based on the copilot CLI.

---

## Project Layout

|- .docs/ || provides a set of docs for this repository
|   |- guides/ || contains all guides and tutorials on concepts used in this repository.
|   |   |- building-cli-tools-with-uv.md || provides a guide on how to build new cli projects
|- src/ || source directory for any tools and code written in this project.
|   |- <project name>
|- test/ || test directory for tests for any tools and code found in ./src
|   |- Tests.<project name>
|- CONTRIBUTING.md || You are here
|- README.md || overview of this repository

## Installing the Subagents CLI

The `subagents` CLI tool provides commands for managing GitHub Copilot subagents with tool verification and execution. You can install it using `uv` in two ways:

### A) Installing within this project (Development)

For local development and contribution to this repository:

```bash
# Clone the repository
git clone https://github.com/SheldonGrant/copilot-subagents.git
cd copilot-subagents

# create a new venv
uv venv

# Install in development mode using uv
uv pip install -e ./src/copilot_subagents

# Verify installation
uv run subagents --help
```

### B) Installing from remote GitHub URL

For users who want to install the latest version directly from GitHub:

```bash
# Install latest from main branch
uvx --from git+https://github.com/SheldonGrant/copilot-subagents.git#subdirectory=src/copilot_subagents subagents

# Install from specific branch
uvx --from git+https://github.com/SheldonGrant/copilot-subagents.git@first_steps#subdirectory=src/copilot_subagents subagents

# Install from specific tag (when available)
uvx --from git+https://github.com/SheldonGrant/copilot-subagents.git@v1.0.0#subdirectory=src/copilot_subagents subagents
```

**Note:** The `#subdirectory=src/copilot_subagents` part is required because the CLI tool is located in a subdirectory of the repository.

### Verifying Installation

After installation, verify the CLI is working correctly:

```bash
# Check version and help
uv run subagents --help

# List available subagents
uv run subagents list

# Show tool permissions for a specific subagent
uv run subagents show-tools code-reviewer

# Verify a subagent configuration
uv run subagents verify code-reviewer
```

### Available Commands

- `subagents list` - List all available subagents
- `subagents invoke <name> --prompt "<prompt>"` - Execute a subagent with a specific prompt
- `subagents verify <name>` - Verify subagent configuration and tool permissions  
- `subagents show-tools <name>` - Display tool permissions for a subagent

For detailed usage examples, see the [building CLI tools guide](.docs/guides/building-cli-tools-with-uv.md).

## Git Commit Best Practices

The required git commit policies to follow.
NOTE: !! do not change this.

**Git Commands**

- Use the `git status` command to get a clear view of what you are updating.
- Add and commit your changes with a helpful message using `git add -A && git commit -m '[HELPFUL COMMIT MESSAGE HERE]'`

**Basic Rules**
- Git commits should be a wrapper for related changes. For example, fixing two different bugs should produce two separate commits. 
- Commit Often to keep your commits small to enable better reporting on changes and git history management.
- Don't Commit Half-Done Work, only commit code when a logical component is completed. Split a feature's implementation into logical chunks that can be completed quickly so that you can commit often.
- Test Your Code Before You Commit. Follow the Debugging Strategies.
- Resist the temptation to commit something that you «think» is completed. Test it thoroughly by making sure the code builds.
