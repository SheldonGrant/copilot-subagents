# Building Modern CLI Tools with uv, click, and rich

A comprehensive guide to creating beautiful, installable CLI tools that can be run directly from GitHub branches using uv, click for argument parsing, and rich for beautiful terminal output.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation and Setup](#installation-and-setup)
3. [Project Structure](#project-structure)
4. [Building CLI Tools](#building-cli-tools)
5. [Testing Your CLI Tools](#testing-your-cli-tools)
6. [Installing from GitHub Branches](#installing-from-github-branches)
7. [Best Practices](#best-practices)
8. [Example Implementation](#example-implementation)

## Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher
- Git installed and configured
- Basic knowledge of Python and command-line interfaces

## Installation and Setup

### Installing uv

uv is a fast Python package installer and resolver. Install it using the standalone installer:

**macOS and Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative (using pip):**
```bash
pip install uv
```

**Verify Installation:**
```bash
uv --version
```

### Setting up Your Development Environment

Create a workspace for your CLI projects:

```bash
mkdir ~/cli-projects
cd ~/cli-projects
```

## Project Structure

Following the repository's conventions, create a well-organized project structure:

```
├── ./src/                    # Source code (following project layout)
│   └── my_cli_tool/
│       ├── README.md       # guide on how to use the cli tool here
│       ├── pyproject.toml  # cli tool pyproject configuration and dependencies
│       ├── src/            # source code for the project. Designed to follow a nested structure
│       │       ├── __init__.py
│       │       ├── cli.py          # Main CLI entry point
│       │       └── commands/       # Command modules
│       │           ├── __init__.py
│       │           ├── hello.py
│       │           └── info.py
├── ./test/                   # Tests directory (following project layout)
│   └── Tests.my_cli_tool/
│       ├── README.md       # guide on how to test the cli tool here
│       ├── __init__.py
│       ├── test_cli.py
│       └── test_commands.py
```

## Building CLI Tools

### 1. Project Configuration (pyproject.toml)

Create your project configuration file:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-cli-tool"
version = "0.1.0"
description = "A beautiful CLI tool built with uv, click, and rich"
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "click>=8.0.0",
    "rich>=13.0.0",
]

# CLI entry point
[project.scripts]
my-cli = "my_cli_tool.cli:cli"

[project.urls]
Homepage = "https://github.com/yourusername/my-cli-tool"
Repository = "https://github.com/yourusername/my-cli-tool"

# Development dependencies
[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "black>=22.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]
```

### 2. Initialize Your Project

```bash
# Create project directory
mkdir my-cli-tool && cd my-cli-tool

# Initialize with uv
uv init

# Create the src structure
mkdir -p src/my_cli_tool/commands
mkdir -p test/Tests.my_cli_tool
mkdir -p .docs/guides

# Install dependencies
uv add click rich

# Install development dependencies
uv add --dev pytest black ruff mypy
```

### 3. Core CLI Module

**src/my_cli_tool/__init__.py**
```python
"""A beautiful CLI tool built with uv, click, and rich."""

__version__ = "0.1.0"
```

**src/my_cli_tool/cli.py**
```python
"""Main CLI module."""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from .commands import hello, info

console = Console()

@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):
    """A beautiful CLI tool built with uv, click, and rich."""
    ctx.ensure_object(dict)
    ctx.obj['console'] = console

# Register subcommands
cli.add_command(hello.hello)
cli.add_command(info.info)

@cli.command()
def welcome():
    """Display a welcome message with available commands."""
    welcome_text = Text("Welcome to My CLI Tool!", style="bold blue")
    
    panel = Panel(
        welcome_text,
        title="🚀 Getting Started",
        border_style="blue",
        padding=(1, 2)
    )
    
    console.print(panel)
    
    # Create command reference table
    table = Table(title="Available Commands", show_header=True, header_style="bold magenta")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    
    table.add_row("hello", "Say hello with customizable styles")
    table.add_row("info", "Display system information")
    table.add_row("welcome", "Show this welcome message")
    
    console.print(table)

if __name__ == "__main__":
    cli()
```

### 4. Command Modules

**src/my_cli_tool/commands/__init__.py**
```python
"""Command modules for the CLI tool."""
```

**src/my_cli_tool/commands/hello.py**
```python
"""Hello command with rich styling options."""

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

@click.command()
@click.option('--name', '-n', default='World', help='Name to greet')
@click.option('--style', '-s', 
              type=click.Choice(['simple', 'fancy', 'rainbow']), 
              default='simple',
              help='Greeting style')
@click.option('--repeat', '-r', default=1, type=int, help='Number of times to repeat greeting')
@click.pass_context
def hello(ctx, name, style, repeat):
    """Say hello with customizable style and repetition."""
    console = ctx.obj['console']
    
    for i in range(repeat):
        if style == 'simple':
            console.print(f"Hello, {name}!", style="bold green")
        elif style == 'fancy':
            greeting = Text(f"🎉 Hello, {name}! 🎉", style="bold magenta")
            panel = Panel(greeting, border_style="magenta", padding=(1, 2))
            console.print(panel)
        elif style == 'rainbow':
            greeting = Text(f"Hello, {name}!")
            greeting.stylize("bold red", 0, 5)
            greeting.stylize("bold yellow", 5, 7)
            greeting.stylize("bold green", 7, len(greeting))
            console.print(greeting)
        
        if repeat > 1 and i < repeat - 1:
            console.print()  # Add spacing between repetitions
```

**src/my_cli_tool/commands/info.py**
```python
"""System information command."""

import platform
import sys
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

@click.command()
@click.option('--detailed', '-d', is_flag=True, help='Show detailed system information')
@click.option('--format', '-f', 
              type=click.Choice(['table', 'json']), 
              default='table',
              help='Output format')
@click.pass_context
def info(ctx, detailed, format):
    """Display system information in various formats."""
    console = ctx.obj['console']
    
    # Collect system information
    info_data = {
        "Python Version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "Platform": platform.system(),
        "Architecture": platform.machine(),
    }
    
    if detailed:
        info_data.update({
            "Platform Release": platform.release(),
            "Platform Version": platform.version(),
            "Processor": platform.processor() or "Unknown",
            "Python Implementation": platform.python_implementation(),
            "Python Executable": sys.executable,
        })
    
    if format == 'json':
        import json
        console.print_json(json.dumps(info_data, indent=2))
    else:
        # Create table format
        table = Table(title="System Information", show_header=True, header_style="bold cyan")
        table.add_column("Property", style="yellow", no_wrap=True)
        table.add_column("Value", style="green")
        
        for key, value in info_data.items():
            table.add_row(key, str(value))
        
        panel = Panel(table, border_style="cyan", padding=(1, 1))
        console.print(panel)
```

## Testing Your CLI Tools

### 1. Test Structure

Following the project layout, create tests in the `test/` directory:

**test/Tests.my_cli_tool/__init__.py**
```python
"""Tests for my_cli_tool."""
```

**test/Tests.my_cli_tool/test_cli.py**
```python
"""Tests for the main CLI functionality."""

import pytest
from click.testing import CliRunner
from my_cli_tool.cli import cli

def test_main_command():
    """Test the main command group."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert "A beautiful CLI tool" in result.output

def test_welcome_command():
    """Test the welcome command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['welcome'])
    assert result.exit_code == 0
    assert "Welcome to My CLI Tool!" in result.output

def test_version_option():
    """Test version option."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
```

**test/Tests.my_cli_tool/test_commands.py**
```python
"""Tests for individual commands."""

import pytest
from click.testing import CliRunner
from my_cli_tool.cli import cli

class TestHelloCommand:
    """Tests for the hello command."""
    
    def test_hello_default(self):
        """Test hello command with default parameters."""
        runner = CliRunner()
        result = runner.invoke(cli, ['hello'])
        assert result.exit_code == 0
        assert "Hello, World!" in result.output
    
    def test_hello_with_name(self):
        """Test hello command with custom name."""
        runner = CliRunner()
        result = runner.invoke(cli, ['hello', '--name', 'Developer'])
        assert result.exit_code == 0
        assert "Hello, Developer!" in result.output
    
    def test_hello_with_style(self):
        """Test hello command with different styles."""
        runner = CliRunner()
        result = runner.invoke(cli, ['hello', '--style', 'fancy'])
        assert result.exit_code == 0
    
    def test_hello_with_repeat(self):
        """Test hello command with repeat option."""
        runner = CliRunner()
        result = runner.invoke(cli, ['hello', '--repeat', '2'])
        assert result.exit_code == 0

class TestInfoCommand:
    """Tests for the info command."""
    
    def test_info_basic(self):
        """Test basic info command."""
        runner = CliRunner()
        result = runner.invoke(cli, ['info'])
        assert result.exit_code == 0
        assert "System Information" in result.output
    
    def test_info_detailed(self):
        """Test detailed info command."""
        runner = CliRunner()
        result = runner.invoke(cli, ['info', '--detailed'])
        assert result.exit_code == 0
    
    def test_info_json_format(self):
        """Test info command with JSON format."""
        runner = CliRunner()
        result = runner.invoke(cli, ['info', '--format', 'json'])
        assert result.exit_code == 0
```

### 2. Running Tests

```bash
# Install your package in development mode
uv pip install -e .

# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src/my_cli_tool

# Run specific test file
uv run pytest test/Tests.my_cli_tool/test_cli.py

# Run with verbose output
uv run pytest -v
```

### 3. Development Testing

Test your CLI during development:

```bash
# Run directly with uv
uv run python -m my_cli_tool.cli welcome

# Test specific commands
uv run python -m my_cli_tool.cli hello --name "Developer" --style fancy
uv run python -m my_cli_tool.cli info --detailed --format json

# Install in development mode and test globally
uv pip install -e .
my-cli welcome
```

## Installing from GitHub Branches

Once your CLI tool is pushed to GitHub, users can install it directly using `uvx`:

### Basic Installation

```bash
# Install from main branch
uvx --from git+https://github.com/yourusername/my-cli-tool my-cli

# Install from specific branch
uvx --from git+https://github.com/yourusername/my-cli-tool@development my-cli

# Install from feature branch
uvx --from git+https://github.com/yourusername/my-cli-tool@feature/new-commands my-cli
```

### Advanced Installation Options

```bash
# Install from specific tag
uvx --from git+https://github.com/yourusername/my-cli-tool@v1.0.0 my-cli

# Install from specific commit
uvx --from git+https://github.com/yourusername/my-cli-tool@abc1234 my-cli

# Install with custom name
uvx --from git+https://github.com/yourusername/my-cli-tool@main my-awesome-cli

# Install in isolated environment
uvx --from git+https://github.com/yourusername/my-cli-tool my-cli --with rich --with click
```

### Usage After Installation

```bash
# Use your CLI tool globally
my-cli welcome
my-cli hello --name "World" --style rainbow --repeat 3
my-cli info --detailed --format json
```

## Best Practices

### 1. Code Quality

```bash
# Format code with black
uv run black src/ test/

# Lint with ruff
uv run ruff check src/ test/

# Type checking with mypy
uv run mypy src/

# Run all quality checks
uv run black src/ test/ && uv run ruff check src/ test/ && uv run mypy src/
```

### 2. Error Handling

Implement robust error handling:

```python
import sys
from rich.console import Console

def handle_error(error_msg: str, exit_code: int = 1):
    """Handle errors gracefully with rich formatting."""
    console = Console(stderr=True)
    console.print(f"❌ Error: {error_msg}", style="bold red")
    sys.exit(exit_code)

# Usage in commands
try:
    # Your command logic here
    pass
except Exception as e:
    handle_error(f"Command failed: {str(e)}")
```

### 3. Configuration Management

Add configuration file support:

```python
import click
from pathlib import Path
import json

@click.group()
@click.option('--config', 
              type=click.Path(exists=True, path_type=Path),
              help='Path to configuration file')
@click.pass_context
def cli(ctx, config):
    """Main CLI with configuration support."""
    ctx.ensure_object(dict)
    if config:
        with open(config) as f:
            ctx.obj['config'] = json.load(f)
    else:
        ctx.obj['config'] = {}
```

### 4. Progress Indicators

Use rich for long-running operations:

```python
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

@click.command()
@click.pass_context
def process(ctx):
    """Process with progress indication."""
    console = ctx.obj['console']
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Processing...", total=None)
        
        # Simulate work
        for i in range(10):
            time.sleep(0.5)
            progress.update(task, description=f"Step {i+1}/10")
        
        progress.update(task, description="Complete!")
    
    console.print("✅ Processing finished!", style="bold green")
```

## Example Implementation

Here's a complete working example following all the guidelines:

### Repository Setup

```bash
# Create new project
mkdir awesome-cli-tool
cd awesome-cli-tool

# Initialize project structure
uv init
mkdir -p src/awesome_cli/commands
mkdir -p test/Tests.awesome_cli
mkdir -p .docs/guides

# Set up dependencies
uv add click rich
uv add --dev pytest black ruff mypy

# Create all necessary files
touch src/awesome_cli/__init__.py
touch src/awesome_cli/cli.py
touch src/awesome_cli/commands/__init__.py
touch test/Tests.awesome_cli/__init__.py
touch test/Tests.awesome_cli/test_cli.py
```

### Development Workflow

```bash
# 1. Develop your CLI
# ... (create your CLI code as shown above)

# 2. Test locally
uv pip install -e .
awesome-cli welcome

# 3. Run tests
uv run pytest

# 4. Quality checks
uv run black src/ test/
uv run ruff check src/ test/
uv run mypy src/

# 5. Commit and push to GitHub
git add .
git commit -m "Add awesome CLI tool"
git push origin main

# 6. Install from GitHub
uvx --from git+https://github.com/yourusername/awesome-cli-tool awesome-cli
```

### Distribution

Once your tool is ready:

1. **Tag releases:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Share installation commands:**
   ```bash
   # Latest release
   uvx --from git+https://github.com/yourusername/awesome-cli-tool@v1.0.0 awesome-cli
   
   # Development version
   uvx --from git+https://github.com/yourusername/awesome-cli-tool@main awesome-cli
   ```

This comprehensive guide provides everything needed to create, test, and distribute modern CLI tools using uv, click, and rich, while following the project's established conventions and best practices.