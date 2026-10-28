---
description: Review the diff, commit all project changes with the given message, then rebase onto origin/main
---

# Commit

Use `$ARGUMENTS` as the commit message, exactly as given. If it is empty, stop
and ask for one instead of inventing a message.

## 1. Review before staging

Inspect the full working tree without modifying it:

- `git status --short`
- `git diff` for edits to tracked files
- `git ls-files --others --exclude-standard` for new files, then read each one

Confirm the changes are intended and belong to the requested message. Stop and
report instead of committing if you find secrets or credential files, generated
or ignored artifacts, unrelated edits, or anything you do not understand. Never
read or stage `.env` files.

## 2. Stage and commit

1. Stage every project change: `git add -A`.
2. Review the staged set: `git diff --cached --stat` and `git diff --cached`.
3. Commit with the provided message: `git commit -m "$ARGUMENTS"`.
4. Do not add a body, trailers, co-author lines, or sign-off that the message
   does not contain.

## 3. Rebase

Run `git pull --rebase origin main`. Report its output.

If the rebase reports conflicts, stop and list the conflicted paths. Do not
force-push, abort, or resolve conflicts unless asked.

## 4. Report

Give the new commit hash and subject, the files it changed, and the result of the
rebase. If nothing was staged, say so and do not create an empty commit.
