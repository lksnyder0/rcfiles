---
name: todo
description: "Use when managing tasks - adding, completing, cancelling, or listing items as individual commitment notes in the Vaults/Work/Commitments/ folder"
---

# TODO Skill

Manage commitments as individual notes in `/Users/luke.snyder/code/Vaults/Work/Commitments/`, one file per task, frontmatter-driven. This replaces the old single-file `TODO.md` pattern.

## Commitment File Format

Path: `Commitments/YYYY-MM-DD-<slug>.md` where the date is `committed_date` and `<slug>` is the kebab-case title (truncate long titles for the filename; keep the full title in frontmatter).

```markdown
---
title: <Task title, sentence case>
committed_date: YYYY-MM-DD
due_date: YYYY-MM-DD          # omit if open-ended
complexity: low|medium|high
tags:
  - tag-one
  - tag-two
summary: <one sentence, optional>
link: "<source URL, or omit if none>"
status: open
sort_key: <integer>
---

<optional body: sub-tasks as `- [ ]` bullets, notes, or `[Original](link)`>
```

**Conventions:**
- `status` is one of `open`, `done`, `cancelled`.
- On `done`/`cancelled`, add `resolved_date: YYYY-MM-DD`.
- `sort_key` orders open commitments by urgency — see below.
- Quote `title`/`link` in frontmatter only when they contain a colon.

## sort_key Rule

`sort_key` ranks **open** commitments by ascending `due_date`; items with no `due_date` are open-ended/undecided and go first (`sort_key: 0`).

When adding a commitment:
1. Read frontmatter of every `status: open` file in `Commitments/`.
2. Find where the new item's `due_date` fits among the others (no-due-date items first, then ascending due date; ties broken by insertion order — new item goes after existing items with the same due date).
3. Set the new item's `sort_key` to that position.
4. Increment `sort_key` by 1 on every existing open commitment that now sits after it.

Skip `.gitkeep` and any non-frontmatter files when scanning.

## Actions

### `/todo add <description> [--due YYYY-MM-DD] [--complexity low|medium|high] [#tags] [--link URL] [--summary "..."]`
1. Scan `Commitments/*.md` for open items to compute `sort_key` (see rule above).
2. Create `Commitments/YYYY-MM-DD-<slug>.md` (date = today) with the frontmatter above. Default `complexity: medium` if not specified.
3. Write the new file, then update `sort_key` on any bumped files.
4. Confirm to user: "Added commitment: <title> (due <due_date or 'open-ended'>)"

### `/todo done <identifier>`
1. Find the matching file (title/filename substring match, case-insensitive; ask to disambiguate if multiple match).
2. Set `status: done`, add `resolved_date: YYYY-MM-DD` (today).
3. Confirm to user.

### `/todo cancel <identifier>`
1. Same as `done` but `status: cancelled`.

### `/todo list [status]`
1. Read all `Commitments/*.md`, default filter `status: open`.
2. Sort by `sort_key` ascending.
3. Display as: `<due_date or "open-ended"> — <title> (<complexity>)`.

## Implementation

Use Read, Edit, Write, and Glob directly on the markdown files in `/Users/luke.snyder/code/Vaults/Work/Commitments/`. No external scripts needed.
