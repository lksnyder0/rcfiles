---
name: sod
description: "Use when the user wants to start their day, generate a morning plan, or review overnight activity"
allowed-tools: Bash(python3 *), Bash(gh *), Bash(short *), Read, Edit, Glob, mcp__glean_claude-code__search
---

# Start-of-Day

Seed today's daily note with four sections: **IMPORTANT TODAY/THIS WEEK**, **OPEN COMMITMENTS**, **PR REVIEW BACKLOG**, **PROJECT WORK**.

Almost all of this is deterministic and lives in `sod.py`. Your only judgment call is deciding which Slack/Gmail phrase-search hits are real commitments. Everything else is a script invocation whose output goes into the note verbatim.

**Vault root:** `/Users/luke.snyder/code/Vaults/Work`
**Script:** `~/.claude/skills/sod/sod.py` (all commands below assume `python3 ~/.claude/skills/sod/sod.py`)

## What you must NOT do

- Never hand-write the PR REVIEW BACKLOG table, the IMPORTANT TODAY list, or any `Project Work/` note. All three are script output by design, so two runs with unchanged upstream state produce identical text.
- Never create or edit `Commitments/` notes directly. Use `commit-add`, which owns dedup and filenames.
- Never fall back to the Shortcut MCP tools. PROJECT WORK must come from `short api` or not at all — the MCP path is not reproducible.
- Never delegate Glean searches to a subagent. Subagents have fabricated Slack messages and incidents in the past. Call `mcp__glean_claude-code__search` yourself, in the main session.

## Step 1: Resolve the search window

```bash
python3 ~/.claude/skills/sod/sod.py window
```

Prints the cutoff date — the most recent daily note strictly before today, or yesterday on a first-ever run. Use it as `after` for every Glean search below. Call it `CUTOFF`.

## Step 2: Slack commitments

Run **one search per phrase** rather than reading the whole window's Slack activity. For each phrase, call `mcp__glean_claude-code__search` with:

- `query`: the phrase
- `app`: `slack`
- `from`: `me`
- `after`: `CUTOFF`

Phrases (case-insensitive substring match):

```
i'll, i will, i can take, i've got, i got it, let me take, let me handle,
i'm on it, will do, leave it with me, i'll follow up, i'll circle back,
i'll own, i'll pick that up, i'll get on it
```

Use the dedicated `app` / `from` / `after` parameters — do not embed them as keywords in `query`, which breaks Glean's faceted search.

**Only phrase hits are candidates.** Then judge each one. A real commitment is a promise of *future action by Luke*. Reject:

- Idiomatic false positives — "that will do", "will do nicely", "it'll do".
- Quoted or forwarded text where Luke is relaying someone else's words.
- Anything already completed inside the same thread.
- Results that look fabricated. A genuine Slack hit has a real channel id (e.g. `C03TRM93V0C`) and a real message permalink. Discard anything generic or placeholder-ish rather than writing it.

## Step 3: Training emails

Same pattern, one search per phrase, with `app: gmail` and `after: CUTOFF`:

```
training, certification, complete by, required course, assigned course,
compliance training, due by, deadline to complete, please complete
```

Judge which candidates are genuine assigned trainings. Reject newsletters, marketing, form receipts, and threads merely *discussing* training. For the ones that qualify: date assigned → `--committed-date`, date communicated in the email → `--due-date`.

## Step 4: Write each commitment

One call per surviving commitment, Slack and email alike — they share one Base and one schema:

```bash
python3 ~/.claude/skills/sod/sod.py commit-add \
  --title "Send Connor the Elastic user info" \
  --summary "Promised in DM to send the Elastic user list by EOD." \
  --link "https://huntress.slack.com/archives/C03TRM93V0C/p1757894400123456" \
  --committed-date 2026-09-14 \
  --due-date 2026-09-16 \
  --complexity low \
  --tags elasticsearch,idex
```

`--link` is the Slack permalink or Gmail message URL and is the row key. The script prints `created`, `updated`, or `duplicate`:

- `duplicate` — same permalink already recorded (a same-day re-run). Nothing written.
- `updated` — a similar open commitment exists under a different permalink, so this is a cross-day restatement; only `due_date` was refreshed.
- `created` — new row.

