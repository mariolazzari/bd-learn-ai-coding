# Sloperator

A tree-walking interpreter for SlopLang, written in Python.

```bash
uv run sloperator.py examples/fib.slop      # run a program
uv run sloperator.py --check program.slop   # lex and parse only
uv run pytest                               # tests
uv run ruff format --check                  # formatting
uv run ruff check                           # linting
uv run ty check                             # type checking
```

## Playground

`uv run playground/server.py`, then open <http://localhost:8080>.

## Language

SlopLang files use the `.slop` extension and end statements with `✨`. The full
specification — keywords, values, scoping, control flow, operators, grammar, and
errors — lives in [docs/spec.md](docs/spec.md). More programs are in `examples/`.

```slop
clanker describe(count) {
    vibe count > 1 { ship “big slop”✨ } nah { ship “small slop”✨ }
}
slop count = 0✨
ralph count < 3 {
    hallucinate(describe(count))✨
    count = count + 1✨
}
```

Prints `small slop` twice, then `big slop`.

## Layout

| Path                    | What it is                                           |
| ----------------------- | ---------------------------------------------------- |
| `sloperator.py`         | Command-line entrypoint                              |
| `sloperator/lexer/`     | Source text to tokens                                |
| `sloperator/parser/`    | Tokens to AST (`ast.py` holds the node definitions)  |
| `sloperator/evaluator/` | Walks the AST: values, environments, the interpreter |
| `sloperator/runner.py`  | Runs source through all three stages                 |
| `docs/spec.md`          | The language specification                           |
| `examples/`             | Example programs                                     |
| `tests/`                | Pytest suite                                         |
| `playground/`           | A tiny web server and editor page for running code   |
