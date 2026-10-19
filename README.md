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
