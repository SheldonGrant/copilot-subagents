"""List command for subagents."""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from core import SubagentParser, get_default_subagents_dir, get_ai_tool_verifier, get_supported_ai_tools

console = Console()

@click.command()
@click.option('--subagents-dir', '-d',
              type=click.Path(exists=True, path_type=Path),
              help='Path to subagents directory (default from COPILOT_SUBAGENTS_SUBAGENTS_DIR env var or .github/subagents)')
@click.pass_context
def list_subagents(ctx, subagents_dir):
    """List all available subagents."""
    try:
        # Use provided directory or fall back to environment variable/default
        if subagents_dir is None:
            subagents_dir = get_default_subagents_dir()
        parser = SubagentParser(subagents_dir)
        
        subagents = parser.list_subagents()
        
        if not subagents:
            console.print("📭 No subagents found in subagents directory", style="yellow")
            console.print(f"Directory: {subagents_dir}", style="dim")
            return
        
        table = Table(title="Available Subagents", show_header=True, header_style="bold magenta")
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="green")
        table.add_column("Allowed Tools", style="blue")
        table.add_column("Denied Tools", style="red")
        
        for subagent in subagents:
            try:
                frontmatter, _ = parser.parse_subagent_file(subagent)
                description = frontmatter.get('description', 'No description')
                allowed = frontmatter.get('allowed_tools', [])
                denied = frontmatter.get('deny_tools', [])
                
                allowed_str = f"{len(allowed)} tools" if allowed else "None"
                denied_str = f"{len(denied)} tools" if denied else "None"
                
                table.add_row(subagent, description, allowed_str, denied_str)
            except Exception:
                table.add_row(subagent, "[red]Error loading[/red]", "Unknown", "Unknown")
        
        console.print(table)
        
        # Show directory info
        info_panel = Panel(
            f"[dim]Subagents directory: {subagents_dir}[/dim]",
            border_style="dim"
        )
        console.print(info_panel)
        
    except Exception as e:
        console.print(f"❌ Error listing subagents: {e}", style="red")
        ctx.exit(1)


@click.command()
@click.argument('ai_tool_name')
@click.pass_context
def show_tools(ctx, ai_tool_name):
    """Show all valid tools for a specific AI tool.
    
    Arguments:
        AI_TOOL_NAME: The name of the AI tool (e.g., copilot-cli, claude-code, etc.)
    """
    try:
        # Validate that the AI tool is supported
        supported_tools = get_supported_ai_tools()
        if ai_tool_name not in supported_tools:
            console.print(f"❌ Unsupported AI tool: '{ai_tool_name}'", style="red")
            console.print(f"Supported AI tools: {', '.join(supported_tools)}", style="yellow")
            ctx.exit(1)
        
        # Get the verifier for the specified AI tool
        verifier = get_ai_tool_verifier(ai_tool_name)
        valid_tools = verifier.get_valid_tools()
        
        if not valid_tools:
            console.print(f"📭 No valid tools found for AI tool '{ai_tool_name}'", style="yellow")
            return
        
        # Create a table to display the tools
        table = Table(title=f"Valid Tools for {ai_tool_name}", show_header=True, header_style="bold magenta")
        table.add_column("Tool Name", style="cyan", no_wrap=True)
        table.add_column("Description", style="green")
        
        # Add tool descriptions (basic for now, can be enhanced later)
        tool_descriptions = {
            'write': 'Create, edit, and modify files',
            'shell(*)': 'Execute any shell commands',
            'shell(git)': 'Execute git-specific commands',
            'create_file': 'Create new files',
            'read_file': 'Read existing files',
            'edit_file': 'Edit existing files',
            'run_terminal': 'Execute terminal commands',
            'list_directory': 'List directory contents',
            'search_files': 'Search within files',
            'web_search': 'Search the web',
            'code_analysis': 'Analyze code structure',
            'file_operations': 'General file operations',
            'execute_code': 'Execute code snippets',
            'search_web': 'Web search functionality',
            'analyze_code': 'Code analysis and review',
            'debug_code': 'Debug code issues',
            'format_code': 'Format and style code',
            'file_read': 'Read file contents',
            'file_write': 'Write to files',
            'shell_execute': 'Execute shell commands',
            'web_browse': 'Browse web content',
            'code_review': 'Review code quality',
            'documentation_gen': 'Generate documentation',
            'test_generation': 'Generate test cases'
        }
        
        for tool in valid_tools:
            description = tool_descriptions.get(tool, 'Tool for AI assistant operations')
            table.add_row(tool, description)
        
        console.print(table)
        
        # Show additional info
        info_text = f"[dim]AI Tool: {ai_tool_name}[/dim]\n"
        info_text += f"[dim]Total Tools: {len(valid_tools)}[/dim]\n"
        if verifier.supports_yolo_mode():
            info_text += f"[dim]YOLO Mode: ✅ Supported[/dim]"
        else:
            info_text += f"[dim]YOLO Mode: ❌ Not supported[/dim]"
        
        info_panel = Panel(
            info_text,
            title="AI Tool Information",
            border_style="dim"
        )
        console.print(info_panel)
        
    except Exception as e:
        console.print(f"❌ Error showing tools for '{ai_tool_name}': {e}", style="red")
        ctx.exit(1)