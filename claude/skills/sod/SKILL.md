---
name: sod
description: "Use when the user wants to start their day, generate a morning plan, or review overnight activity"
allowed-tools: Bash(gh *), Glob, Read, Write, Edit, mcp__glean_claude-code__search
---

# Start-of-Day Plan

Generate a prioritized daily plan and seed the day's Obsidian daily note by gathering overnight incidents, meetings, open PR reviews, Slack requests, and carryover TODOs. Present a draft for review, then write the daily note.

**Vault root:** `/Users/luke.snyder/code/Vaults/Work`
**Daily note path:** `Daily notes/YYYY/MM-<Month>/YYYY-MM-DD.md` (use today's date, e.g., `Daily notes/2026/03-March/2026-03-31.md`)
**TODO.md path:** `TODO.md` (relative to vault root)

## Step 0: Determine Time Window

Find the most recent daily note to establish the "overnight" cutoff:

1. Use Glob to find all daily note files: `/Users/luke.snyder/code/Vaults/Work/Daily notes/**/*.md`
2. Parse filenames to extract dates (format: `YYYY-MM-DD.md`). Sort descending.
3. The most recent date is the cutoff. All data sources search for activity after this date.
4. If no daily notes exist, default to yesterday's date.
5. Record the cutoff date for use in all subsequent steps.

## Step 1: Gather Data

Gather data from all sources in parallel. Each source is independent — if one fails, note it and continue with the others.

### 1a. Overnight Incidents (Glean -> Slack #incidents)

Call `mcp__glean_claude-code__search` with query: `app:slack channel:#incidents after:CUTOFF_DATE`

Parse the structured incident message format:
- Severity (SEV-1 through SEV-4)
- Title/description from "New Incident:" line
- Reporter from "Reporter:" line
- Affected Services from "Affected Services:" line
- Status from "Status:" line (Investigating, Resolved, Monitoring, etc.)
- Description from "Description:" line
- Dedicated incident channel (#tmp-incident-*)

After retrieving results, filter out any incidents where the Status field is "Resolved" — only include active/investigating incidents. Sort by severity (SEV-1 first).

If unavailable: record `"Incidents: unavailable"` and continue.

### 1b. Meetings Today (Glean -> Google Calendar)

Call `mcp__glean_claude-code__search` with query: `app:calendar updated:today`

For each event, record:
- Start time (24h format)
- Meeting title
- Key attendees (if available)
- Whether the user is the organizer or presenter

Sort chronologically.

If unavailable: record `"Calendar: unavailable"` and continue.

### 1c. Open PR Reviews (GitHub CLI)

Run these `gh` commands (scoped to `huntresslabs` org):

1. PRs where review is requested:
   ```bash
   gh search prs --review-requested @me --state open --owner huntresslabs --json number,title,repository,url,createdAt --limit 50
   ```

2. PRs authored by user still open:
   ```bash
   gh search prs --author @me --state open --owner huntresslabs --json number,title,repository,url,createdAt --limit 50
   ```

Categorize:
- **Review requested**: PRs where your review is blocking someone else
- **Your open PRs**: PRs you authored that are still open (informational)

If `gh` errors or is unavailable, record: `"GitHub: unavailable"` and continue.

### 1d. Slack Requests (Glean -> Slack)

Call `mcp__glean_claude-code__search` with query: `app:slack to:"Luke Snyder" after:CUTOFF_DATE`

Also search: `app:slack @luke after:CUTOFF_DATE`

Scan for request patterns: "can you", "could you", "would you mind", "do you know", action items.

For each relevant result:
- Record the channel or DM context
- Summarize the request in one line

Filter out outbound-only channels.

If unavailable: record `"Slack: unavailable"` and continue.

### 1e. Overnight Emails (Glean -> Gmail)

Call `mcp__glean_claude-code__search` with query: `app:gmail after:CUTOFF_DATE` and `type` set to `email`.

For each email, record:
- Subject line
- Sender
- Whether the user is in the To or CC field
- One-line summary of the content

Filter to emails that likely need a response or action:
- Direct emails to the user (not just CC'd on a thread)
- Emails containing questions, requests, or action items directed at the user
- Emails from managers, stakeholders, or cross-team contacts

Exclude:
- Automated notifications (JIRA, GitHub, PagerDuty, etc. — these are covered by other sources)
- Mailing list digests where no action is needed
- Newsletters and marketing emails

If unavailable or no relevant results: record `"Email: unavailable"` and continue.

### 1f. TODO.md

1. Read `Vaults/Work/TODO.md`
2. Extract items from:
   - `## Today` — highest priority
   - `## Backlog` — surfaced only if Today is light (fewer than 3 items)
   - `## Waiting` — informational only, not actionable
3. Preserve full markdown including wiki links and tags.

### 1g. Previous Daily Note Carryover

1. Read the most recent daily note (identified in Step 0).
2. Extract all unchecked `- [ ]` items from any section.
3. Record the item text and originating section for each.

### All Sources Check

If ALL data sources returned unavailable or empty results (no incidents, no calendar events, no PRs, no Slack requests, no emails, TODO.md is empty, and no carryover items), report to the user:
> "All data sources returned empty or unavailable. Nothing to plan today."

Stop here — do not proceed to synthesis.

## Step 2: Synthesize & Prioritize

### Deduplication

Items appearing in multiple sources are shown once with combined context (e.g., a TODO.md item that matches an open PR is shown once with both contexts noted).

### Priority Order (fixed)

1. **Active incidents** — unresolved from overnight
2. **PR reviews requested** — blocking someone else
3. **TODO.md Today items** — already flagged as important
4. **Open Slack requests** — commitments/questions directed at user
5. **Emails needing response** — overnight emails requiring action
6. **Unchecked items from previous daily note** — carryover
7. **TODO.md Backlog items** — only if Today has fewer than 3 items

Within each tier, preserve original ordering.

### Item Format

One-line with source context in parentheses:
- `SEV-3 incident: Session Redis migration — Investigating — #tmp-incident-channel (incident)`
- `Review PR: huntresslabs/infra-k8s#529 — Tailscale K8s operator (PR review)`
- `Expand on Tailscale Initial Deployment Epic (TODO: Today)`
- `@jane asked about deployment process in #sre-team (Slack)`
- `Reply to @john.stotler re: Tailscale rollout timeline (email)`
- `Add failure stream alert (carryover from [[2026-03-30]])`

### Your Open PRs

Listed separately as informational, not action items.

## Step 3: Present Draft for Review

Assemble and present in terminal, formatted exactly as it will be written to the daily note.

Draft sections (omit any section that has no data):

```
## Plan
- [ ] Priority 1 item (source context)
- [ ] Priority 2 item (source context)

## Your Open PRs
- [repo#number](url) — title — status

## Incidents
- :large_red_circle: SEV-1: Title — Status — #tmp-incident-channel
- :large_orange_circle: SEV-2: Title — Status — #tmp-incident-channel
- :large_yellow_circle: SEV-3: Title — Status — #tmp-incident-channel
- :large_green_circle: SEV-4: Title — Status — #tmp-incident-channel

## Meetings
### HH:MM — Meeting Title
- Agenda:  ← only include if user is the organizer or presenter
- Notes:
- Action items:
```

**Section purposes:**
- `## Plan` is the prioritized action list — incidents appear here as action items (e.g., "SEV-3 incident: Title (incident)")
- `## Incidents` is a reference section with full structured details (severity, status, channel link) — supplements the plan item, not a duplicate
- `## Your Open PRs` is informational only — these are NOT in the plan unless they need action (rebasing, review comments)
- `## Meetings` provides scaffolding for note-taking throughout the day

If any data sources were unavailable, note this at the top:
> **Note:** The following sources were unavailable: [list]. Data from these sources is not included.

Present the draft, then immediately proceed to Step 4 — do not wait for user approval. The user will review the daily note in Obsidian and make manual edits if needed.

## Step 4: Write Output

### 4a. Create or Seed the Daily Note

**Path:** `/Users/luke.snyder/code/Vaults/Work/Daily notes/YYYY/MM-<Month>/YYYY-MM-DD.md` (e.g., `Daily notes/2026/03-March/2026-03-31.md`). Create parent directories if they don't exist.

- If the file does not exist, create it with the draft content.
- If the file already exists and already contains a `## Plan` section (from a previous SOD run today), replace the existing Plan, Incidents, and Meetings sections with the new content.
- If the file already exists without a `## Plan` section, merge the new content:
  - For each section (`## Plan`, `## Incidents`, `## Meetings`, etc.):
    - If the section heading already exists in the file, append new items below existing items in that section.
    - If the section heading does not exist, add the section at the appropriate position in the file.
  - Never overwrite or remove existing content.

### Obsidian Formatting Conventions

Use these conventions throughout all written content:
- Wiki links for cross-references: `[[YYYY-MM-DD]]`
- Checkbox syntax: `- [ ]` for open, `- [x]` for completed
- PR links: `[repo#number](url)`
- Shortcut story links as URLs: `[SC-12345](https://app.shortcut.com/huntress/story/12345)`
- Note links: `[[Tailscale]]`, `[[elasticsearch]]`, etc.
- Meeting times in 24h format: `10:00 — Meeting title`
- Incident severity: emoji prefix matching Slack conventions
  - `:large_red_circle:` SEV-1
  - `:large_orange_circle:` SEV-2
  - `:large_yellow_circle:` SEV-3
  - `:large_green_circle:` SEV-4

### Completion

After writing all files, confirm to the user:
> "Morning plan written to `Daily notes/YYYY-MM-DD.md`. [N] plan items, [N] meetings scaffolded."
