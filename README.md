# Learn AI coding

## Agent harness

### Chat, autocomplete and agents

Not every AI coding tool does the same job. "Agents" became a wild buzzword over the last year, and non-technical people use the term incorrectly all the time. I think of AI-use in three buckets:

- **Chat** explains ideas and answers questions. Whether it happens in a browser, in your editor, or on Boot.dev with Boots, it's still just a conversation with an LLM.
- **Autocomplete** suggests the rest of the line or code block when you're writing code. This one is very editor-specific. It's about ergonomics and UX more than anything. Functionally, it's when you start typing a function name and your editor suggests the rest, allowing you to press tab to accept.
- **Agents** are where the biggest boost in productivity has been. You interact with them conversationally, but on each turn of the conversation they can run commands on your machine, read and write files, run tests, and use tools to gather information. Agents handle an entire coding workflow.

### Installing OpenCode

[OpenCode](https://opencode.ai/) is an open-source AI coding agent. It can read your repository, edit files, run commands, and use your local dev tooling to validate its own work.

- **Terminal-first**: Everyone on the team can use it no matter which editor they prefer.
- **Open-source**: It has a big community contributing to it, and you can see for yourself how it works under the hood.
- **Provider-agnostic**: It isn't tied to one AI provider (like Anthropic or OpenAI), so you can choose your favorite.
- **Optimized for UX**: The team isn't trying to sell models, so all their energy goes into improving the agent itself.

#### Sloperator

In this course, we'll be working on "Sloperator," an interpreter for the SlopLang programming language. You'll use OpenCode to help you build Sloperator and learn about effective agentic AI usage. Sloperator is written in Python, but runs .slop files, which are text files containing SlopLang code.

```sh
# install OpenCode
curl -fsSL https://opencode.ai/v2/install | bash
# install uv
curl -fsSL https://docs.astral.sh/uv/install.sh | bash
# check versions
opencode --version
uv --version
# starter code
cd starter
uv sync
opencode
```

### OpenCode console

[OpenCode Console](https://opencode.ai/console/) is a suite of hosted services offered by the same team that develops the OpenCode agent. The console gives you access to a large catalog of AI coding models, some of which are free, which means you can complete this course _without paying anything_.

#### Commands

- Using the **/connect** command inside an OpenCode session connects to a provider like OpenCode Console or ChatGPT:
- The **/models** command opens the model selector, so you can search for a model and switch to it.

#### Gui clients

```sh
opencode pair
```

## Models and providers

### Providers and models

- A **provider** is the service OpenCode uses a model through, like OpenAI, Anthropic, Google, or OpenCode Go.
- A **model** is the specific LLM you use through that provider, like gpt-5, claude-sonnet-4-5, gemini-3.1-pro, or deepseek-v4.1-flash-free.

### Model costs

| Developer Model Input Cost (1M Tokens) | Output Cost (1M Tokens) |
| -------------------------------------- | ----------------------- |
| OpenAI gpt-6-astra                     | $10.00	$50.00            |
| OpenAI gpt-5.6-sol                     | $4.00	$20.00             |
| Anthropic claude-fable-5-1             | $10.00	$50.00            |
| Anthropic claude-opus-5-5              | $4.00	$20.00             |
| Google gemini-4-argon                  | $2.00	$10.00             |

### Open-weight models

This isn't a course on LLM architecture, but at a high level the process looks like this:

- Gather a massive dataset – Reddit posts, GitHub repos, tweets, Wikipedia articles, etc.
- Run that text through a training process that adjusts the model's internal parameters, its "weights," to reduce prediction error.
- The end result is a giant file full of numbers that encode the patterns the model learned during training.

### Self hosting models

In OpenCode, local/self-hosted usage is often done via:

- LM Studio
- Ollama
- llama.cpp / llama-server

### Pay per token

| Model                    | Model ID                   | Input (per 1M) | Output (per 1M) |
| ------------------------ | -------------------------- | -------------: | --------------: |
| DeepSeek V4.1 Flash Free | `deepseek-v4.1-flash-free` |           Free |            Free |
| GPT 5.6                  | `sol gpt-5.6-sol`          |          $4.00 |          $20.00 |
| Claude Opus 5            | `claude-opus-5`            |          $5.00 |          $25.00 |
| Claude Fable 5.1         | `claude-fable-5-1`         |         $10.00 |          $50.00 |

## Tools

### What is a tool

A tool is essentially a function the model is allowed to call. For example, OpenCode comes with a read tool that lets the model read files.
The agent harness tells the model which tools are available, what each one does, and what arguments each accepts.

### Built-in tools

OpenCode has some built-in tools that you don't need to install yourself. The most important ones for day-to-day coding are:

- _read_, glob, and grep for gathering context
- _edit_, write, and patch for changing files
- _shell_ for running commands
- _webfetch_ and websearch for fetching pages and searching online
- _question_ for asking you clarifying questions (which displays a custom selector UI)
- _skill_ for loading reusable SKILL.md files (we'll cover these later)

### Custom tools

Custom tools are useful for specialized actions the agent performs repeatedly:

- Querying an internal database safely
- Calling a project-specific API
- Wrapping a complicated script behind a simpler interface
- Looking up metadata from a system the repo depends on

### Create custom tool

```sh
cd .opencode
bun add @opencode/plugin@2.0.3
touch .opencode/plugins/database.ts
```

```ts
import { Plugin } from "@opencode/plugin";

export default Plugin.define({
  id: "applymaxxing.database-tool",
  setup: async (ctx) => {
    await ctx.tool.transform((tools) => {
      tools.add({
        name: "database",
        description: "Query the project database",
        input: {
          type: "object",
          properties: {
            query: { type: "string" },
          },
          required: ["query"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input) => {
          const { query } = input as { query: string };
          return { content: `Executed query: ${query}` };
        },
      });
    });
  },
});
```

### Tool permissions

OpenCode lets you decide whether a tool action should run automatically, ask first, or simply be denied using the permissions array in opencode.jsonc:

```ts
{
  "$schema": "https://opencode.ai/config.json",
  "permissions": [
    { "action": "shell", "resource": "*", "effect": "ask" },
    { "action": "edit", "resource": "*", "effect": "allow" },
    { "action": "webfetch", "resource": "*", "effect": "deny" },
  ],
}
```

h rule's effect is one of:

- allow: run without approval
- ask: prompt before running
- deny: block the action

## Promptiung

### Good prompt

- Be specific (you need strong technical skills to be able to do this)
- Define constraints
- Add meaningful context
- Describe edge cases
- Provide validation instructions

### Plan agent

- Build (default): The agent can take action on the codebase: edit files, run commands, use tools.
- Plan: The agent can inspect the project, run shell commands, ask questions, and plan changes. OpenCode blocks its edit, write, and patch tool calls from modifying project files – except for dedicated plan files.

### Cancelling

If you can't find an API endpoint that matches the functionality we need, pause and ask me what to do next.

### Steering

A steering message gets picked up at the next step boundary (usually as soon as the tool calls it's running finish). The agent then keeps going on the same task with your new information in context.

### Prompt box

Some default TUI shortcuts include:

- Enter sends the prompt. While the agent is working, it sends a steering message.
- Shift+Enter adds a newline. If your terminal doesn't support that combination, try Ctrl+J.
- Up recalls an earlier prompt when the cursor is at the start of the input. Down moves forward through prompt history when the cursor is at the end.
- Ctrl+C clears the input field or, if the input is already clear, exits OpenCode.
- Ctrl+X, then E, opens your prompt in your external editor (VISUAL, or EDITOR if VISUAL isn't set). Save and close the editor; OpenCode reads the draft back when the editor process exits. GUI editors need a wait flag, such as code --wait.

### Queueing

To queue a prompt, type it in, then press Ctrl+X before Enter to send it. The agent will finish its entire current task, then pick up the queued prompt and start working on that.

- Steer: changes the work in flight (default)
- Queue: waits until the current work is done, then sends the next prompt (Ctrl+X before Enter)

### Prompt examples

Prompting isn't a dark art. I'd take a technical domain expert who understands their customer over someone with a "Prompting for Dummies" cheatsheet any day.

It's easy to learn to write better prompts. It's hard to learn to code and understand your customers' needs. That said, there are some basic rules to be aware of. Some providers even have guides on writing better prompts:

### Speech to text

You don't need to polish a spoken prompt as you would a PR description meant for a human. Agents have no problem understanding messy wording and corrections like "Um, actually, forget that, do this other thing," but what helps is the extra context you provide, not the additional words themselves.

## Agents

### Agent

Agents in OpenCode are configurable AI assistants with their own prompts, models, and permissions.

OpenCode ships with two built-in primary agents, "Build" and "Plan", but you can also create your own with custom tools, model settings, instructions, etc.

### Temperature

Lower temperature (closer to 0.0) means:
- More focused responses
- Less randomness

Higher temperature (closer to 1.0) means:
- More variety and "creativity" (scare quotes intended)
- Less control over the output

### Custom Agents

A custom agent can be defined easily with a Markdown file. And OpenCode watches for changes in its config directories, so if you update an agent's settings, it will normally reload without a restart.

Put the file in one of these locations:

- *.opencode/agents/* for a project-specific agent
- *~/.config/opencode/agents/* for a global agent

### Max Steps

Sometimes you know a task really just shouldn't take that long.

You can limit your agent's ability to spin its wheels with the steps setting. Each step is one model response, which can include multiple tool calls. The results of those calls feed into the next step.

### Subagents

Subagents are specialized agents that your primary agent can spin off concurrently to tackle narrower jobs. OpenCode ships with two built-in subagents:

- general: a general-purpose worker that can research and execute multi-step tasks
- explore: a fast, read-only worker for codebase and web exploration

### Task Permissions

Just because a subagent exists doesn't mean every agent should be allowed to invoke it.
You can control that with subagent permission rules.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agents": {
    "orchestrator": {
      "mode": "primary",
      "permissions": [
        { "action": "subagent", "resource": "*", "effect": "deny" },
        {
          "action": "subagent",
          "resource": "orchestrator-*",
          "effect": "allow",
        },
        { "action": "subagent", "resource": "code-reviewer", "effect": "ask" },
      ],
    },
  },
}
```

## Context

### What is context

Context is all the information your AI model can "see" when it's generating a response. A "context window" is the limit on how much of that information the model can work with at once.

### Context as RAM

The "Context" section in OpenCode's right-hand sidebar shows your current context usage in tokens and as a percentage of your model's maximum.

### New sessions

The */new* command in OpenCode starts a fresh conversation without carrying over the previous session's history. Project instructions still apply, and your files stay as they are.

Don't worry, you can use the */sessions* command to jump back and resume any previous session at any time. Or use the tabs along the top of the TUI.

### Token economics

- More tokens mean more cost. And larger context = more input tokens.
- Each time you send a message, the LLM has to reprocess the entire conversation
- Not every session you start needs to have the entirety of your codebase, docs, and session history in context
