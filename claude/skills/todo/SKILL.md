---
name: todo
description: "Use when managing self-directed tasks - adding, completing, marking waiting, listing, or moving items in the Commitments/ note pool in the Obsidian vault"
---

# TODO Skill

Manage self-directed tasks as Commitments-format notes (file-per-row, frontmatter) in the shared `Commitments/` folder at `/Users/luke.snyder/code/Vaults/Work/Commitments/`, via the `sod.py` CLI at `~/.rcfiles/claude/skills/sod/sod.py`. Self-directed tasks sit in the same pool as Slack/email commitments, distinguished only by a synthetic `todo://<slug>` link instead of a real permalink. The `Commitments.base` Obsidian Base and the `IMPORTANT TODAY/THIS WEEK` daily-note section already render whatever is in this pool — this skill never edits vault files directly, it only calls the CLI.

## Status vocabulary

`open` (actionable) | `waiting` (blocked on someone else, informational) | `done` (closed). All three show up in the Base's "All" view; only `open` items appear in the Daily Note View / IMPORTANT TODAY ranking.

## Actions

Parse the user's `/todo` invocation and run ONE of these with Bash, from `~/.rcfiles/claude/skills/sod/`:

### `/todo add <description> [#tags] [--due YYYY-MM-DD] [--complexity low|medium|high]`

```bash
python3 sod.py todo-add --title "<description>" --tags "<tag1,tag2>" --due-date <date> --complexity <level>
```

Omit `--tags`, `--due-date`, or `--complexity` entirely if the user didn't give one — do not pass empty values. Confirm to the user using the command's own output: `created: <path>`, `duplicate: <path>` if an identical task already exists, or `updated: <path>` if a similar existing task's due date was updated instead.

### `/todo done <identifier>`

```bash
python3 sod.py todo-done "<identifier>"
```

### `/todo wait <identifier>`

```bash
python3 sod.py todo-wait "<identifier>"
```

### `/todo list [status]`

```bash
python3 sod.py todo-list --status <open|waiting|done|all>
```

Default to `open` if the user doesn't specify a status.

### `/todo move <identifier> <status>`

```bash
python3 sod.py todo-move "<identifier>" <open|waiting|done>
```

Use this for anything `done`/`wait` don't cover directly — most commonly, reopening a `waiting` or `done` item back to `open`.

## Identifier resolution

`<identifier>` is either:
- **A number** — the 1-indexed position in the current `todo-list` ordering for the pool being acted on (open items by default).
- **Text** — a case-insensitive substring match against task titles.

If a text identifier matches more than one task, the error lists the candidates; if it matches none, it says so with no task found — relay that back to the user and ask them to be more specific rather than guessing.

If the user wants to act on an item that isn't currently `open` (e.g. completing something marked `waiting`), pass `--status waiting` (or the relevant status) on the underlying `sod.py` command so the identifier resolves against the right pool.
