# copilot-subagents
A preamble to the use of subagents in github copilot for vscode. This project shows how to leverage prompts and the [Github Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli) to build agentic ai assistants that run in their own terminal and environments.

```
NOTE:
- This work explores the use of Github Copilot CLI( currently in preview)
- It is my hope this inspires `copilot subagents` as a CLI feature
- This work can easily be adapted for use with ClaudeCode CLI, Gemini CLI, etc.
```

## Sub-agents - Learning from the giants
This work is based on my experience using [Claude code sub-agents](https://docs.claude.com/en/docs/claude-code/sub-agents).

### Why sub-agents?
This follows a similar expectation as that in [Claude code sub-agents](https://docs.claude.com/en/docs/claude-code/sub-agents).

| | Comments |
|---------|-------------|
| 🤖 Specialized & Reusable Agents | Enable specialized, expert agents that can be orchestrated together |
| 🤝 Agentic Collaboration | Allows multiple specialized agents to work collaboratively on complex tasks |
| 🧠 Context Management by separate context window | Improves token management as the main agents chat is not overwhelmed. |
| 🎯 Focused Execution | Improved Focus of capabilities like Tool-use selection, etc |
| ⚡ Parallelize task execution | Enables the potential for concurrent execution of multiple tasks and perhaps contained environments of execution. |

### How does this work here?

I wanted to show how using just what's available in Github Copilot for VsCode we could build a subagents system without writing any code. Github Copilot, with Anthropics Claude or Grok Code Fast 1 or GPT5 offer a great way to implement scripts as only markdown, where the LLM agent can call a set of commands and execute a sequence of tasks or even loops if required. 

#### The Basic subagent flow

Use command line tools + github copilots awesome 'workflow' following capabilities.

1. Create your subagents 🤖 ... 🤖 
  
- Use [.github/prompts/create-subagent.prompt.md] to create specialized defined as single '.md' files in [.github/subagents/<agent-name>.md]

2. Plan your task using your subagents as commands 📝 i.e. `copilot -p` where each call is a subagent
- Use [.github/prompts/plan-with-subagents.prompt.md] to create a [.github/subagents/state/plan.md] using each of the available agents in [.github/subagents/<agent-name>.md]

3. Execute your plan 🚀
- Use [.github/prompts/invoke-with-subagents.prompt.md] to execute the [.github/subagents/state/plan.md]

4. Your main agent acts as a manager that can re-execute failed tasks.

```
NOTE: we've implemented a simple command line called 'subagents' that abstracts the calling of copilot -p CLI and adds in validation for tools, and provide list agents functionality. This has improved the reliability of calling agents, since there is no fuzziness between 'defining a subagent' and 'calling a subagent'.
```


### Limitations & Suggestions

Here are some 💡 ideas, limitations and suggestions that i feel could be beneficial when considering how to build a better agents system for Github Copilot CLI.

| Limitations | Comments | Suggestion |
|-------|--------|------------|
| 'copilot' CLI has no way to prompt user for permission | This leads to error when performing elevated privileged tasks | Add a prompt or elicit interface similar to MCP elicit and provide rather a --yolo mode to opt out |
| Agent system prompt must be manually injected | Use of 'copilot -p' CLI enables creating custom agents but having to reference the prompt inline instead of having a specialized command | Adding a 'copilot agents -p' command so that the main copilot agent chooses the appropriate agent or relies on 'copilot agents -n coder.agent.md -p' to call a specific agent |
| Hardcoding copilot-instructions.md | Difficult to add context markdown files like AGENTS.md or other special cases except by hardcoding in prompts | Leverage the .github directory or a configuration for setting the instructions or important files |
| Lack of hooks to trigger subagents on certain lifecycle events | Agents can only be executed as part of plan from main github copilot assistant | Add a configuration to trigger hooks based on 'pre-commit' style triggers |
| Main agent only gets feedback based on terminal execution | The main agent should show progress feedback from subagents running | Use of either a new 'context' / chat history per subagent accessible from main agent or at least continue use of central file like the plan.md |
| Fuzzy matching allowed tools / deny-tool | Currently the tools are fuzzy matched by the ai which allows flexibility between different ai CLI but means that there will be possiblity of not allowing/denying the correct tool | Implement a concrete list of tools per client that can be referenced and an set of utilities for verifying tools when agent is created or at runtime |

## 📢 Contribution and Participation

We're excited to explore this discussion further. Ultimately, let's contribute ideas back the copilot cli and other AI client CLI's like claude code and gemini.
I've shared my thoughts here for interest as i've long wanted github copilot to add support for a CLI and for agents expecially.

## Common Issues

1. **Permission denied and could not request permission from user**
   This is likely due to subagent not having permissions in the directory it is executing.
   ✅ (Resolved) - Typically, you need to add the --add-dir and an --allow-tool for that command.

2. **Plan incorrectly uses gh copilot instead of copilot**
   The plan prompt previously asked to use copilot CLI uses the github CLI instead of the new copilot CLI.
   ✅ (Resolved) - By updating the prompts with the correct copilot CLI usage.

3. **Brittle execution and failures on tools and permissions**
   Copilot-cli has complexity due to the cli not having a tool to prompt user for 'permissions' leading to failures on task.
   ✅ (Resolved) - Implementing of subagents cli to help validate tools and invoke agents. Additionally, setting the copilot main agent as a 'manager' which would resolve any issues after the agent is complete. The advantage of running in terminal being the copilot main agent can see what failed and resolve this.




