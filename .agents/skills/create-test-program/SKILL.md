---
name: create-test-program
description: Use when adding a runnable SlopLang example and an exact-output regression test for a language feature described in docs/spec.md. Creates examples/<feature>.slop and an entry in tests/test_example_outputs.py.
---

# Create Test Program

Turn one language feature into a small, focused `.slop` program plus a test that
pins its exact stdout. The example is documentation; the test is the contract.

## Workflow

1. **Confirm the feature in the spec.** Open `docs/spec.md` and read the section
   that defines the feature (syntax, values, operators, scoping, errors). Quote
   the rule you are exercising in your own notes. Do not infer language behavior
   from other examples or from the implementation — the spec is the source of
   truth. If the spec does not define the behavior, stop and ask before writing
   anything.
2. **Name the example.** Use `<feature>.slop`, lowercase kebab-case, in
   `examples/`. Reuse an existing file only when the feature already has a
   dedicated example; otherwise create a new one. Never overwrite an unrelated
   example.
3. **Write the program.** Keep it to one feature and 3–8 `hallucinate` calls.
   Follow the syntax rules exactly:
   - start with a one-line comment introduced by an em dash `—`;
   - terminate every declaration, assignment, `ship`, and expression statement
     with `✨`; never after a closing `}`;
   - use smart quotes `“ ”` (straight quotes are a lexical error);
   - escape `\n`, `\t`, `\”`, `\\` inside strings; never put a raw newline in a
     string;
   - conditions are bare (no parentheses) and must be booleans;
   - `hallucinate` is the only built-in; it separates arguments with one space
     and always ends with a newline.
   Make the program deterministic and finite: no input, no division by zero, no
   reliance on undefined names, no loop that can run forever.
4. **Capture the real output.** From the project root run:

   ```bash
   uv run sloperator.py examples/<feature>.slop
   ```

   Compare the output line by line with what the spec requires. If they differ,
   fix the program (or report a spec/implementation conflict) — never encode
   unexpected output as the expected value.
5. **Add the exact-output test.** Ensure `tests/test_example_outputs.py` exists
   with this shape, and add one entry per example:

   ```python
   """Exact stdout for examples that demonstrate a language feature."""

   from pathlib import Path

   import pytest

   from sloperator.runner import run_source

   EXAMPLES = Path(__file__).resolve().parent.parent / "examples"
   EXPECTED_OUTPUT = {
       "equality": "✅\n❌\n❌\n",
   }


   @pytest.mark.parametrize(("stem", "expected"), EXPECTED_OUTPUT.items(), ids=EXPECTED_OUTPUT.keys())
   def test_example_output(stem: str, expected: str):
       path = EXAMPLES / f"{stem}.slop"
       result = run_source(path.read_text(encoding="utf-8"))
       assert result.stderr == ""
       assert result.exit_code == 0
       assert result.stdout == expected
   ```

   Rules for the entry:
   - the key is the filename stem, with no `.slop`;
   - the value is the exact stdout as a Python literal, including the final
     newline from `hallucinate`;
   - write one `\n` per output line; never use `.strip()`, `.split()`, or a
     substring assertion;
   - keep entries sorted by stem so diffs stay reviewable;
   - do not weaken or rerun-through-`pytest.skip` an entry to make it pass.
6. **Test.** Run the focused tests first, then the full gate from `AGENTS.md`:

   ```bash
   uv run pytest tests/test_example_outputs.py tests/test_examples.py
   uv run pytest
   uv run ruff format --check
   uv run ruff check
   uv run ty check
   ```

   `tests/test_examples.py` already asserts every `examples/*.slop` runs cleanly,
   so this only needs the exact stdout added. Report any check that fails and
   fix the cause; do not reformat unrelated files.

## Definition of done

- `docs/spec.md` still describes the behavior the example relies on.
- `examples/<feature>.slop` exists, is deterministic, and prints only the
  intended output.
- `tests/test_example_outputs.py` pins that output byte for byte.
- All four project checks pass.
- The final summary lists the example path, the expected stdout, and the test
  command that was run.
