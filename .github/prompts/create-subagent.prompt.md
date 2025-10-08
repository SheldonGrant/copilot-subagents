# Create Subagent Prompt

Create a new subagent definition in the `.github/subagents/` directory.

## Purpose
Generate a structured subagent definition file that can be used by the Aurora AI system for specialized task execution.

## Instructions

1. **Analyze the Request**: Understand what type of subagent is needed based on the user's description.

2. **Create Subagent File**: Generate a new markdown file in `.github/subagents/[subagent-name].md` with the following structure:

```markdown
---
name: "[subagent-name]"
description: "[Brief description of what this subagent does]"
version: "1.0.0"
created: "2025-10-08"
allowed_tools: 
  - "tool1"
  - "tool2" 
  - "tool3"
deny_tools:
  - "shell(git push)"
  - "shell(git branch)"
tags: ["tag1", "tag2"]
---
[Your subagent's core system prompt goes here]. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.

Include specific instructions, best practices, and any constraints
the subagent should follow.

## Response
[Your subagent's response structure template goes here. Optionally].
```

3. **Guidelines for Subagent Creation**:
   - **Name**: Use kebab-case (e.g., "code-reviewer", "data-analyzer")
   - **Description**: Keep under 100 characters, be specific about the domain
   - **Allowed Tools**: List specific tools this subagent can use (e.g., "file_read", "web_search", "code_analysis")
   - **Deny Tools**: Optional section to explicitly deny certain tools. Always includes "shell(git push)" and "shell(git branch)" for security
   - **Tags**: Use relevant categories (e.g., "development", "analysis", "automation")
   - **System Prompt**: Write 2-4 paragraphs defining the subagent's role and behavior
   - **Response Format**: Optional but recommended for structured outputs

4. **Security Requirements**:
   - **Always include** `shell(git push)` and `shell(git branch)` in the `deny_tools` section
   - Add any other tools that should be explicitly denied for security or functional reasons
   - The `deny_tools` section is optional but recommended for clarity

5. **Create Directory**: If `.github/subagents/` doesn't exist, create it first.

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
