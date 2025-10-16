"""Subagent invocation command."""

import subprocess
import sys
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from core import SubagentParser, ToolVerifier, format_copilot_tools, get_default_subagents_dir

console = Console()

@click.command()
@click.argument('subagent_name', required=False)
@click.option('--prompt', '-p', 
              help='Custom prompt/task for the subagent')
@click.option('--context', '-c',
              help='Additional context for the subagent')
@click.option('--subagents-dir', '-d',
              type=click.Path(exists=True, path_type=Path),
              help='Path to subagents directory (default from COPILOT_SUBAGENTS_SUBAGENTS_DIR env var or .github/subagents)')
@click.option('--valid-tools-file', '-v',
              type=click.Path(exists=True, path_type=Path),
              help='Path to file containing valid tools list')
@click.option('--dry-run', '--dry',
              is_flag=True,
              help='Show the copilot command that would be executed without running it')
@click.option('--verify-tools/--skip-verification',
              default=True,
              help='Verify tools before execution (default: enabled)')
@click.pass_context
def invoke(ctx, subagent_name, prompt, context, subagents_dir, valid_tools_file, 
           dry_run, verify_tools):
    """Invoke a subagent using GitHub Copilot CLI with proper tool restrictions."""
    
    # Use provided directory or fall back to environment variable/default
    if subagents_dir is None:
        subagents_dir = get_default_subagents_dir()
    parser = SubagentParser(subagents_dir)
    
    # Validate required arguments
    if not subagent_name:
        console.print("❌ Error: subagent_name is required (use 'subagents list' to see available subagents)", style="red")
        ctx.exit(1)
    
    if not prompt:
        console.print("❌ Error: --prompt is required for subagent invocation", style="red")
        ctx.exit(1)
    
    try:
        # Verify subagent exists and parse it
        console.print(f"🔍 Loading subagent '{subagent_name}'...", style="cyan")
        
        # Parse the full subagent data including model
        subagent_data = parser.parse_file(f"{subagents_dir}/{subagent_name}.md")
        allowed_tools = subagent_data['tools']['allowed']
        denied_tools = subagent_data['tools']['denied']
        subagent_prompt = subagent_data['prompt']
        model = subagent_data.get('model', '')
        
        # Verify tools if requested
        if verify_tools:
            _verify_subagent_tools(subagent_name, allowed_tools, denied_tools, valid_tools_file)
        
        # Build the full prompt
        full_prompt = _build_full_prompt(subagent_prompt, prompt, context)
        
        # Format tool flags and model
        allowed_flags = format_copilot_tools(allowed_tools, "allow")
        denied_flags = format_copilot_tools(denied_tools, "deny")
        
        # Format model flags using the AI verifier
        from core import get_ai_tool_verifier
        verifier = get_ai_tool_verifier("copilot-cli")
        model_flags = verifier.format_model(model)
        
        # Build copilot command
        copilot_cmd = _build_copilot_command(full_prompt, allowed_flags, denied_flags, model_flags)
        
        # Display execution info
        _display_execution_info(subagent_name, allowed_tools, denied_tools, model, full_prompt, copilot_cmd)
        
        if dry_run:
            console.print("\n🏃 [yellow]Dry run mode - command would be:[/yellow]")
            console.print(f"[dim]{copilot_cmd}[/dim]")
            return
        
        # Execute copilot command
        _execute_copilot_command(copilot_cmd)
        
    except FileNotFoundError as e:
        console.print(f"❌ Error: {e}", style="red")
        _suggest_available_subagents(parser)
        ctx.exit(1)
    except ValueError as e:
        console.print(f"❌ Error parsing subagent file: {e}", style="red")
        ctx.exit(1)
    except Exception as e:
        console.print(f"❌ Unexpected error: {e}", style="red")
        ctx.exit(1)


