---
name: todo
description: "Use when managing tasks - adding, completing, cancelling, or listing items as individual commitment notes in the Vaults/Work/Commitments/ folder"
allowed-tools: Bash(python3 *), Read, Glob
---

# TODO Skill

Manage commitments as individual notes in `/Users/luke.snyder/code/Vaults/Work/Commitments/`, one file per task, frontmatter-driven. This replaces the old single-file `TODO.md` pattern and shares its schema, dedup, and `sort_key` ordering with the `sod` skill — reuse `sod.py` rather than re-implementing any of that here.

**Script:** `~/.claude/skills/sod/sod.py` (all commands below assume `python3 ~/.claude/skills/sod/sod.py`)

## Commitment File Format

Path: `Commitments/YYYY-MM-DD-<slug>.md`. Frontmatter fields: `title`, `committed_date`, `due_date` (omit if open-ended), `complexity` (`low`/`medium`/`high`), `tags`, `summary`, `link`, `status` (`open` or `done` — this is the only vocabulary `sod.py` understands, so don't invent others), `sort_key`. On completion/cancellation add `resolved_date: YYYY-MM-DD`. `sort_key` is recomputed by `sod.py commitments`: overdue first, then ascending `due_date`, undated last, complexity as tiebreaker within a tier — never hand-assign it.

## Actions

### `/todo add <description> [--due YYYY-MM-DD] [--complexity low|medium|high] [#tags] [--summary "..."]`
1. `link` is the row key `sod.py` dedups on. Manual adds have no natural URL, so synthesize one: `manual://<slugified-description>`.
2. ```bash
   python3 ~/.claude/skills/sod/sod.py commit-add \
     --title "<description>" \
     --summary "<--summary, or the description itself>" \
     --link "manual://<slug>" \
     --committed-date <today> \
     [--due-date <date>] \
     --complexity <low|medium|high, default medium> \
     [--tags <comma-separated>]
   ```
3. ```bash
   python3 ~/.claude/skills/sod/sod.py commitments
   ```
4. Report the script's `created`/`updated`/`duplicate` result — don't re-litigate it.

### `/todo done <identifier>`
1. Find the matching file in `Commitments/` (title/filename substring match, case-insensitive; ask to disambiguate if multiple match).
2. Set `status: done`, add `resolved_date: YYYY-MM-DD` (today).
3. Run `python3 ~/.claude/skills/sod/sod.py commitments` to recompute ordering.
4. Confirm to user.

### `/todo cancel <identifier>`
Same as `done`, but `sod.py` only recognizes `open`/`done` — there is no `cancelled` status. Set `status: done`, add `resolved_date`, and prepend `_Cancelled — not pursued._` to the note body so it's distinguishable from a real completion.

### `/todo list [status]`
1. Glob `Commitments/*.md` (skip `.gitkeep`), read frontmatter, default filter `status: open`.
2. Sort by `sort_key` ascending.
3. Display as: `<due_date or "open-ended"> — <title> (<complexity>)`.

## Implementation

Delegate every write to `sod.py` (add/done/cancel change frontmatter directly for done/cancel since `sod.py` has no such subcommands, but always finish with `sod.py commitments` to keep `sort_key` consistent). `list` is read-only via Glob/Read — no script needed for that.
