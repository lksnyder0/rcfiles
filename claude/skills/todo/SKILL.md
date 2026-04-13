---
name: todo
description: "Use when managing tasks - adding, completing, cancelling, listing, or moving items in the central TODO.md file in the Obsidian vault"
---

# TODO Skill

Manage a central task list at `/Users/luke.snyder/code/Vaults/Work/TODO.md` with kanban-style sections, cross-linked to Obsidian daily notes.

## TODO.md Format

```markdown
# TODO

## Today
- [ ] Task description #tag #priority ([[YYYY-MM-DD]])

## Backlog
- [ ] Task description #tag ([[YYYY-MM-DD]])

## Waiting
- [ ] Task description — waiting on X ([[YYYY-MM-DD]])

## Done
- [x] Completed task #tag ([[YYYY-MM-DD]]) ✅ [[YYYY-MM-DD]]
- [-] Cancelled task #tag ([[YYYY-MM-DD]]) ❌ [[YYYY-MM-DD]]
```

**Conventions:**
- Standard markdown checkboxes (`- [ ]`, `- [x]`, `- [-]`)
- Inline `#tags` for topic and priority (Obsidian-compatible)
- Creation date as daily note link: `([[2026-03-30]])`
- Completion/cancellation date appended: `✅ [[2026-03-31]]` or `❌ [[2026-03-31]]`
- Sub-items are indented bullets under the parent task
- Sections are `## Today`, `## Backlog`, `## Waiting`, `## Done`

## Actions

Parse the user's `/todo` invocation and execute ONE of these actions:

### `/todo add <description> [#tags] [--today|--waiting]`
1. Read `TODO.md`
2. Create task line: `- [ ] <description> [#tags] ([[YYYY-MM-DD]])`
3. Append under `## Backlog` by default, or `## Today` if `--today`, or `## Waiting` if `--waiting`
4. Write updated `TODO.md`
5. Confirm to user: "Added to [section]: <description>"

### `/todo done <identifier>`
1. Read `TODO.md`
2. Find the task matching `<identifier>` (number by position in active sections, or text substring match)
3. Change `- [ ]` to `- [x]`
4. Append ` ✅ [[YYYY-MM-DD]]` with today's date
5. Move the task (and any sub-items) from its current section to `## Done`
6. Write updated `TODO.md`
7. Read today's daily note (`Daily notes/YYYY-MM-DD.md`), create if missing
8. Add under a `## Completed` heading (create heading if missing): `- [x] <task description> ([[TODO]])`
9. Confirm to user

### `/todo cancel <identifier>`
1. Same as `done` but change `- [ ]` to `- [-]` and append ` ❌ [[YYYY-MM-DD]]`
2. Cross-link to daily note under `## Completed`: `- [-] <task description> ([[TODO]])`

### `/todo list [section]`
1. Read `TODO.md`
2. If no section specified: display all tasks in `## Today`, then show counts for Backlog and Waiting
3. If section specified: display all tasks in that section
4. Format output as a clean list with section headers

### `/todo move <identifier> <section>`
1. Read `TODO.md`
2. Find the task matching `<identifier>`
3. Remove it (and any sub-items) from its current section
4. Insert it under the target section (`today`, `backlog`, or `waiting`)
5. Write updated `TODO.md`
6. Confirm to user: "Moved to [section]: <description>"

## Task Identification

When the user provides an `<identifier>`:
- **Number**: Count tasks across Today, Backlog, and Waiting sections (1-indexed). Task 1 is the first task in Today, numbering continues through Backlog, then Waiting.
- **Text**: Substring match against task descriptions (case-insensitive). If ambiguous, ask the user to clarify.

## Cross-Linking Rules

- **On task creation**: Task gets `([[YYYY-MM-DD]])` linking to the daily note for the creation date
- **On task completion/cancellation**: Task gets `✅ [[YYYY-MM-DD]]` or `❌ [[YYYY-MM-DD]]`, and today's daily note gets an entry under `## Completed`
- **Daily note path**: `Daily notes/YYYY/MM-<Month>/YYYY-MM-DD.md` relative to vault root (e.g., `Daily notes/2026/03-March/2026-03-30.md`). Create parent directories if they don't exist.

## Implementation

Use Read, Edit, and Write tools directly on the markdown files. No external scripts or plugins needed. The TODO.md file and daily notes are plain markdown in the Obsidian vault at `/Users/luke.snyder/code/Vaults/Work/`.