def _verify_subagent_tools(subagent_name: str, allowed_tools: List[str], 
                          denied_tools: List[str], valid_tools_file: Optional[Path]):
    """Verify both allowed and denied tools."""
    # For now, we default to copilot-cli (ignoring valid_tools_file parameter for now)
    verifier = ToolVerifier("copilot-cli")
    
    all_issues = []
    
    # Verify allowed tools
    if allowed_tools:
        _, invalid_allowed = verifier.verify_tools(allowed_tools)
        if invalid_allowed:
            all_issues.extend([f"Invalid allowed tool: {tool}" for tool in invalid_allowed])
    
    # Verify denied tools
    if denied_tools:
        _, invalid_denied = verifier.verify_tools(denied_tools)
        if invalid_denied:
            all_issues.extend([f"Invalid denied tool: {tool}" for tool in invalid_denied])
    
    if all_issues:
        error_panel = Panel(
            f"[red]Tool verification failed for '{subagent_name}':[/red]\n" +
            "\n".join([f"• {issue}" for issue in all_issues]),
            title="⚠️  Tool Verification Failed",
            border_style="red"
        )
        console.print(error_panel)
        raise ValueError("Tool verification failed")
    else:
        console.print("✅ All tools verified successfully", style="green")

def _build_full_prompt(subagent_prompt: str, user_prompt: str, context: Optional[str] = None) -> str:
    """Build the complete prompt for the subagent."""
    full_prompt = subagent_prompt
    
    if context:
        full_prompt += f"\n\nContext: {context}"
    
    full_prompt += f"\n\nTask: {user_prompt}"
    
    return full_prompt

def _build_copilot_command(prompt: str, allowed_flags: str, denied_flags: str, model_flags: str = "") -> List[str]:
    """Build the copilot CLI command."""
    cmd = ["copilot"]
    
    # Add model flag first if specified
    if model_flags:
        flags = model_flags.split()
        cmd.extend(flags)
    
    # Add prompt
    cmd.extend(["-p", prompt])
    
    if allowed_flags:
        # Split and add each flag
        flags = allowed_flags.split()
        cmd.extend(flags)
    
    if denied_flags:
        # Split and add each flag  
        flags = denied_flags.split()
        cmd.extend(flags)
    
    return cmd

def _display_execution_info(subagent_name: str, allowed_tools: List[str], 
                           denied_tools: List[str], model: str, prompt: str, command: List[str]):
    """Display information about the execution."""
    
    # Tools summary
    tools_table = Table(title=f"Subagent Configuration: {subagent_name}", 
                       show_header=True, header_style="bold cyan")
    tools_table.add_column("Type", style="yellow")
    tools_table.add_column("Count", style="green")
    tools_table.add_column("Tools", style="blue")
    
    allowed_str = ", ".join(allowed_tools) if allowed_tools else "None"
    denied_str = ", ".join(denied_tools) if denied_tools else "None"
    
    tools_table.add_row("Allowed", str(len(allowed_tools)), allowed_str)
    tools_table.add_row("Denied", str(len(denied_tools)), denied_str)
    if model:
        tools_table.add_row("Model", "1", model)
    
    console.print(tools_table)
    
    # Prompt preview
    prompt_preview = prompt[:200] + "..." if len(prompt) > 200 else prompt
    prompt_panel = Panel(
        f"[dim]{prompt_preview}[/dim]",
        title="Prompt Preview",
        border_style="green"
    )
    console.print(prompt_panel)

def _execute_copilot_command(command: List[str]):
    """Execute the copilot CLI command."""
    console.print("\n🚀 [bold green]Executing GitHub Copilot CLI...[/bold green]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Running copilot command...", total=None)
        
        try:
            # Execute the command
            result = subprocess.run(
                command,
                capture_output=False,  # Let copilot handle its own output
                text=True,
                check=True
            )
            
            progress.update(task, description="Complete!")
            console.print("✅ [bold green]Copilot execution completed successfully![/bold green]")
            
        except subprocess.CalledProcessError as e:
            progress.stop()
            console.print(f"❌ [red]Copilot execution failed with exit code {e.returncode}[/red]")
            sys.exit(e.returncode)
        except FileNotFoundError:
            progress.stop()
            console.print("❌ [red]GitHub Copilot CLI not found. Please ensure it's installed and in your PATH.[/red]")
            console.print("Install instructions: https://docs.github.com/en/copilot/github-copilot-in-the-cli")
            sys.exit(1)

def _suggest_available_subagents(parser: SubagentParser):
    """Suggest available subagents when one is not found."""
    subagents = parser.list_subagents()
    if subagents:
        console.print(f"\n💡 Available subagents: {', '.join(subagents)}", style="dim")
        console.print("Use 'subagents list' to see detailed information", style="dim")