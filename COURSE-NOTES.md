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

- _.opencode/agents/_ for a project-specific agent
- _~/.config/opencode/agents/_ for a global agent

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
          "effect": "allow"
        },
        { "action": "subagent", "resource": "code-reviewer", "effect": "ask" }
      ]
    }
  }
}
```

## Context

### What is context

Context is all the information your AI model can "see" when it's generating a response. A "context window" is the limit on how much of that information the model can work with at once.

### Context as RAM

The "Context" section in OpenCode's right-hand sidebar shows your current context usage in tokens and as a percentage of your model's maximum.

### New sessions

The _/new_ command in OpenCode starts a fresh conversation without carrying over the previous session's history. Project instructions still apply, and your files stay as they are.

Don't worry, you can use the _/sessions_ command to jump back and resume any previous session at any time. Or use the tabs along the top of the TUI.

### Token economics

- More tokens mean more cost. And larger context = more input tokens.
- Each time you send a message, the LLM has to reprocess the entire conversation
- Not every session you start needs to have the entirety of your codebase, docs, and session history in context

### Ignoring files

OpenCode's content searches use ripgrep, which respects .gitignore patterns by default. This keeps ordinary searches from getting blasted by node_modules/ or dist/ folders. That said, explicit file patterns can override those exclusions, and the agent can still read ignored files directly if needed.

You don't really need anything AI-specific here. Just make sure you actually .gitignore generated files and dependencies like you normally would:

- Build output (dist/, build/, generated assets)
- Dependency trees (node_modules/, .venv/)
- Large logs and temporary dumps
- Binary blobs that won't help code reasoning

### File watcher

OpenCode watches the filesystem for relevant changes, and those events let it reload watched skills and plugins while it's still running.

### Lost in the middle

Having a large context window doesn't mean a model uses every part of it equally well. A famous study called [Lost in the Middle](https://arxiv.org/abs/2307.03172) found that models tend to retrieve information better from the beginning and end of long contexts, rather than from the middle.

### Compaction

If you've never hit a context window limit using a "raw" AI provider's API, know that it's literally a hard stop. You just get an error saying the input is too long.

To avoid this, OpenCode (like other coding agents) will automatically compact your session as you approach the context window limit. In practice, and assuming you're using a model with a reasonably large window, you'll likely never have a "hard stop" because OpenCode's auto-compaction will keep you in safe territory.

you can also trigger it manually at any time with the _/compact_ command

### Configure compaction

- _auto_: whether to compact automatically near context limits. It defaults to true, and usually you want it to stay that way.
- _keep.tokens_: the approximate number of tokens of recent context that OpenCode tries to preserve (in addition to the summary).
- _buffer_: the safety margin, in tokens, below the model's limit; increasing it can trigger compaction earlier.

### Undo & redo

I like to think of my session contexts more as "resources" than "conversations." They're ultimately logs of text, so it's easy to build tools for manipulating them. Just like git makes manipulating code changes super powerful, some agent session management tools can edit session context in ingenious ways.

### Forking

Another powerful context-manipulation command is /fork. It creates a new session with the same context as the current session – while also letting you quickly choose a "fork point" from the recent message history.

Sometimes I want to try a different approach, but I don't want to recreate all the context and history of my current session from scratch. I just fork off the latest message that has the context I actually want, and keep going in the new session.

- Branch to try a risky idea.
- Keep the main session clean.
- Return to the main session if the experiment fails.

### Secrets in context

Anything you put in an OpenCode session can become part of the model's context. That includes pasted text, file contents, and shell output. Copying or exporting the session can spread that information further.

So yes, developer secrets (passwords, API keys, tokens, etc.) can leak into "context" in many ways, not just through committed code.

#### The Good News

OpenCode's default permissions allow read for most files, but .env files ask for your approval by default.
The shell tool runs with your user's host permissions, so treat shell access as real terminal access, not as a filesystem sandbox.

#### The Bad News

Not all secrets are in .env files. You can still leak secrets by:

- Pasting API keys directly into the chat
- Approving a shell command that prints secret values
- Letting logs dump authentication tokens into the terminal
- Allowing OpenCode to run a script that accesses other parts of the filesystem
- Copying or exporting a contaminated session into another system

#### Best Practices

Tune your permissions to deny reads of files you use for secrets, or require explicit approval. For example, this rule in opencode.jsonc blocks the read tool from opening .secrets files:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permissions": [
    { "action": "read", "resource": "*.secrets", "effect": "deny" }
  ]
}
```

## Feedback loops

### Loops

AI agents are not completely useless better when they can get fast, accurate, and automated feedback about their work. A feedback loop is simple:

- Attempt a change
- Run a check
- Inspect the results of the check
- Repeat

### Static typing

Static analysis can immediately tell the model that it:

- Called a function with the wrong arguments
- Returned a value of the wrong type from a function
- Accessed a field that doesn't exist
- Broke an interface contract somewhere downstream

### Automatic formatting

