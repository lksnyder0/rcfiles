---
name: eod
description: "Use when the user wants to write their end-of-day summary, generate a daily note, or review what they accomplished today"
allowed-tools: Bash(gh *), Bash(python3 *), Glob, Read, Write, Edit, mcp__shortcut__stories-search, mcp__glean_claude-code__search
---

# End-of-Day Summary

Generate a structured daily note by gathering activity from Shortcut, GitHub, Slack, specs, Claude Code sessions, and TODO.md. Write the daily note, update TODO.md, and update Obsidian Notes.

**Vault root:** `/Users/luke.snyder/code/Vaults/Work`
**Daily note path:** `Daily notes/YYYY/MM-<Month>/YYYY-MM-DD.md` (use today's date, e.g., `Daily notes/2026/03-March/2026-03-30.md`)
**TODO.md path:** `TODO.md` (relative to vault root)
**Specs path:** `Specs/` (relative to vault root)
**Notes path:** `Notes/` (relative to vault root)

**Shortcut constants (do not look these up at runtime):**
- **User mention name:** `lukesnyder`
- **User ID:** `62669f7b-b605-4cc7-86c4-ce48baf7d6e9`
- **SRE team mention name:** `infra-sre`
- **SRE team ID:** `696ffe68-beb6-46f5-ac94-be72a7974939`

## Step 1: Gather Data

Gather data from all sources in parallel. Each source is independent — if one fails, note it and continue with the others.

**Shared lookup:** At the start of Step 1, use Glob once to list all files in `Vaults/Work/Notes/`. Cache this list and reuse it in Steps 1d, 1e.5, and 2.2 — do not re-glob the Notes directory.

### 1a. Shortcut Stories

Use the hardcoded Shortcut constants above — do not call `users-get-current` or `users-get-current-teams`.

1. Call `mcp__shortcut__stories-search` with `owner` set to `lukesnyder` and `updated` set to `today` to find stories owned by the user and updated today.
2. Call `mcp__shortcut__stories-search` with `requester` set to `lukesnyder` and `updated` set to `today` to find stories requested by the user and updated today.
3. Call `mcp__shortcut__stories-search` with `team` set to `infra-sre` and `updated` set to `today` to find team stories updated today.
4. Deduplicate stories that appear in multiple result sets (match by story ID).
5. For each story, record:
   - Story ID (e.g., `SC-12345`)
   - Title
   - Workflow state (e.g., "Done", "In Development", "Ready for Review", "Blocked")
   - Whether it was completed today (moved to a "Done"-type state today)
6. Categorize:
   - **Completed**: stories in a "Done"-type workflow state
   - **In Progress**: stories in active workflow states ("In Development", "Ready for Review", etc.)
   - **Blocked**: stories explicitly marked blocked

If Shortcut MCP tools are unavailable or error, record: `"Shortcut: unavailable"` and continue.

### 1b. GitHub PRs

Run these `gh` commands (scoped to `huntresslabs` org):

1. PRs authored by user, updated today:
   ```bash
   gh search prs --author @me --updated ">=$(date +%Y-%m-%d)" --owner huntresslabs --json number,title,repository,state,url,updatedAt,headRefName --limit 50
   ```

2. PRs reviewed by user today:
   ```bash
   gh search prs --reviewed-by @me --updated ">=$(date +%Y-%m-%d)" --owner huntresslabs --json number,title,repository,state,url,updatedAt,headRefName --limit 50
   ```

3. PRs merged by user today:
   ```bash
   gh search prs --author @me --merged ">=$(date +%Y-%m-%d)" --owner huntresslabs --json number,title,repository,state,url,updatedAt,headRefName --limit 50
   ```

4. PRs where user's review is still requested (for Tomorrow recommendation):
   ```bash
   gh search prs --review-requested @me --state open --owner huntresslabs --json number,title,repository,url,createdAt --limit 50
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

### 1d. Specs Written Today

1. Use Glob to find specs written today:
   ```
   Glob pattern: Vaults/Work/Specs/YYYY-MM-DD-*.md (substitute today's date)
   ```
2. For each spec found, Read the file and extract:
   - The title (first `#` heading)
   - A one-line summary of what was designed (from the Overview section or first paragraph)
3. Identify related Obsidian Notes by scanning the spec content for topic keywords that match the cached Notes file list.
   - Example: a spec mentioning "Tailscale" links to `[[Tailscale]]` if `Notes/Tailscale.md` exists
   - Example: a spec about "Elasticsearch data streams" links to `[[elasticsearch]]` if `Notes/elasticsearch.md` exists
4. Record each spec for backlinking in Step 3b (do not write to spec files yet).

If no specs match today's date, skip this section.

### 1e. Claude Code Sessions

Read pre-built session index files for metadata. For research sessions, do targeted transcript reads to extract key findings (see step 6).

**Index location:** `~/.claude/session-index/*.json`

**Procedure:**

1. **Load today's sessions.** Run the helper script:
   ```bash
   python3 ~/.claude/skills/eod/load_sessions.py YYYY-MM-DD
   ```
   This returns a JSON array of matching session objects (filters by `days_active`, `started_at`, or `ended_at`). Parse the output.

2. **Categorize each session:**
   - **Started**: `started_at` date == today
   - **Ongoing**: `started_at` date < today AND today is in `days_active` AND `status` == "active"
   - **Completed**: `ended_at` date == today
   A same-day session appears as both "started" and "completed."

3. **Read pre-computed data directly from each session's index:**
   - `classification` — session type (research, implementation, planning, mixed, other)
   - `first_messages` — the session's purpose (first 3 user messages)
   - `tool_counts` — tool usage distribution
   - `research_queries` — research tool calls with queries and timestamps
   - `file_writes` — files created or modified
   - `open_tasks` — tasks created but not completed

4. **For multi-day sessions, build the activity chain.** From `days_active`, construct a chronological chain of wiki-linked dates for cross-referencing in the daily note:
   - Format: `[[2026-04-14]] > [[2026-04-15]] > **[[2026-04-16]]**`
   - Today's date is bolded
   - The "day N" count equals `len(days_active)`

5. **For research sessions, identify related Obsidian Notes.** For each research session, match the session's primary topic keywords (from `first_messages` and `research_queries`) against the cached Notes file list. Record matches.

6. **For research sessions, extract key findings.** Use `research_queries` from the index to do targeted reads of `transcript_path`:
   a. For each research query, search the JSONL for tool_use blocks matching the tool name and query.
   b. Read the assistant text block(s) that immediately follow each matching tool result.
   c. Extract a concise summary (2-4 bullet points) of what was learned.
   This is a targeted scan of specific sections, not a full-file parse.
   If `transcript_path` does not exist or is unreadable, skip key findings for that session and continue.

If the session index directory does not exist, contains no files, or files fail to parse, record: `"Claude Sessions: unavailable"` and continue.

If no sessions match today's date, skip this section.

### 1f. TODO.md

1. Read `Vaults/Work/TODO.md`
2. Extract all items from the `## Today` and `## Backlog` sections
3. These are used later for:
   - Cross-referencing against detected promised action items (to avoid suggesting duplicates)
   - Generating the "tomorrow" recommendation

### All Sources Check

If ALL data sources returned unavailable or empty results (no stories, no PRs, no Slack messages, no specs, no Claude sessions, and TODO.md is empty), stop here — do not proceed to synthesis or write any files.

## Step 2: Synthesize

### Deduplication

- If a Shortcut story has a linked GitHub PR (check if the PR title or branch name `headRefName` contains the story ID like `sc-12345`), show it once in whichever section provides more context. Prefer the Shortcut entry for completed stories (it has workflow context) and the GitHub entry for in-progress PRs (it has review status).

### Knowledge Base Updates

The `Vaults/Work/Notes/` directory is a living knowledge base. Notes should reflect the **current state** of systems, standards, and architecture — not just research history. All data sources from Step 1 can trigger Note updates, not just research sessions.

**1. Collect all Note-relevant events from today's data:**

For each source, extract items that represent real-world changes to systems, standards, or architecture:

| Source | What qualifies as a Note-worthy event |
|--------|--------------------------------------|
| **Merged PRs** | Any merged PR. Match by: repo name against Note filenames (e.g., `infra-aws` → `[[AWS]]`), PR title keywords, and branch name keywords from `headRefName`. |
| **Completed stories** | Stories in a "Done" state. Match story title/description keywords against Note filenames. |
| **Specs written** | Any spec from Step 1d. Already has related Notes identified — use those matches. |
| **Slack decisions** | Messages containing decision language: "we decided", "going forward", "new standard", "we're switching to", "approved", "agreed". Match thread topic against Note filenames. |
| **Research sessions** | Sessions classified as "research" in Step 1e. Already has related Notes identified via topic keyword matching. Use key findings from Step 1e.6. |

**2. Match events to existing Notes:**

Using the cached Notes file list, match each Note-worthy event against Note filenames using:
- Direct filename match (case-insensitive): PR in `infra-elastic` repo → `Notes/elasticsearch.md`
- Keyword extraction from titles, descriptions, and file paths
- Repo-to-topic mapping based on the Repository Map in CLAUDE.md (e.g., `infra-k8s` → `ArgoCD`, `Kubernetes`; `detection-engine` → `Sigma`, `Elasticsearch`)

Matching is filename-based only — do not read Note files during this step.

**3. For each matched Note, prepare an update:**

Read the matched Note files (batch reads in parallel where possible). For each matched event, determine if it contains information not already present in the Note. Prepare an update entry with:
- Source type and reference (PR link, story link, Slack channel, spec link, or session summary)
- What changed or was decided — focus on facts that affect how the system works, not activity logs
- Backlink to today's daily note

**4. For unmatched events, suggest new Notes:**

If a Note-worthy event's topic doesn't match any existing Note file, add it to the **Suggested New Notes** list. Only suggest Notes for topics that are likely to have ongoing relevance (skip one-off bug fixes or trivial changes).

**5. Open session tasks.**

For each session with open (incomplete) tasks detected in Step 1e, add them to the **Suggested TODOs** list with the source context (e.g., "open task from Claude session at 10:46 in /code").

### Promised Action Item Detection

1. Collect all commitment-language matches from Slack messages (gathered in Step 1c).
2. For each detected commitment:
   - Check if a matching item already exists in TODO.md (fuzzy match on description keywords)
   - If no match found, add it to the **Suggested TODOs** list with the source context (e.g., "promised in #sre-team")
3. If no commitments are detected AND no open session tasks exist (from Step 2.5), omit the Suggested TODOs section.

### Tomorrow Recommendation

Determine the single most important thing to start with tomorrow by combining:
1. Items in TODO.md `## Today` that are still open (highest priority — user already flagged these)
2. Open Shortcut stories assigned to user, prioritized by:
   - Stories in the current iteration first
   - Stories closest to completion (e.g., "Ready for Review" > "In Development")
3. Pending PR reviews requested from the user

Pick one item and present it as the top recommendation with a brief reason why.

### Assemble the Daily Note

Build the daily note content with these sections (omit any section that has no data):

1. `## Completed` — completed Shortcut stories and merged PRs
2. `## In Progress` — active stories and open PRs
3. `## Slack Highlights` — key threads, decisions, action items
4. `## Specs Written` — specs from today with links to related Notes
5. `## Claude Sessions` — summary of today's Claude Code sessions (time, cwd, type, topic). For research sessions, include key findings as sub-bullets. For multi-day sessions, show under a `### Ongoing Sessions` sub-heading with the activity chain: `Active: [[date1]] > [[date2]] > **[[today]]**` (today bolded). Include the day count as "(day N, status)".
6. `## Knowledge Base Updates` — updates to existing Obsidian Notes based on all sources (merged PRs, completed stories, specs, Slack decisions, research sessions). For each Note, list the updates with source references.
7. `## Suggested New Notes` — topics from today's activity that don't match existing Notes and have ongoing relevance. Show the proposed Note filename and a brief description of what it would contain.
8. `## Suggested TODOs` — detected commitments not in TODO.md, plus open tasks from Claude sessions
9. `## Tomorrow` — single highest-priority recommendation

## Step 3: Write Output

Write all output files directly. No review gate — all suggested items (TODOs, Research Note Updates, New Notes) are auto-accepted.

**Execution order:** Run 3a first (creates/updates the daily note). Then run 3b, 3c, and 3d in parallel (they write to independent files). Run 3e last (it modifies the daily note written in 3a).

### 3a. Update or Create the Daily Note

**Path:** `/Users/luke.snyder/code/Vaults/Work/Daily notes/YYYY/MM-<Month>/YYYY-MM-DD.md` (e.g., `Daily notes/2026/03-March/2026-03-30.md`). Create parent directories if they don't exist.

- If the file does not exist, create it with the draft content.
- If the file already exists, merge the new content:
  - For each section (`## Completed`, `## In Progress`, etc.):
    - If the section heading already exists in the file, append new items below existing items in that section.
    - If the section heading does not exist, add the section at the appropriate position in the file.
  - Never overwrite or remove existing content.

### 3b. Add Backlinks to Specs

For each spec found in Step 1d:
- Read the spec file
- If it does not already contain a backlink to today's daily note, insert `> Daily note: [[YYYY-MM-DD]]` immediately after the YAML frontmatter closing `---` delimiter (if present), with a blank line before the first heading. If no frontmatter exists, insert it as the first line of the file.
- Write the updated spec file

### 3c. Update TODO.md

1. Read `Vaults/Work/TODO.md`
2. Add all Suggested TODOs to the `## Backlog` section in a single edit:
   ```
   - [ ] Description ([[YYYY-MM-DD]])
   ```
3. Write the updated TODO.md once

### 3d. Update Obsidian Notes (Knowledge Base)

For each Knowledge Base Update:
1. Read the existing Note file (e.g., `Vaults/Work/Notes/Tailscale.md`).
2. Append the updates under a `## Updates (YYYY-MM-DD)` section at the end of the file. Each bullet should include the source reference and describe what changed:
   ```markdown
   ## Updates (YYYY-MM-DD)

   - PR huntresslabs/infra-aws#142 merged: migrated ACLs to tag-based access ([[YYYY-MM-DD]])
   - Decided in #sre-team: all new services must use tags instead of IP-based ACLs ([[YYYY-MM-DD]])
   - Research: Tailscale ACL syntax supports `autogroup:internet` for egress rules ([[YYYY-MM-DD]])
   ```
   If an `## Updates (YYYY-MM-DD)` section for today already exists, append to it instead of creating a duplicate.
3. Write the updated Note file.

### 3e. Create New Obsidian Notes

For each Suggested New Note:
1. Create the Note file at `Vaults/Work/Notes/<TopicName>.md`.
2. Write initial content with the updates that triggered its creation:
   ```markdown
   # <TopicName>

   ## Updates (YYYY-MM-DD)

   - Source and description of what happened ([[YYYY-MM-DD]])
   ```
3. Update the daily note's `## Suggested New Notes` section to show the created Note as a wiki link: `- Created [[TopicName]]`.

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

After writing all files, output a summary line:
> EOD summary written to `Daily notes/YYYY-MM-DD.md`. [N] TODOs added to TODO.md. [N] specs backlinked. [N] Notes updated. [N] Notes created.
