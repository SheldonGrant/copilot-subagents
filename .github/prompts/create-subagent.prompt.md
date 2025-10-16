# Create Subagent Workflow

A structured 4-step workflow for creating new subagent definitions in the `.github/subagents/` directory.

## Purpose
Generate a specialized subagent definition file that can be used by the GitHub Copilot CLI for task-specific execution with proper tool verification.

## Workflow Steps

### Step 1: Check Available Subagents
**Objective**: Verify if a similar subagent already exists to avoid duplication.

**Action**: Run the following command to list all existing subagents:
```bash
uv run subagents list
```

**Analysis**: 
- Review the output to see existing subagents and their descriptions
- Confirm that no existing subagent already covers the requested functionality
- If a similar subagent exists, consider if it should be enhanced instead of creating a new one

### Step 2: Check Available Tools for Copilot CLI
**Objective**: Understand what tools are available for the subagent to use.

**Action**: Run the following command to see all valid tools:
```bash
uv run subagents show-tools copilot-cli
```

**Analysis**:
- Review the list of available tools: `write`, `shell(*)`, `shell(git)`
- Plan which tools the new subagent will need based on its intended functionality
- Consider security implications of tool choices

### Step 3: Follow Subagent Creation Guidelines
**Objective**: Design the subagent according to best practices and security requirements.

**Planning**:

- **Name**: Use kebab-case (e.g., "code-reviewer", "data-analyzer")
- **Description**: Keep under 100 characters, be specific about the domain
- **Model**: Optional field for specific model requirements (e.g., "gpt-4", "gpt-3.5-turbo")
- **Allowed Tools**: Choose from available copilot-cli tools: `write`, `shell(*)`, `shell(git)`
- **Deny Tools**: Optional section to explicitly deny certain tools for security
- **Tags**: Use relevant categories (e.g., "development", "analysis", "automation")
- **System Prompt**: Write 2-4 paragraphs defining the subagent's role and behavior
- **Response Format**: Optional but recommended for structured outputs

**Security Considerations**:
- Carefully consider if `shell(*)` access is necessary
- Use `shell(git)` only if git operations are required
- Default to minimal tool permissions following principle of least privilege

### Step 4: Create the Subagent Markdown File
**Objective**: Generate the actual subagent definition file.

**Action**: Create a new file `.github/subagents/[subagent-name].md` with the following structure:

```markdown
---
name: "[subagent-name]"
description: "[Brief description of what this subagent does]"
version: "1.0.0"
created: "2025-10-15"
model: "[optional-model-name]"  # e.g., "gpt-4" or remove if not needed
allowed_tools: 
  - "[tool1]"  # Choose from: write, shell(*), shell(git)
  - "[tool2]"
deny_tools:      # Optional section
  - "[tool3]"   # Tools to explicitly deny
tags: ["tag1", "tag2"]
---
[Your subagent's core system prompt goes here]. This should be 2-4 paragraphs
that clearly define the subagent's role, capabilities, and approach to solving problems.

Include specific instructions, best practices, and any constraints
the subagent should follow when completing tasks.

## Guidelines
[Optional section with specific operational guidelines]

## Response Format
[Optional section defining expected output structure]
```

**File Creation Guidelines**:
- Ensure the file is saved in `.github/subagents/` directory
- Use `.md` extension for the filename
- Validate YAML frontmatter syntax
- Test the subagent using `uv run subagents invoke [subagent-name] --prompt "test" --dry-run`

## Workflow Validation Checklist

After completing all steps, verify:
- [ ] **Step 1 Complete**: Confirmed no duplicate subagent exists
- [ ] **Step 2 Complete**: Reviewed available copilot-cli tools
- [ ] **Step 3 Complete**: Planned subagent following guidelines
- [ ] **Step 4 Complete**: Created `.github/subagents/[name].md` file
- [ ] **File Validation**: YAML frontmatter properly formatted
- [ ] **Tool Validation**: Only uses valid copilot-cli tools (`write`, `shell(*)`, `shell(git)`)
- [ ] **Security Review**: Appropriate tool permissions assigned
- [ ] **Functionality Test**: Tested with dry-run command

## Example Usage
**User Request**: "Create a subagent for code review that can analyze TypeScript files for best practices, security issues, and performance optimizations."

**Expected Output**: 
```markdown
---
name: "typescript-code-reviewer"
description: "Reviews TypeScript code for best practices, security issues, and performance optimizations"
version: "1.0.0"
created: "2025-10-08"
allowed_tools: 
  - "file_read"
  - "code_analysis"
  - "security_scan"
  - "performance_check"
deny_tools:
  - "shell(git push)"
  - "shell(git branch)"
tags: ["development", "code-review", "typescript", "security"]
---
You are a specialized TypeScript code reviewer focused on ensuring high-quality, secure, 
and performant code. Your primary responsibility is to analyze TypeScript files and 
provide comprehensive feedback on code quality, security vulnerabilities, and performance 
optimization opportunities.

When reviewing code, you should examine: type safety and proper TypeScript usage, 
adherence to coding standards and best practices, potential security vulnerabilities, 
performance bottlenecks and optimization opportunities, maintainability and readability 
concerns, and proper error handling patterns.

Your analysis should be thorough yet practical, focusing on actionable improvements 
that will enhance code quality without introducing unnecessary complexity.

## Response
Provide a structured review with:
- Overall quality score (1-10)
- Critical issues that must be addressed
- Suggested improvements with code examples
- Security concerns and mitigation strategies
- Performance optimization recommendations
- Best practice violations and corrections
```

## Validation Checklist
- [ ] File created in `.github/subagents/` directory
- [ ] YAML frontmatter properly formatted
- [ ] System prompt clearly defines subagent's role
- [ ] Allowed tools are relevant to the subagent's function

- [ ] Deny tools section includes required git restrictions: `shell(git push)` and `shell(git branch)`
- [ ] Tags are appropriate and help with categorization
- [ ] Response format provided (if applicable)
