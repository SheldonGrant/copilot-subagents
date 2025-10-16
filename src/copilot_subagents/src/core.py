"""Core utilities for parsing subagent files and managing tools."""

import os
import re
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from rich.console import Console
from dotenv import load_dotenv

# Load environment variables from .env file in current working directory
load_dotenv()

console = Console()

def get_default_subagents_dir(ai_tool: str = "copilot-cli") -> Path:
    """Get the default subagents directory from environment variables or fallback.
    
    Args:
        ai_tool: The AI tool name to get the specific directory for
        
    Returns:
        Path to the subagents directory for the specified AI tool
    """
    # Look for .env file starting from current working directory
    current_dir = Path.cwd()
    env_file = current_dir / '.env'
    
    # Load .env from current working directory if it exists
    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=True)
    
    # Get AI tool specific directory or fallback to general directory
    ai_tool_env_var = f'COPILOT_SUBAGENTS_{ai_tool.upper().replace("-", "_")}_SUBAGENTS_DIR'
    general_env_var = 'COPILOT_SUBAGENTS_SUBAGENTS_DIR'
    
    env_dir = os.getenv(ai_tool_env_var) or os.getenv(general_env_var, '.github/subagents')
    
    # If the path is relative, make it relative to current working directory
    subagents_path = Path(env_dir)
    if not subagents_path.is_absolute():
        subagents_path = current_dir / subagents_path
    
    return subagents_path

def get_yolo_mode() -> bool:
    """Check if YOLO mode is enabled from environment variables."""
    # Look for .env file starting from current working directory
    current_dir = Path.cwd()
    env_file = current_dir / '.env'
    
    # Load .env from current working directory if it exists
    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=True)
    
    yolo_mode = os.getenv('COPILOT_SUBAGENTS_YOLO_MODE', 'false').lower()
    return yolo_mode in ('true', '1', 'yes', 'on')

def get_valid_tools_for_ai_tool(ai_tool: str) -> List[str]:
    """Get the list of valid tools for a given AI tool.
    
    Args:
        ai_tool: The AI tool name (e.g., 'copilot-cli', 'claude-code', etc.)
        
    Returns:
        List of valid tool names
    """
    verifier = get_ai_tool_verifier(ai_tool)
    return verifier.get_valid_tools()

def get_supported_ai_tools() -> List[str]:
    """Get list of supported AI tools."""
    return ['copilot-cli', 'claude-code', 'codex', 'gemini-cli']

class SubagentParser:
    """Parse subagent markdown files with YAML frontmatter."""
    
    def __init__(self, subagents_dir: Optional[Path] = None, ai_tool: str = "copilot-cli"):
        self.ai_tool = ai_tool
        if subagents_dir:
            self.subagents_dir = subagents_dir
        else:
            verifier = get_ai_tool_verifier(ai_tool)
            self.subagents_dir = verifier.get_default_subagents_dir()
    
    def parse_subagent_file(self, subagent_name: str) -> Tuple[Dict, str]:
        """Parse a subagent file and return frontmatter and content.
        
        Args:
            subagent_name: Name of the subagent (without .md extension)
            
        Returns:
            Tuple of (frontmatter_dict, content_string)
            
        Raises:
            FileNotFoundError: If subagent file doesn't exist
            ValueError: If YAML frontmatter is invalid
        """
        subagent_path = self.subagents_dir / f"{subagent_name}.md"
        
        if not subagent_path.exists():
            raise FileNotFoundError(f"Subagent file not found: {subagent_path}")
        
        content = subagent_path.read_text()
        
        # Extract YAML frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
        
        if not frontmatter_match:
            raise ValueError(f"No YAML frontmatter found in {subagent_path}")
        
        frontmatter_yaml = frontmatter_match.group(1)
        content_body = frontmatter_match.group(2)
        
        try:
            frontmatter = yaml.safe_load(frontmatter_yaml)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML frontmatter in {subagent_path}: {e}")
        
        return frontmatter, content_body.strip()
    
    def get_allowed_tools(self, subagent_name: str) -> List[str]:
        """Extract allowed tools from subagent file."""
        frontmatter, _ = self.parse_subagent_file(subagent_name)
        return frontmatter.get('allowed_tools', [])
    
    def get_denied_tools(self, subagent_name: str) -> List[str]:
        """Extract denied tools from subagent file."""
        frontmatter, _ = self.parse_subagent_file(subagent_name)
        return frontmatter.get('deny_tools', [])
    
    def get_subagent_prompt(self, subagent_name: str) -> str:
        """Extract the main content (prompt) from subagent file."""
        _, content = self.parse_subagent_file(subagent_name)
        return content
    
    def parse_file(self, subagent_path: str) -> Dict[str, Any]:
        """Parse a subagent file and return structured data.
        
        Args:
            subagent_path: Path to the subagent file
            
        Returns:
            Dict with structured subagent data
        """
        # Convert path to Path object and get relative name
        path_obj = Path(subagent_path)
        subagent_name = path_obj.stem  # Get filename without extension
        
        frontmatter, content = self.parse_subagent_file(subagent_name)
        
        # Structure the data as expected by ToolVerifier
        return {
            'name': frontmatter.get('name', subagent_name),
            'description': frontmatter.get('description', ''),
            'version': frontmatter.get('version', '1.0.0'),
            'model': frontmatter.get('model', ''),  # Optional model specification
            'tools': {
                'allowed': frontmatter.get('allowed_tools', []),
                'denied': frontmatter.get('deny_tools', [])
            },
            'prompt': content
        }
    
    def list_subagents(self) -> List[str]:
        """List all available subagent files."""
        if not self.subagents_dir.exists():
            return []
        
        subagents = []
        for file_path in self.subagents_dir.glob("*.md"):
            if file_path.name != "README.md":
                subagents.append(file_path.stem)
        
        return sorted(subagents)

