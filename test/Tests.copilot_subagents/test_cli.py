"""Tests for the main CLI functionality."""

import pytest
from click.testing import CliRunner
from pathlib import Path
import tempfile
import os

# Import from the source directory
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "copilot_subagents" / "src"))

from cli import cli

def test_main_command():
    """Test the main command group."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert "Copilot Subagents" in result.output

def test_info_command():
    """Test the info command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['info'])
    assert result.exit_code == 0
    assert "Copilot Subagents CLI" in result.output
    assert "Available Commands" in result.output

def test_version_option():
    """Test version option."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert "0.1.0" in result.output

class TestWithTempSubagents:
    """Tests that require temporary subagent files."""
    
    def setup_method(self):
        """Set up temporary directory with test subagent files."""
        self.temp_dir = tempfile.mkdtemp()
        self.subagents_dir = Path(self.temp_dir) / "subagents"
        self.subagents_dir.mkdir()
        
        # Create a test subagent file
        test_subagent = self.subagents_dir / "test-agent.md"
        test_subagent.write_text("""---
name: "test-agent"
description: "A test subagent"
version: "1.0.0"
allowed_tools: ["write", "shell(*)"]
deny_tools: ["shell(git)"]
---

You are a test subagent for unit testing.
""")
    
    def teardown_method(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_verify_allowed_tools_success(self):
        """Test verify_allowed_tools with valid tools."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            'verify-allowed-tools', 
            'test-agent',
            '--subagents-dir', str(self.subagents_dir)
        ])
        assert result.exit_code == 0
        assert "Verification Passed" in result.output
    
    def test_verify_denied_tools_success(self):
        """Test verify_denied_tools with valid tools.""" 
        runner = CliRunner()
        result = runner.invoke(cli, [
            'verify-denied-tools',
            'test-agent', 
            '--subagents-dir', str(self.subagents_dir)
        ])
        assert result.exit_code == 0
        assert "Verification Passed" in result.output
    
    def test_verify_nonexistent_subagent(self):
        """Test verification of non-existent subagent."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            'verify-allowed-tools',
            'nonexistent-agent',
            '--subagents-dir', str(self.subagents_dir)
        ])
        assert result.exit_code == 1
        assert "not found" in result.output
    
    def test_invoke_list_subagents(self):
        """Test listing subagents."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            'list',
            '--subagents-dir', str(self.subagents_dir)
        ])
        assert result.exit_code == 0
        assert "test-agent" in result.output
    
    def test_invoke_missing_prompt(self):
        """Test invoke command without prompt."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            'invoke',
            'test-agent',
            '--subagents-dir', str(self.subagents_dir)
        ])
        assert result.exit_code == 1
        assert "--prompt is required" in result.output
    
    def test_invoke_dry_run(self):
        """Test invoke command in dry run mode."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            'invoke',
            'test-agent',
            '--prompt', 'Test prompt',
            '--dry-run',
            '--subagents-dir', str(self.subagents_dir)
        ])
        assert result.exit_code == 0
        assert "Dry run mode" in result.output
        assert "copilot" in result.output