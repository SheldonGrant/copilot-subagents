"""Main CLI module for copilot subagents."""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from commands import verify, invoke, list

console = Console()

@click.group()
@click.version_option(version="0.1.0")
@click.pass_context
def cli(ctx):
    """Copilot Subagents - Manage GitHub Copilot subagents with tool verification."""
    ctx.ensure_object(dict)
    ctx.obj['console'] = console

# Register subcommands
cli.add_command(verify.verify_allowed_tools)
cli.add_command(verify.verify_denied_tools)
cli.add_command(invoke.invoke)
cli.add_command(list.list_subagents, name="list")
cli.add_command(list.show_tools, name="show-tools")

@cli.command()
def info():
    """Display information about the CLI tool and available commands."""
    info_text = Text("Copilot Subagents CLI", style="bold blue")
    
    panel = Panel(
        info_text,
        title="🤖 GitHub Copilot Subagents Manager",
        border_style="blue",
        padding=(1, 2)
    )
    
    console.print(panel)
    
    # Create command reference table
    table = Table(title="Available Commands", show_header=True, header_style="bold magenta")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    
    table.add_row("verify-allowed-tools", "Verify allowed tools against valid tools list")
    table.add_row("verify-denied-tools", "Verify denied tools against valid tools list")
    table.add_row("invoke", "Execute subagent using GitHub Copilot CLI")
    table.add_row("list", "List all available subagents")
    table.add_row("show-tools", "Show valid tools for a specific AI tool")
    table.add_row("info", "Show this information message")
    
    console.print(table)
    
    # Usage examples
    usage_panel = Panel(
        """[bold cyan]Examples:[/bold cyan]

[yellow]# Verify allowed tools for a subagent[/yellow]
subagents verify-allowed-tools code-reviewer

[yellow]# Verify denied tools for a subagent[/yellow] 
subagents verify-denied-tools security-scanner

[yellow]# Invoke a subagent with custom prompt[/yellow]
subagents invoke code-reviewer --prompt "Review this TypeScript file"

[yellow]# List all available subagents[/yellow]
subagents list

[yellow]# Show valid tools for an AI tool[/yellow]
subagents show-tools copilot-cli""",
        title="Usage Examples",
        border_style="green",
        padding=(1, 2)
    )
    
    console.print(usage_panel)

if __name__ == "__main__":
    cli()