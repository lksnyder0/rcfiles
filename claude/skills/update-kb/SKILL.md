---
name: update-kb
description: Use when a decision is made about software selection, implementation approach, system architecture, or configuration. Also use when the user explicitly asks to update the knowledge base. Triggers for: choosing a tool/service for a purpose, selecting one approach over alternatives, defining or changing how systems connect, or setting configuration patterns. Do NOT trigger for ephemeral debugging steps, temporary workarounds, or in-progress exploration that hasn't reached a decision.
---

# Update Knowledge Base

Update the Obsidian knowledge base at `Vaults/Work/Notes/` with decisions made during this conversation. Handles software selection, implementation approaches, architecture changes, and configuration decisions. Maintains both topic notes and dedicated architecture notes.

## Step 0: Announce (Proactive Trigger Only)

If this skill was triggered proactively (not via explicit `/update-kb` invocation), announce what was detected before doing any work:

> "I noticed a decision about [topic] — let me draft a KB update."

Wait for the user to acknowledge or say "skip it" before proceeding. If the user skips, stop here.

## Step 1: Classify the Decision

Determine the following from the conversation context (or from `/update-kb` arguments if invoked explicitly):

- **Decision type:** one of: tool/service selection, implementation approach, architecture change, configuration decision
- **Topic:** the subject (e.g., "Tailscale", "Elasticsearch", "Detection Engine")
- **Summary:** one-line description of what was decided
- **Alternatives considered:** if the conversation discussed other options, capture them
- **PR/issue links:** if any were mentioned in conversation, note them

## Step 2: Check for Existing Notes

Search `Vaults/Work/Notes/` for existing files:

1. Use Glob to find a topic note matching the subject: `Vaults/Work/Notes/<Topic>.md`
   - Try exact match first, then case-insensitive search
   - Check for common variations (e.g., "PostgreSQL" vs "Postgres", "K8s" vs "Kubernetes")
2. If the decision is architecture-related, also search for `Vaults/Work/Notes/<Topic> Architecture.md`
3. Read any existing files fully using the Read tool — understand the current structure, sections, and content to avoid duplication and to place new content correctly

## Step 3: Draft the Update

Based on what exists, draft the changes. Follow the content conventions below strictly.

### If the topic note exists

- Read the full note and understand its structure
- Place new content in the most appropriate existing section
- Create a new `##` section only if no existing section fits
- Always add or append to the `## Updates (YYYY-MM-DD)` section at the bottom
- Do NOT duplicate information already present in the note

### If the topic note does not exist

Create a new file at `Vaults/Work/Notes/<Topic>.md` with this structure:

```
<Topic> - <one-line purpose>

<decision content>

## Updates (YYYY-MM-DD)

- <one-line summary of the decision> ([[YYYY-MM-DD]])
```

### If architecture decision + no architecture note exists

Create `Vaults/Work/Notes/<Topic> Architecture.md` with:

- Description of the current system state: components, connections, data flows
- Mermaid diagram if the architecture is complex, multi-step, or multi-system
- Links back to the topic note: `See [[<Topic>]] for usage decisions and update history.`

Also add a `[[<Topic> Architecture]]` wikilink in the topic note.

### If architecture decision + architecture note exists

- Read the existing architecture note fully
- Update it in place to reflect the current state — do not append history
- Update or add Mermaid diagrams if the architecture change affects component relationships

## Content Conventions

Follow these rules for all content written to the knowledge base:

### Topic Notes

- Concise, factual tone — no fluff, assumes reader has context
- Use wikilinks for cross-references: `[[Tailscale Architecture]]`, `[[Kubernetes]]`
- Use inline code for commands, config keys, technical terms
- Use tables for comparisons when documenting alternatives considered
- Dates in ISO format inside double brackets: `[[2026-04-20]]`
- If PR/issue links are available: `[repo#123](url)`
- No frontmatter unless aliases are needed
- No bold/italic for emphasis
- No lengthy prose — keep it scannable

### Architecture Notes

- Named `<Topic> Architecture.md`
- Describe the current state only — not history
- Use Mermaid diagrams when describing complex, multi-step, or multi-system architecture
- Living document — update in place, do not append history
- Link back to the topic note and related architecture notes
- History of changes belongs in the topic note's Updates section

### Updates Section Format

```
## Updates (YYYY-MM-DD)

- <description> — [repo#N](url) ([[YYYY-MM-DD]])
- <description> ([[YYYY-MM-DD]])
```

If an Updates section already exists with a different date in the heading, add a new entry to the existing section. Do not create a second Updates heading.

## Step 4: Present the Draft

Show the user exactly what will be written or changed:

- **For existing files:** show the specific additions/changes in context, clearly marking what is new
- **For new files:** show the full file content

Present the draft and explicitly ask: "Does this look right? I'll write it on your approval."

Do NOT write anything until the user approves. If the user requests modifications, revise the draft and present again.

## Step 5: Write on Approval

Once the user approves:

- Use Edit for existing files (to modify specific sections)
- Use Write for new files
- Do NOT git commit — these are personal vault files outside of version control
- Confirm what was written: "Updated `<filename>` with <brief description>."

## What This Skill Should NOT Do

- Add frontmatter unless aliases are needed
- Use bold/italic for emphasis
- Write lengthy prose
- Duplicate information already in a note
- Git commit vault files
- Trigger for non-decisions (debugging, exploration, temporary workarounds)
- Proceed without user approval of the draft
