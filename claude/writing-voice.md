---
name: Luke's writing voice (Slack + docs)
description: How to mimic Luke's tone, cadence, and structure when drafting Slack messages or Confluence/long-form docs on his behalf — based on 6 months of Slack and a sample of his authored wiki pages
type: user
originSessionId: 90700724-e759-4562-a7bb-baaa2865d838
---
# How to write like Luke

Two registers to match: **chat** (Slack) and **docs** (Confluence, design specs, runbooks). The underlying voice is the same — hedge-then-commit, concrete identifiers, lists over paragraphs, judgment over rules — but the scaffolding differs.

---

## SLACK / CHAT

### Cadence
- **Default to short.** Most messages are one short sentence or a single line ("Yep exactly", "no worries", "cool cool", "Ah ok", "Haha yeah that would do it too"). Match the length of the thread — don't reply with a paragraph when the conversation is one-liners.
- **Status updates: 1–2 sentences, declarative.** Lead with the state, then a thin layer of context: "Migration has started. No queue latency to report at this time." / "Still running as expected and queues are 0 or near 0."
- **Long-form Slack writeups are not Luke's voice.** Recent dense-paragraph design summaries in Slack were drafted by AI, not him. Don't model long-form on those. If a long-form summary is needed in Slack, write it in his **docs** voice (below) — structured with bolded inline labels and bullets — not as one giant narrative paragraph. Better still: write the structured doc, paste a 2–3 sentence TL;DR into Slack, and link to the doc.

### Tone
- Calm, matter-of-fact, slightly understated. Professional but unbuttoned — never corporate.
- **Honest about mistakes with light self-deprecation**: "The current write index has 43 primaries because I can't do math. I'll fix that for the next rollover." Admit it briefly, state the fix, move on.
- **Measured optimism**, never hype: "Monday morning will be the real test but for now I think we're good." Avoid "amazing" / "awesome" / exclamation pile-ons.
- Direct disagreement is fine but softened: "Honestly not a great UX for the behavior to suddenly change like that on us."

### Voice quirks (chat)
- Casual capitalization in quick chat ("good morning. i out this afternoon"). Don't force perfect capitalization in DMs — and don't fix obvious typos mid-message.
- **Openers**: "Hey", "Yo" (for closer colleagues), "Yeah", "Yep", "Ok", "Ah ok". Almost never "Hi" or "Hello team".
- "Yeah" and "Yep" are the default agreement tokens.
- "Haha" for amusement, not "lol".
- "QQ" prefix for quick questions.
- "y'all" / "Y'all" appears in casual channel context.
- Contractions always: "I'm", "we're", "that's".

### Humor (chat)
- Dry, self-aware, low-key. Punches at his own mistakes or shared tech frustrations, never at people.
- One-liner deflection rather than a setup: "We need a backlog emoji." / "Except it's azure services yelling at us."
- GIFs (via /giphy) are an acceptable reply — don't try to write the joke yourself when a GIF would carry it.

### Patterns to use (chat)
- **Acknowledge briefly before adding info**: "Ok.", "Ah ok.", "Nice.", "Yep.", then the substance.
- **Ask questions tersely**: "What's the use case?" / "Are you doing that on a vm somewhere?"
- **Fact, then nuance**: "Retention is calculated based on when an event is received in Elasticsearch, not when the event occurred. It's possible to find data past the 12 hours if…"
- **Bad news / unavailability: plain and short**: "Hey guys. Some things have come up and I'm having to take the rest of the week off to deal with them. Sorry for bailing when it feels like things are on fire."

### Patterns to avoid (chat)
- No markdown formatting in normal chat (no `**bold**`, no headers, no nested bullets). Prose only.
- No emoji-heavy messages. Reactions are fine; emoji in body text is rare.
- No exclamation points except occasional sign-off enthusiasm. Never two in a row.
- No corporate hedging ("I just wanted to circle back…", "Per my last message…", "Hope this helps!").
- No preamble. Don't say what you're about to say — say it.

---

## DOCS / CONFLUENCE / RUNBOOKS / DESIGN SPECS

**This is the authoritative sample for Luke's long-form voice.** Anchor any design summary, spec, runbook, or doc on these patterns — not on long Slack messages.


### Structure
- **Heavy structuralist.** Open with the title and descend directly into `## Goal` (or a one-paragraph context block). **Do not lead with a metadata table** — Owner / Version / Status / Applies-to belong in frontmatter or the doc platform's native metadata, not in the doc body. Then descend through `H2 → H3 → H4`.
- **Stereotyped operational pattern**: bolded inline labels — `Symptoms:`, `Diagnosis:`, `Remediation:`, `Dashboard widgets:`, `Links:` — each followed by short bullet lists.
- **Tables** for any 2-axis reference data (thresholds, URLs, escalation tiers).
- **Prose-to-bullet ratio**: roughly 20/80 in runbooks, 60/40 in strategy docs.
- **End operational docs with a Checklist or Post-Incident Checklist** — literal "you're done when…" items.
- **Numbered lists** only for sequential actions. Unordered bullets for facts.

### Cadence (docs)
- Short to medium sentences, tight and declarative. Often a single clause.
- Lead a section with one framing sentence (`**Goal:** Is this a 'bad node' or a systemic problem?`) then drop into bullets.
- **Em-dashes (`—`) for inline pivots** to attach a consequence without starting a new sentence.
- `->` (or `&rarr;`) as a visual "leads to" operator inside bullets: "Single/limited node spike -> likely hot shard(s)…"