Without a strict formatter, your agent will spend tokens worrying about indentation, trailing commas, and line length. Not only will it waste tokens, but it will also (like any human) be inconsistent.

So, just like when working with humans, always add a code formatter to your workflow and put the problem to rest. For example:

- oxfmt for JavaScript/TypeScript, HTML, CSS, Markdown, and more
- ruff for Python
- gofmt for Go

### Tests

Linters and type checks tell the agent whether the code is structurally valid. Tests tell it whether the code does the right thing. There are two types of tests, generally speaking:

- Unit tests for fast, local correctness checks
- Integration tests for realistic end-to-end behavior

### AI and Test Economics

Writing tests with AI is way cheaper than writing them by hand, which changes the ol' "How many tests are enough tests" debate in an interesting way.

These days, you can be more aggressive about adding targeted tests because the cost of writing them has come down. But "cheap to write" does not mean "generate 1,000 brittle, low-quality tests."

## Skills

### Skill

A "skill" is (mostly) just a reusable prompt for an agent.

Skills are simple, but they're useful enough to deserve serious attention. They sit in the sweet spot between "type the same giant prompt again" and "stuff every possible instruction into AGENTS.md forever."

### Writing Skills

Again, a skill is just a directory with a Markdown file that has YAML frontmatter at the top. Here's an example from the OpenCode maintainers:

- Project-specific skills: .agents/skills/<name>/SKILL.md
- Global (personal) skills: ~/.agents/skills/<name>/SKILL.md

### Skills are tools

Skills aren't just manually invocable Markdown files. OpenCode also exposes them through the native skill tool.

- Skills you and your team write that are hyper-specific to your project and workflow
- Skills that are published alongside a library or API so that users of those products can give their agents instructions for how to use them more effectively.

### Skills permissions

- _allow_: the skill loads immediately
- _ask_: OpenCode asks before loading it
- _deny_: the skill is hidden from the agent and inaccessible to it

### Composable Skills

The best skills are small and narrow enough that they're useful for many different types of tasks.

Try to follow the time-tested Unix philosophy of "do one thing and do it well." If you have a massive skill, consider breaking it up into a few more reusable ones.

- _review_: Reviews the current working directory for any changes, and calls attention to any issues
- _commit_: Stages and commits changes with a conventional commit message, no more than one sentence long
- _sync_: Rebases the current branch onto main, resolves conflicts, and squashes
- _publish_: Pushes to the feature branch and creates a PR for Allan

### Skill, Tool, or Agent?

Skills, tools, and agents all feel like "things that do stuff," which makes it hard to know which is best for a given task that you're trying to automate. Here's how I think about it.

- Is it mostly custom code with defined inputs and outputs? It's a tool.
- Is it a mostly a custom prompt with some optional assets on disk? It's a skill.
- Is it a "mode of operation" that uses tools and skills with a specific set of permissions and settings? It's an agent.

### Custom Commands

Custom commands and skills are very similar.

Both are basically reusable prompt templates. Both help you avoid retyping the same instructions. Both can live at the project level or globally.

But there are a couple of important differences.

- A skill is exposed through OpenCode's native skill tool, meaning it's in context and can be loaded when the agent chooses to.
- A command is primarily a user-invoked TUI shortcut.

### Dynamic Prompts

OpenCode's command pipeline supports a few useful prompt features:

- Positional arguments like $1, $2, and $ARGUMENTS
- Shell output injection like !`bun test`

