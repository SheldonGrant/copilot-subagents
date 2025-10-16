"""Tool verification commands."""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from core import SubagentParser, ToolVerifier, get_default_subagents_dir

console = Console()

@click.command()
@click.argument('subagent_name')
@click.option('--valid-tools-file', '-v', 
              type=click.Path(exists=True, path_type=Path),
              help='Path to file containing valid tools list')
@click.option('--subagents-dir', '-d',
              type=click.Path(exists=True, path_type=Path),
              help='Path to subagents directory (default from COPILOT_SUBAGENTS_SUBAGENTS_DIR env var or .github/subagents)')
@click.pass_context
def verify_allowed_tools(ctx, subagent_name, valid_tools_file, subagents_dir):
    """Verify allowed tools for a subagent against the valid tools list."""
    try:
        # Use provided directory or fall back to environment variable/default
        if subagents_dir is None:
            subagents_dir = get_default_subagents_dir()
        parser = SubagentParser(subagents_dir)
        # For now, we default to copilot-cli (ignoring valid_tools_file parameter for now)
        verifier = ToolVerifier("copilot-cli")
        
        # Get allowed tools from subagent
        allowed_tools = parser.get_allowed_tools(subagent_name)
        
        if not allowed_tools:
            console.print(f"📝 No allowed tools found for subagent '{subagent_name}'", style="yellow")
            return
        
        # Verify tools
        valid_tools, invalid_tools = verifier.verify_tools(allowed_tools)
        
        # Create results table
        table = Table(title=f"Allowed Tools Verification: {subagent_name}", 
                     show_header=True, header_style="bold magenta")
        table.add_column("Tool", style="cyan")
        table.add_column("Status", style="bold")
        
        for tool in valid_tools:
            table.add_row(tool, "[green]✅ Valid[/green]")
        
        for tool in invalid_tools:
            table.add_row(tool, "[red]❌ Invalid[/red]")
        
        console.print(table)
        
        # Summary
        if invalid_tools:
            error_panel = Panel(
                f"[red]Found {len(invalid_tools)} invalid allowed tool(s):[/red]\n" +
                "\n".join([f"• {tool}" for tool in invalid_tools]),
                title="⚠️  Verification Failed",
                border_style="red"
            )
            console.print(error_panel)
            ctx.exit(1)
        else:
            success_panel = Panel(
                f"[green]All {len(valid_tools)} allowed tools are valid![/green]",
                title="✅ Verification Passed",
                border_style="green"
            )
            console.print(success_panel)
    
    except FileNotFoundError as e:
        console.print(f"❌ Error: {e}", style="red")
        ctx.exit(1)
    except ValueError as e:
        console.print(f"❌ Error parsing subagent file: {e}", style="red")
        ctx.exit(1)
    except Exception as e:
        console.print(f"❌ Unexpected error: {e}", style="red")
        ctx.exit(1)

@click.command()
@click.argument('subagent_name')
@click.option('--valid-tools-file', '-v',
              type=click.Path(exists=True, path_type=Path),
              help='Path to file containing valid tools list')
@click.option('--subagents-dir', '-d',
              type=click.Path(exists=True, path_type=Path),
              help='Path to subagents directory (default from COPILOT_SUBAGENTS_SUBAGENTS_DIR env var or .github/subagents)')
@click.pass_context
def verify_denied_tools(ctx, subagent_name, valid_tools_file, subagents_dir):
    """Verify denied tools for a subagent against the valid tools list."""
    try:
        # Use provided directory or fall back to environment variable/default
        if subagents_dir is None:
            subagents_dir = get_default_subagents_dir()
        parser = SubagentParser(subagents_dir)
        # For now, we default to copilot-cli (ignoring valid_tools_file parameter for now)
        verifier = ToolVerifier("copilot-cli")
        
        # Get denied tools from subagent
        denied_tools = parser.get_denied_tools(subagent_name)
        
        if not denied_tools:
            console.print(f"📝 No denied tools found for subagent '{subagent_name}'", style="yellow")
            return
        
        # Verify tools
        valid_tools, invalid_tools = verifier.verify_tools(denied_tools)
        
        # Create results table
        table = Table(title=f"Denied Tools Verification: {subagent_name}",
                     show_header=True, header_style="bold magenta")
        table.add_column("Tool", style="cyan")
        table.add_column("Status", style="bold")
        
        for tool in valid_tools:
            table.add_row(tool, "[green]✅ Valid[/green]")
        
        for tool in invalid_tools:
            table.add_row(tool, "[red]❌ Invalid[/red]")
        
        console.print(table)
        
        # Summary
        if invalid_tools:
            error_panel = Panel(
                f"[red]Found {len(invalid_tools)} invalid denied tool(s):[/red]\n" +
                "\n".join([f"• {tool}" for tool in invalid_tools]),
                title="⚠️  Verification Failed",
                border_style="red"
            )
            console.print(error_panel)
            ctx.exit(1)
        else:
            success_panel = Panel(
                f"[green]All {len(valid_tools)} denied tools are valid![/green]",
                title="✅ Verification Passed",
                border_style="green"
            )
            console.print(success_panel)
    
    except FileNotFoundError as e:
        console.print(f"❌ Error: {e}", style="red")
        ctx.exit(1)
    except ValueError as e:
        console.print(f"❌ Error parsing subagent file: {e}", style="red")
        ctx.exit(1)
    except Exception as e:
        console.print(f"❌ Unexpected error: {e}", style="red")
        ctx.exit(1)