class ToolVerifier:
    """Verifies if tools are allowed or denied based on configuration."""
    
    def __init__(self, ai_tool: str = "copilot-cli"):
        """Initialize ToolVerifier with AI tool configuration.
        
        Args:
            ai_tool: The AI tool to use (default: copilot-cli)
        """
        self.ai_tool = ai_tool
        self.ai_verifier = get_ai_tool_verifier(ai_tool)
    
    def verify_allowed_tools(self, subagent_path: str) -> Dict[str, Any]:
        """Verify that only allowed tools are specified in the subagent.
        
        Args:
            subagent_path: Path to the subagent file
            
        Returns:
            Dict with verification results
        """
        parser = SubagentParser(ai_tool=self.ai_tool)
        subagent = parser.parse_file(subagent_path)
        
        if not subagent['tools']['allowed']:
            return {
                'success': True,
                'message': 'No allowed tools specified',
                'invalid_tools': [],
                'valid_tools': [],
                'cli_flags': ''
            }
        
        valid_tools = self.ai_verifier.get_valid_tools()
        allowed_tools = subagent['tools']['allowed']
        
        # Check which tools are invalid
        invalid_tools = [tool for tool in allowed_tools if tool not in valid_tools]
        valid_allowed_tools = [tool for tool in allowed_tools if tool in valid_tools]
        
        success = len(invalid_tools) == 0
        
        # Generate CLI flags for valid tools
        cli_flags = ""
        if valid_allowed_tools:
            cli_flags = self.ai_verifier.format_tools(valid_allowed_tools, "allow")
        
        return {
            'success': success,
            'message': 'All tools are valid' if success else f'Invalid tools found: {", ".join(invalid_tools)}',
            'invalid_tools': invalid_tools,
            'valid_tools': valid_allowed_tools,
            'cli_flags': cli_flags
        }
    
    def verify_denied_tools(self, subagent_path: str) -> Dict[str, Any]:
        """Verify that denied tools are valid tool names.
        
        Args:
            subagent_path: Path to the subagent file
            
        Returns:
            Dict with verification results
        """
        parser = SubagentParser(ai_tool=self.ai_tool)
        subagent = parser.parse_file(subagent_path)
        
        if not subagent['tools']['denied']:
            return {
                'success': True,
                'message': 'No denied tools specified',
                'invalid_tools': [],
                'valid_tools': [],
                'cli_flags': ''
            }
        
        valid_tools = self.ai_verifier.get_valid_tools()
        denied_tools = subagent['tools']['denied']
        
        # Check which tools are invalid
        invalid_tools = [tool for tool in denied_tools if tool not in valid_tools]
        valid_denied_tools = [tool for tool in denied_tools if tool in valid_tools]
        
        success = len(invalid_tools) == 0
        
        # Generate CLI flags for valid tools
        cli_flags = ""
        if valid_denied_tools:
            cli_flags = self.ai_verifier.format_tools(valid_denied_tools, "deny")
        
        return {
            'success': success,
            'message': 'All tools are valid' if success else f'Invalid tools found: {", ".join(invalid_tools)}',
            'invalid_tools': invalid_tools,
            'valid_tools': valid_denied_tools,
            'cli_flags': cli_flags
        }
    
    # Backward compatibility methods for tests
    def verify_tools(self, tools: List[str]) -> Tuple[List[str], List[str]]:
        """Verify tools and return valid and invalid lists.
        
        Args:
            tools: List of tools to verify
            
        Returns:
            Tuple of (valid_tools, invalid_tools)
        """
        valid_tools = self.ai_verifier.get_valid_tools()
        valid = [tool for tool in tools if tool in valid_tools]
        invalid = [tool for tool in tools if tool not in valid_tools]
        return valid, invalid
    
    def add_valid_tool(self, tool: str) -> None:
        """Add a valid tool (for backward compatibility - not implemented)."""
        # This is a placeholder for backward compatibility with tests
        # In the new architecture, tools are defined in the AI verifier classes
        pass
    
    def remove_valid_tool(self, tool: str) -> None:
        """Remove a valid tool (for backward compatibility - not implemented)."""
        # This is a placeholder for backward compatibility with tests
        # In the new architecture, tools are defined in the AI verifier classes
        pass

