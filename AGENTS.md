# Project instructions

Sloperator is a tree-walking interpreter for **SlopLang**, written in dependency-free
Python 3.13. `uv` manages the environment; dev tooling is `pytest`, `ruff`, and `ty`.
Run everything from the repo root.

## Layout

Pipeline: source → `tokenize` → `parse` → `Interpreter(out).run(...)`.

| Path | Purpose |
| --- | --- |
| `sloperator.py` | CLI entrypoint: argument parsing, exit codes |
| `sloperator/runner.py` | `run_program` / `check_program` / `run_source` — wires the stages |
| `sloperator/lexer/`, `sloperator/parser/`, `sloperator/evaluator/` | The three stages; `parser/AGENTS.md` adds parser rules |
| `sloperator/errors.py` | `SlopError` plus its lexical, syntax, and runtime subclasses |
| `docs/spec.md` | Language specification |
| `examples/`, `tests/` | Example `.slop` programs, pytest suite |
| `playground/` | Web playground: `uv run playground/server.py` |

## Formatting

Run the formatter after **any** code change, before running the validation suite:

```bash
uv run ruff format
```

Do this as part of the normal workflow, not only when `ruff format --check` complains.
Never leave formatting for the user to fix up.

## Validation

Before calling a change done, all four must pass:

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
uv run pytest tests/test_comparisons.py   # comparison/equality precedence tests
```

## When to add regression tests

Add them to `tests/` next to the behavior they cover (`test_lexer.py`, `test_parser.py`,
`test_evaluator.py`, `test_errors.py`, `test_cli.py`) whenever you:

- fix a bug — reproduce it in a test first, then assert the fix;
- add or change a language feature: syntax, values, scoping, or operators;
- touch error messages, their formatting, or exit codes;
- add a program under `examples/`;
- change CLI flags or `--check` behavior.

## Language behavior

[docs/spec.md](docs/spec.md) is the source of truth for language behavior — syntax,
values, scoping, operators, and error formats. Read it before changing the language
rather than guessing, and update it in the same change.
