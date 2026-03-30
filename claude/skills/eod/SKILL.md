---
name: eod
description: "Use when the user wants to write their end-of-day summary, generate a daily note, or review what they accomplished today"
allowed-tools: Bash(gh *), Glob, Read, Write, Edit, mcp__shortcut__users-get-current, mcp__shortcut__stories-search, mcp__shortcut__users-get-current-teams, mcp__glean_claude-code__search
---

# End-of-Day Summary

Generate a structured daily note by gathering activity from Shortcut, GitHub, Slack, Google Calendar, specs, and TODO.md. Present a draft for review, then write the daily note and update TODO.md.

**Vault root:** `/Users/luke.snyder/code/Vaults/Work`
**Daily note path:** `Daily notes/YYYY-MM-DD.md` (use today's date)
**TODO.md path:** `TODO.md` (relative to vault root)
**Specs path:** `Specs/` (relative to vault root)
**Notes path:** `Notes/` (relative to vault root)

## Step 1: Gather Data

Gather data from all sources in parallel. Each source is independent — if one fails, note it and continue with the others.

### 1a. Shortcut Stories

1. Call `mcp__shortcut__users-get-current` to get your user ID and mention name.
2. Call `mcp__shortcut__users-get-current-teams` to find the SRE team ID. From the returned teams, select the team whose name contains 'SRE'.
3. Call `mcp__shortcut__stories-search` with a natural language query string describing what you need (e.g., "Search for stories where the owner is [user mention name] and updated after [today's date in YYYY-MM-DD]"). Let the tool interpret the query — do not assume specific filter syntax.
4. Call `mcp__shortcut__stories-search` with a natural language query string for team stories (e.g., "Search for stories owned by team [SRE team name] and updated after [today's date in YYYY-MM-DD]").
5. Deduplicate stories that appear in both result sets (match by story ID).
6. For each story, record:
   - Story ID (e.g., `SC-12345`)
   - Title
   - Workflow state (e.g., "Done", "In Development", "Ready for Review", "Blocked")
   - Whether it was completed today (moved to a "Done"-type state today)
7. Categorize:
   - **Completed**: stories in a "Done"-type workflow state
   - **In Progress**: stories in active workflow states ("In Development", "Ready for Review", etc.)
   - **Blocked**: stories explicitly marked blocked

If Shortcut MCP tools are unavailable or error, record: `"Shortcut: unavailable"` and continue.

### 1b. GitHub PRs

Run these `gh` commands (scoped to `huntresslabs` org):

1. PRs authored by user, updated today:
   ```bash
   gh search prs --author @me --updated ">=$(date +%Y-%m-%d)" --owner huntresslabs --json number,title,repository,state,url,updatedAt --limit 50
   ```

2. PRs reviewed by user today:
   ```bash
   gh search prs --reviewed-by @me --updated ">=$(date +%Y-%m-%d)" --owner huntresslabs --json number,title,repository,state,url,updatedAt --limit 50
   ```

3. PRs merged by user today:
   ```bash
   gh search prs --author @me --merged ">=$(date +%Y-%m-%d)" --owner huntresslabs --json number,title,repository,state,url,updatedAt --limit 50
   ```

For each PR, record:
- Repo name (e.g., `huntresslabs/infra-aws`)
- PR number and title
- State: merged, open, closed
- Whether the user authored or reviewed it

Categorize:
- **Completed**: merged PRs
- **In Progress**: open PRs (authored or under review)

If `gh` errors or is unavailable, record: `"GitHub: unavailable"` and continue.

### 1c. Slack Messages (via Glean)

Call `mcp__glean_claude-code__search` with a query to find the user's Slack messages and mentions from today. Use filters like `app:slack updated:today from:"Luke Snyder"`.

For each relevant result:
- Extract the channel or DM context (e.g., `#sre-team`, `DM from @jane`)
- Summarize the key thread topic, decision, or action item in one line
- Scan for commitment language indicating promised action items:
  - Patterns: "I'll", "I can", "will do", "let me", "I'll take a look", "action item", "I'll follow up", "I'll handle", "I'll check"
  - For each detected commitment, record the promise text and the source (channel/DM)

If Glean is unavailable or returns no Slack results, record: `"Slack: unavailable"` and continue.

### 1d. Google Calendar (via Glean)

Call `mcp__glean_claude-code__search` with a query to find the user's calendar events for today. Use filters like `app:calendar updated:today`.

For each event, record:
- Meeting title
- Start time
- Key attendees (if available)

If Glean returns no calendar results, record: `"Calendar: unavailable"` and continue.

### 1e. Specs Written Today

1. Use Glob to find specs written today:
   ```
   Glob pattern: Vaults/Work/Specs/YYYY-MM-DD-*.md (substitute today's date)
   ```
2. For each spec found, Read the file and extract:
   - The title (first `#` heading)
   - A one-line summary of what was designed (from the Overview section or first paragraph)
3. Identify related Obsidian Notes by scanning the spec content for topic keywords that match files in `Vaults/Work/Notes/`. Use Glob to list available Notes files and match against spec content.
   - Example: a spec mentioning "Tailscale" links to `[[Tailscale]]` if `Notes/Tailscale.md` exists
   - Example: a spec about "Elasticsearch data streams" links to `[[elasticsearch]]` if `Notes/elasticsearch.md` exists
4. For each spec, prepare a backlink line: `> Daily note: [[YYYY-MM-DD]]` (today's date). Insert it immediately after the YAML frontmatter closing `---` delimiter (if present), with a blank line before the first heading. If no frontmatter exists, insert it as the first line of the file.

If no specs match today's date, skip this section.

### 1f. TODO.md

1. Read `Vaults/Work/TODO.md`
2. Extract all items from the `## Today` and `## Backlog` sections
3. These are used later for:
   - Cross-referencing against detected promised action items (to avoid suggesting duplicates)
   - Generating the "tomorrow" recommendation

### All Sources Check

If ALL data sources returned unavailable or empty results (no stories, no PRs, no Slack messages, no calendar events, no specs, and TODO.md is empty), report to the user:
> "All data sources returned empty or unavailable. Nothing to summarize today."

Stop here — do not proceed to synthesis.

## Step 2: Synthesize

### Deduplication

- If a Shortcut story has a linked GitHub PR (check if the PR title or branch contains the story ID like `sc-12345`), show it once in whichever section provides more context. Prefer the Shortcut entry for completed stories (it has workflow context) and the GitHub entry for in-progress PRs (it has review status).

### Promised Action Item Detection

1. Collect all commitment-language matches from Slack messages (gathered in Step 1c).
2. Collect any commitments from Shortcut story comments if available.
3. For each detected commitment:
   - Check if a matching item already exists in TODO.md (fuzzy match on description keywords)
   - If no match found, add it to the **Suggested TODOs** list with the source context (e.g., "promised in #sre-team")
4. If no commitments are detected, omit the Suggested TODOs section.

### Tomorrow Recommendation

Determine the single most important thing to start with tomorrow by combining:
1. Items in TODO.md `## Today` that are still open (highest priority — user already flagged these)
2. Open Shortcut stories assigned to user, prioritized by:
   - Stories in the current iteration first
   - Stories closest to completion (e.g., "Ready for Review" > "In Development")
3. Pending PR reviews requested from the user

Pick one item and present it as the top recommendation with a brief reason why.

### Build the Draft

Assemble the daily note draft with these sections (omit any section that has no data):

1. `## Completed` — completed Shortcut stories and merged PRs
2. `## In Progress` — active stories and open PRs
3. `## Meetings` — calendar events with time and title
4. `## Slack Highlights` — key threads, decisions, action items
5. `## Specs Written` — specs from today with links to related Notes
6. `## Suggested TODOs` — detected commitments not in TODO.md
7. `## Tomorrow` — single highest-priority recommendation

## Step 3: Present Draft for Review

Present the complete draft to the user in the terminal. Format it exactly as it will appear in the daily note (markdown with checkboxes, wiki links, etc.).

If any data sources were unavailable, note this at the top:
> **Note:** The following sources were unavailable: [list]. Data from these sources is not included.

Then ask:
> "Here's your EOD summary. You can:
> 1. **Approve** as-is
> 2. **Edit** — tell me what to change (add context, remove items, correct details)
> 3. For **Suggested TODOs** — tell me which to add (and to which section: Today/Backlog/Waiting) and which to dismiss
>
> What would you like to do?"

Wait for the user's response. If they request edits, make them and re-present. Only proceed to Step 4 when the user approves.

## Step 4: Write Output

### 4a. Update or Create the Daily Note

**Path:** `/Users/luke.snyder/code/Vaults/Work/Daily notes/YYYY-MM-DD.md`

- If the file does not exist, create it with the approved draft content.
- If the file already exists, merge the new content:
  - For each section (`## Completed`, `## In Progress`, etc.):
    - If the section heading already exists in the file, append new items below existing items in that section.
    - If the section heading does not exist, add the section at the appropriate position in the file.
  - Never overwrite or remove existing content.

### 4b. Add Backlinks to Specs

For each spec found in Step 1e:
- Read the spec file
- If it does not already contain a backlink to today's daily note, insert `> Daily note: [[YYYY-MM-DD]]` immediately after the YAML frontmatter closing `---` delimiter (if present), with a blank line before the first heading. If no frontmatter exists, insert it as the first line of the file.
- Write the updated spec file

### 4c. Update TODO.md

For each Suggested TODO the user approved:
1. Read `Vaults/Work/TODO.md`
2. Add the item under the section the user chose (Today, Backlog, or Waiting):
   ```
   - [ ] Description ([[YYYY-MM-DD]])
   ```
3. Write the updated TODO.md

For dismissed Suggested TODOs: remove them from the daily note's `## Suggested TODOs` section. If all were dismissed, omit the section entirely.

### Obsidian Formatting Conventions

Use these conventions throughout all written content:
- Wiki links for cross-references: `[[YYYY-MM-DD]]`
- Checkbox syntax: `- [x]` for completed, `- [ ]` for open
- Shortcut story links as URLs: `[SC-12345: Story title](https://app.shortcut.com/huntress/story/12345)`
- Spec links with display text: `[[2026-03-30-eod-skill-design|EOD Skill Design]]`
- Note links: `[[Tailscale]]`, `[[elasticsearch]]`, etc.
- Meeting times in 24h format: `10:00 — Meeting title`
- Slack highlights as plain bullets: `- #channel: Summary of thread`

### Completion

After writing all files, confirm to the user:
> "EOD summary written to `Daily notes/YYYY-MM-DD.md`. [N] TODOs added to TODO.md. [N] specs backlinked."
