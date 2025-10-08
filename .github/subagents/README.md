# Subagents Directory

This directory contains specialized AI subagents for the Aurora system.

## Structure
- `*.md` - Individual subagent definitions
- `state/` - Execution plans and state management. Not added to the git commit history. It is a temporary file.

## Usage
1. **Create**: Use `create-subagent` prompt to generate new subagents
2. **List**: Use `list-subagents` prompt to see all available subagents  
3. **Plan**: Use `plan-with-subagents` prompt to create execution plans
4. **Execute**: Use `invoke-with-subagents` prompt to run planned tasks

## Subagent Format
Each subagent follows this structure:
```markdown
---
name: "subagent-name"
description: "Brief description"
version: "1.0.0"
created: "2025-10-08"
allowed_tools: ["tool1", "tool2"]
tags: ["category1", "category2"]
---
System prompt defining the subagent's role and capabilities.

## Response
Optional response format specification.
```

## Getting Started
Try creating your first subagent:
```
Create a subagent for code review that analyzes TypeScript files
```