Report the counts. Do not re-litigate the script's decision.

`--due-date` is optional: omit it when no date was communicated. Undated commitments still surface, in the no-due-date tier.

### Complexity rubric

Apply it literally, so estimates stay consistent run to run:

- **low** — under ~30 minutes, no dependencies: a quick reply, a single message, forwarding something.
- **medium** — a few hours up to a day; may need to check existing docs or one other person, but the scope is clear.
- **high** — more than a day, spans multiple sessions, needs coordinating across people or teams, or the scope itself is still unclear and needs investigation first.

## Step 5: Regenerate and render

In this exact order:

```bash
python3 ~/.claude/skills/sod/sod.py project-work
python3 ~/.claude/skills/sod/sod.py commitments
python3 ~/.claude/skills/sod/sod.py daily-note
```

Order matters: `commitments` recomputes `sort_key` across everything `commit-add` just wrote, and `daily-note` reads both Bases to rank IMPORTANT TODAY/THIS WEEK.

- `project-work` fully regenerates `Project Work/` from Shortcut. Closed or reassigned stories, and epics left with no qualifying story, disappear on their own.
- `commitments` recomputes ordering over `status: open` notes. `waiting` and `done` entries stay on disk, excluded from ranking until moved back to `open`.
- `daily-note` writes only the four SOD sections. Anything else in the note — including sections `eod` added — is left alone, so re-running mid-day is safe.

## Degradation

Each source fails independently. Note what was unavailable in your summary and continue:

- `gh` fails → the PR table renders its placeholder; the rest of the run proceeds.
- `short api` fails → say so and skip `project-work`. Do **not** substitute the Shortcut MCP.
- Glean returns nothing → no new commitments; both Bases still regenerate.

## Completion

Report:

- the daily note path
- commitment counts as `N created, N updated, N duplicate`
- epic and story counts from `project-work`
- PR row count
- any source that was unavailable

## How the sections work

Useful when something looks wrong:

| Section | Mechanism |
|---|---|
| IMPORTANT TODAY/THIS WEEK | Script-rendered. Merges open commitments and PROJECT WORK **stories only** (never epics) — `important_pool()`'s only two sources. Four bands: **overdue** (any source) → **started** stories by closest due date → **unstarted** stories by complexity → **everything else** by `due_date asc, complexity asc`. `backlog` stories are excluded entirely. Top 5. |
| OPEN COMMITMENTS | Base embed, `![[Commitments.base#Daily Note View]]`. Filters `status == "open"`, sorts by `sort_key` alone. Mark one done by toggling `status` to `done` inline in the Base — no script needed. |
| PR REVIEW BACKLOG | Script-rendered from four `gh` criteria: assigned to me, review-requested for `huntresslabs/infrastructure-sre`, review-requested for `huntresslabs/idex`, and every open PR in `huntresslabs/infra-elastic`. Deduped by repo + number, sorted oldest-first. Drafts are excluded except when assigned directly to me. |
| PROJECT WORK | Base embed, `![[Project Work.base#Daily Note View]]`. Grouped by epic, sorted by `sort_key` alone. Within an epic, stories that block another story render first. |

Both Bases sort by a precomputed integer `sort_key` because Obsidian Bases cannot express "partition into tiers, then sort within each tier". All tiering logic lives in `sod.py`.

The banding exists because Shortcut estimates and deadlines are mostly unset in practice: ranking undated stories on `due_date`/`complexity` alone collapses to story id. Overdue still wins outright from any source, so nothing you promised can be buried. Inside bands 2 and 3, `due_date` and `complexity` still order the work — if estimates get filled in later they take effect automatically, no change needed.

`backlog` stories are dropped because they need shaping before they can be finished. A story with a missing or unrecognised state type is **not** dropped — it lands in band 3 behind real unstarted work. Band membership reads the workflow state `type`, never the name, same as the done-check.

Self-directed tasks are now created directly via the `todo` skill / `sod.py todo-add` — there is no `TODO.md` left to migrate items out of.

## Tests

```bash
cd ~/.claude/skills/sod && python3 -m unittest test_sod -v
```

Stdlib `unittest`, no dependencies. Run it after touching `sod.py`.