These are command features. Invoking a skill with @skill-id activates the skill body without parsing command arguments or shell blocks (but it's still valid to invoke a skill and provide additional instructions in the same prompt).

## Model Context Protocol

### MCP

MCP, or Model Context Protocol, is an open standard for systems (usually web APIs, but not necessarily) to expose tools, prompts, and data to AI agents.

That means an MCP server can give your agent access to things like:

- Issue trackers
- External docs
- Databases
- Internal APIs

#### Architecture

There are three main components to an MCP system:

- MCP Host: The AI application that coordinates and manages one or multiple MCP clients
- MCP Client: A component that maintains a connection to an MCP server and obtains context from the server for the MCP host to use
- MCP Server: A program that provides context to MCP clients

### Configure MCP

You configure MCP servers in your OpenCode config:

- Project-level: opencode.jsonc (in the project root)
- Global: ~/.config/opencode/opencode.jsonc

### OAuth

OpenCode supports two forms of authentication:

- API-key-style auth through custom headers
- OAuth flows that OpenCode can kick off and manage

#### CLI Commands

If you're having trouble with authentication, here are a few of the commands that can help you debug:

- opencode mcp list: List all servers and their authorization status.
- opencode mcp auth <name>: Authenticate with an MCP server.
- opencode mcp logout <name>: Remove stored credentials.

### Code Mode

When presented with too many tools, models can struggle with calling the right tool or calling it correctly.

One thing models are trained to do is write code. Code Mode bridges what models do really well, and what MCP does well. It exposes tools through a JavaScript API so the model can execute code to search for tools, call tools, and process the results.

### Context Bloat

MCP servers can be useful, but just like everything in LLMs: tool bloat becomes context bloat.

Once you configure an MCP server, OpenCode has to describe its tools to the model. That catalog eats context whether the model calls a tool or not. Disable servers you're not using.

## Computer Use

### Computer Use

Coding agents are happiest when they can use precise tools. Reading a file is easier with a read tool than by opening an editor and dragging a mouse over the text. Sometimes, though, the graphical user interface (GUI) is the thing that needs to be tested.

Computer use lets a model inspect a screen and operate graphical applications with actions like clicking, typing, scrolling, and switching windows. ChatGPT Computer Use and Claude's computer use build these controls directly into their desktop applications.

OpenCode doesn't currently include a general-purpose desktop controller. That said, it can still operate browsers through external tools, which is where most coding-related computer use happens anyway!

### Browser Automation

Now, a browser is still a graphical application, but it does expose way more structure than your typical native desktop app. It makes sense: web apps are built on structured text! So text-based browser automation tools can easily inspect:

- The document structure
- The accessibility tree
- Console messages
- Network requests
- Page layout measurements

### Accessibility Trees

A screenshot can tell a model what a page looks like, but an accessibility tree tells it what all the controls mean.

Luckily, browsers build the accessibility tree straight from the DOM. It contains semantic information that assistive technology and browser tools can understand:

- Name: Add application
- Role: button
- State: enabled
- Description: Extra context when the name isn't enough

### Vision Models

A vision model can accept image input along with text. Instead of reading a semantic description of a page, it can inspect the screenshot's pixels.

OpenCode supports image attachments and passes image results from tools to models that can accept them. Not every model does, so be sure to check a model's capabilities before you pay for a bunch of tokens or a subscription.

Pixels sometimes expose problems that structured browser data simply can't:

- Awkward spacing
- Clipped or overlapping content
- Broken responsive layouts
- Charts, canvases, and other graphical output
- A page that technically works but looks like a Craigslist ad from 2004

### Playwright MCP

Playwright MCP gives an agent control of a real browser via the Model Context Protocol (MCP). It can navigate pages, inspect accessibility snapshots, fill forms, click controls, and capture screenshots.

### Chrome DevTools MCP

Chrome DevTools MCP can navigate, click, fill forms, inspect semantic page snapshots, and take screenshots. That overlaps with Playwright MCP, to be fair, but Chrome DevTools goes deeper into Chrome itself.

This tool can also inspect:

- Console messages and source-mapped errors
- Network requests and responses
- Lighthouse audits
- Performance traces
- JavaScript memory usage (with the --memory-debugging flag)

## Plugins

### Plugins

Plugins extend OpenCode itself. They run code inside the agent harness, kinda like editor extensions for VS Code or Neovim.

Plugins can do things like:

- Hook into tool execution
- Modify model context before a model call
- Add support for a new authentication flow
- Register new agents, commands, skills, or tools

### Loading Plugins

OpenCode automatically loads .ts and .js plugin files from these directories:

- Project-level: .opencode/plugins/
- Global: ~/.config/opencode/plugins/

Project plugins are for team behavior in a given repo; global plugins (i.e., global to your system user account) are personal.

### Install Plugins

If you want to install someone else's plugin, just add the relevant npm package name to the plugins array in opencode.jsonc:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["opencode-example-plugin", "@my-org/custom-plugin"],
}
```

### Plugin Transforms

Transforms let plugins change the definitions OpenCode uses for tools, agents, models, and other features. For example, a plugin can adjust a tool's description or choose a default agent.

This is useful when you're packaging a customized OpenCode experience for a team. The plugin can inspect existing definitions and apply changes in code.

### Plugin Hooks

Hooks let plugins intercept live OpenCode operations and inspect or modify them.

OpenCode provides a variety of runtime hooks. Here are some examples (not exhaustive):

- ctx.tool.hook("execute.before", callback) runs before a tool executes
- ctx.tool.hook("execute.after", callback) runs after a tool succeeds or fails
- ctx.session.hook("context", callback) modifies the system prompt, messages, or tools before a model call
- ctx.session.hook("http.request", callback) inspects or modifies a provider request
- ctx.session.hook("http.response", callback) inspects or replaces a provider response

### Plugin Tools

OpenCode registers every custom tool through a plugin. A published plugin can bundle tools with commands, skills, agents, or hooks so other developers can install the whole extension at once.

Use a skill or agent when a workflow needs only instructions. Add a tool when it needs code, for example to query an API or database.

### Publishing Plugins

An OpenCode plugin published on npm uses the same default export as a local plugin. So if you want to publish a plugin, you can treat it as a normal ECMAScript module (ESM), with the plugin runtime listed in dependencies:

```json
{
  "name": "my-slop-opencode-plugin",
  "version": "0.1.0",
  "type": "module",
  "exports": "./dist/index.js",
  "dependencies": {
    "@opencode/plugin": "2.0.3"
  }
}
```

## Best practices
