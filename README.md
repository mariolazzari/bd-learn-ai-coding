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