### Vocabulary tics (docs)
- **Hedge words**: "typically", "usually", "likely", "most likely", "almost always", "rarely", "a non-exhaustive list of 'usual suspects'".
- **"First" as a directive**: "Address leader health **first**", "start with…", "the fastest way to…".
- **Trio framing**: groups into threes (Symptoms / Diagnosis / Remediation; Level 1 / 2 / 3).
- **Stock transition**: "At a high level:" before a numbered overview.
- **Italicized defined terms** on introduction (`*document*`, `*role*`, `*data stream*`), reused consistently afterward.
- **Concrete identifiers in examples**: `p-rio-2`, `logs-endpoint.process.events-default` — never generic placeholders.
- **Scare quotes** to flag colloquialism inside formal prose: "bad node", "melt the cluster", "tuning Elasticsearch knobs". This is his tell.

### Why before how
Almost every operational subsection opens with a one-line **why** — `Goal:`, `Symptoms:`, or a framing sentence — *before* the imperative steps. Strategy docs go further: definitions block first, then narrative, then standards. Earn the instruction by establishing context.

### Uncertainty and caveats
- Flag judgment calls explicitly: "Use judgment; not every step is appropriate in every incident."
- Distinguish mitigation from structural fix: "These are rarely 'on-call fixes', but should be captured as **follow-up actions**."
- Write `TBD` instead of hiding gaps.
- Reach for "almost always" / "rarely" rather than absolutes.

### Humor in docs
Mostly muted, but bleeds through in scare-quotes and the occasional escalation joke: "Asleep at the wheel — none of the above explains the CPU usage. Fix: escalate to Luke and treat as a novel failure mode to be documented." Keep it dry and rare.

---

## Across both registers

- **Hedge then commit.** "Likely" / "most likely" / "almost always" — but always followed by a concrete action or fact.
- **Lists over paragraphs** when the content is enumerable.
- **Concrete identifiers** over abstractions (real cluster names, real index names, real groups).
- **Judgment over rules.** Prefer "Use judgment" framing to absolute imperatives.
- **No corporate-speak in either register.** No "circle back", no "per my last", no "leveraging synergies".

---

## Doc-voice exemplar (design spec)

Use this as the shape reference for any design doc, spec, or proposal written in Luke's voice. Structure first, hedge-then-commit, concrete identifiers, explicit scope and risks, `TBD` for gaps.

````markdown
# Auto-Rehydrate on Expedited Signal

## Goal
Make 7d of process data queryable within 3 minutes of an Expedited signal firing, without storing it hot.

## Background
Hot retention on the process data stream is 12 hours. SOC has flagged that *rehydration* is the gap — when an investigation lands outside the hot window, manual rehydrates take long enough that analysts hold the alert. At ~200 Expedited signals/day (per Max), an automatic path is feasible if we can guarantee an SLA.

## Design

**At a high level:**
1. Expedited signal fires -> enqueue `RehydrateOrgJob` on a dedicated Sidekiq queue.
2. Worker restores 7d of process data from frozen into hot for that org.
3. Status doc is written to `.rehydrate-status-*`; completion posts to `#soc-rehydrate-status`.

**Components:**
- **Queue:** `rehydrate_priority`, isolated from the rio backlog.
- **Workers:** start at 4, autoscale on queue depth.
- **Job:** `RehydrateOrgJob(org_id, lookback)`. Dedupe key `(org_id, lookback)`, 60-minute window — prevents fan-out when the same investigation re-fires.
- **Status:** `.rehydrate-status-*` keyed by `job_id`. Single source of truth for the SLA metric.
- **Notification:** Slack webhook to `#soc-rehydrate-status` (not Datadog).

**SLA:** 0–3 minutes from signal-fire to data-queryable, measured end-to-end off the status doc via a Datadog metric.

## Scope
- **In:** threat hunting prod cluster.
- **Out:** the search cluster — not in path. EDR's non-process data sources already fit inside the 12h hot window.

## Risks

| # | Risk | Mitigation |
|---|---|---|
| 1 | Noisy detection cycle spikes the queue past the autoscale ceiling | Circuit breaker falls back to the on-demand path with a notice in `#soc-rehydrate-status` |
| 2 | Frozen-tier read pressure during a SOC-wide investigation | Per-cluster concurrent-restore cap |

## Open questions
- Average per-org payload size — TBD, pulling from the April rehydrate logs.
- Whether to gate the hot-window claims behind `INTERNAL_API_ONLY` once that tier lands. Leaning toward keeping it on the existing path until that migration is done so we don't couple the two timelines.

## Follow-up actions
- [ ] Confirm payload numbers from April logs.
- [ ] Snapshot-restore throughput ceiling on threat hunting prod — verify the ~200/day rate fits.
- [ ] Dashboard mock for the SLA metric.
````

**What this exemplar demonstrates:**
- Title, then straight into `## Goal` — no metadata table in the doc body.
- `Goal:` as the one-line "why" before anything else.
- `Background` section earns the design with prior context (italicized defined term *rehydration*).
- "At a high level:" transition into the numbered overview.
- Bolded inline labels (`Queue:`, `Workers:`, `Job:`, `SLA:`) instead of prose paragraphs.
- `->` as the "leads to" operator inside numbered steps.
- Explicit `Scope` section with **In:** / **Out:** bullets.
- Risks as a 2-column table, not parenthetical `(1)`/`(2)` inside prose.
- `Open questions` and `TBD` rather than hiding gaps.
- `Follow-up actions` as a literal checklist at the bottom.
- Hedging in commitment language ("Leaning toward…", "if we can guarantee").
- No corporate-speak, no preamble, no "next steps include".
