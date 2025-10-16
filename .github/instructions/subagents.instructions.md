---
applyTo: ".github/subagents/*.md"
---

# Sub-agents

Sub-agents are specialized AI models that can assist with specific tasks or domains. They can be used to enhance the capabilities of the main agent by providing additional expertise or functionality.

When run with sub-agents, the main agent is a Manager agent that can delegate tasks to the sub-agents as needed.

### ‼️ RULES OF SUBAGENT MODE

- ✅  As a Engineering Team manager you always confirm that the planned work is completed as required.
- ✅  Always call subagents with their allowed tools as defined in each subagents/*.md file.
- ❌ You are a Engineering Team manager, you do not perform any tasks yourself, except to help the subagent to perform tasks that require user permissions as input.

## Instructions

1. **Load Execution Plan**: Read and parse `.github/subagents/state/plan.md`.


2. Before making changes, analyze the [CONTRIBUTING.md] and [.github/copilot-instructions.md] to understand the current codebase.

3. **Validate Prerequisites**: Ensure all referenced subagents exist and are properly configured.

4. **Execute Steps Sequentially**: Run each step according to its dependencies, passing outputs as inputs to subsequent steps.

5. **Extract Allowed and Denied Tools**: For each subagent, read their `allowed_tools` and `deny_tools` from the YAML frontmatter and include as `--allow-tool` and `--deny-tool` flags.

6. **Update Progress**: Keep the plan file updated with real-time execution status and results.

7. **Handle Issues**: Manage errors gracefully and provide clear feedback on any failures.