# Base class for AI tool specific verifiers
class BaseAIToolVerifier:
    """Base class for AI tool specific verifiers."""
    
    def __init__(self):
        self.ai_tool_name = "base"
    
    def get_valid_tools(self) -> List[str]:
        """Get the list of valid tools for this AI tool."""
        raise NotImplementedError("Subclasses must implement get_valid_tools")
    
    def format_tools(self, tools: List[str], flag_type: str) -> str:
        """Format tools as CLI flags for this AI tool.
        
        Args:
            tools: List of tool names
            flag_type: Either 'allow' or 'deny'
            
        Returns:
            Formatted string with CLI flags
        """
        raise NotImplementedError("Subclasses must implement format_tools")
    
    def supports_yolo_mode(self) -> bool:
        """Check if this AI tool supports YOLO mode."""
        return False
    
    def format_model(self, model: str) -> str:
        """Format model as CLI flags for this AI tool.
        
        Args:
            model: Model name (e.g., 'gpt-4', 'gpt-3.5-turbo', etc.)
            
        Returns:
            Formatted string with model CLI flags, empty string if no model
        """
        raise NotImplementedError("Subclasses must implement format_model")
    
    def get_default_subagents_dir(self) -> Path:
        """Get the default subagents directory for this AI tool."""
        return get_default_subagents_dir(self.ai_tool_name)

class CopilotCLIVerifier(BaseAIToolVerifier):
    """Tool verifier for GitHub Copilot CLI."""
    
    def __init__(self):
        super().__init__()
        self.ai_tool_name = "copilot-cli"
    
    def get_valid_tools(self) -> List[str]:
        """Get the list of valid tools for Copilot CLI."""
        return [
            "write",
            "shell(*)",
            "shell(git)"
        ]
    
    def format_tools(self, tools: List[str], flag_type: str) -> str:
        """Format tools as copilot CLI flags.
        
        Args:
            tools: List of tool names
            flag_type: Either 'allow' or 'deny'
            
        Returns:
            Formatted string with CLI flags
        """
        if not tools:
            return ""
        
        # Handle YOLO mode for allowed tools
        if flag_type == "allow" and get_yolo_mode():
            return "--allow-all-tools"
        
        flag = "--allow-tool" if flag_type == "allow" else "--deny-tool"
        return " ".join([f'{flag} {tool}' for tool in tools])
    
    def supports_yolo_mode(self) -> bool:
        """Copilot CLI supports YOLO mode with --allow-all-tools."""
        return True
    
    def get_default_subagents_dir(self) -> Path:
        """Get the default subagents directory for Copilot CLI."""
        # First try Copilot-specific directory, then fall back to general
        current_dir = Path.cwd()
        env_file = current_dir / '.env'
        
        # Load .env from current working directory if it exists
        if env_file.exists():
            load_dotenv(dotenv_path=env_file, override=True)
        
        # Try Copilot-specific environment variable first
        copilot_dir = os.getenv('COPILOT_SUBAGENTS_COPILOT_CLI_SUBAGENTS_DIR')
        if copilot_dir:
            subagents_path = Path(copilot_dir)
            if not subagents_path.is_absolute():
                subagents_path = current_dir / subagents_path
            return subagents_path
        
        # Fall back to general directory with copilot-cli subdirectory
        general_dir = os.getenv('COPILOT_SUBAGENTS_SUBAGENTS_DIR', '.github/subagents')
        subagents_path = Path(general_dir) / 'copilot-cli'
        if not subagents_path.is_absolute():
            subagents_path = current_dir / subagents_path
        
        return subagents_path
    
    def format_model(self, model: str) -> str:
        """Format model as CLI flags for Copilot CLI.
        
        Args:
            model: Model name (e.g., 'gpt-4', 'gpt-3.5-turbo', etc.)
            
        Returns:
            Formatted string with model CLI flags, empty string if no model
        """
        if not model or not model.strip():
            return ""
        
        return f"--model {model.strip()}"

# Factory function to get the appropriate verifier
def get_ai_tool_verifier(ai_tool: str) -> BaseAIToolVerifier:
    """Get the appropriate AI tool verifier.
    
    Args:
        ai_tool: The AI tool name
        
    Returns:
        BaseAIToolVerifier: The appropriate verifier instance
    """
    verifiers = {
        'copilot-cli': CopilotCLIVerifier,
    }
    
    verifier_class = verifiers.get(ai_tool)
    if verifier_class:
        return verifier_class()
    else:
        # Default to copilot-cli for unknown tools
        return CopilotCLIVerifier()

def format_copilot_tools(tools: List[str], flag_type: str) -> str:
    """Format tools as copilot CLI flags (legacy function).
    
    Args:
        tools: List of tool names
        flag_type: Either 'allow' or 'deny'
        
    Returns:
        Formatted string with CLI flags
    """
    if not tools:
        return ""
    
    flag = "--allow-tool" if flag_type == "allow" else "--deny-tool"
    return " ".join([f'{flag} {tool}' for tool in tools])
