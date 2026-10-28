---
name: create-and-validate
description: Use when adding a SlopLang language-feature example end to end. Loads the create-test-program skill to write the example and exact-output test, then the validate skill to run the project checks. Defers to those skills instead of repeating their instructions.
---

# Create and Validate

Composite workflow. The authoritative rules live in the two referenced skills;
this skill only sequences them. Load each one with the skill tool and follow it
as written — do not copy, paraphrase, or extend its steps here.

## Workflow

1. **Create the example and test.** Load `create-test-program` (ID:
   `create-test-program`) and follow its workflow end to end. It owns reading
   `docs/spec.md`, the SlopLang syntax rules, the `examples/<feature>.slop`
   layout, and the exact-output entry in `tests/test_example_outputs.py`.
   Loading it may require approval; wait for the request to be approved.
2. **Validate.** After the files exist, load `validate` (ID: `validate`) and
   follow it to run the project checks from the repository root. Also run the
   `ty check` gate required by `AGENTS.md`, which `validate` does not cover.
3. **Report.** If any check fails, fix the cause and rerun step 2. In the final
   summary state that both skills were loaded, the example path, its exact
   stdout, and each check's result.

## Maintenance

If a rule needs to change, edit the skill that owns it:
`.agents/skills/create-test-program/SKILL.md` or
`.agents/skills/validate/SKILL.md`. Never fork their content into this file.

## Definition of done

- `create-test-program` and `validate` were both loaded and followed.
- The new example and its exact-output test exist and pass.
- Every check named in step 2 passes.
