# User Instructions

## Development Workflow

For any non-trivial task (new features, bug fixes, refactors), follow this mandatory workflow using the superpowers skills:

1. **Brainstorm** — Invoke the `superpowers:brainstorming` skill before any creative or implementation work to explore intent, requirements, and design.
2. **Plan** — Invoke the `superpowers:writing-plans` skill to produce a written, step-by-step implementation plan before touching code.
3. **Worktree** — Invoke the `using-worktrunk` skill to create an isolated git worktree using `wt` before writing any files or making any changes.
4. **Implement** — Invoke the `superpowers:subagent-driven-development` skill to execute the plan, with each step following `superpowers:test-driven-development` (write tests first, then implementation).
5. **Self-review** — Invoke the `superpowers:requesting-code-review` skill when implementation is complete to verify work meets requirements before merging.
6. **PR** — Invoke the `superpowers:finishing-a-development-branch` skill and then the `pr` skill to push the branch and open a pull request.

This workflow is mandatory. Do not skip or reorder steps.

## Git Workflow

- Always create a new git branch before starting any code changes or writing any files. Name the branch descriptively based on the task (e.g., `feat/add-login-page`, `fix/null-pointer-error`). Do not make changes directly on the current branch unless explicitly instructed otherwise.
- Never commit directly to `main`. Always work on a separate branch and use a pull request workflow.

## Specs and Implementation Plans

- Always save **design specs** to `Vaults/Work/Specs/` and **implementation plans** to `Vaults/Work/Plans/` (relative to the workspace root at `~/code`).
- Use the template at `Vaults/Work/Templates/Specs.md` for specs and `Vaults/Work/Templates/Plans.md` for implementation plans. Name files with a `YYYY-MM-DD-` date prefix.
- This overrides the default save locations in the `superpowers:writing-plans` and `superpowers:brainstorming` skills (`docs/superpowers/plans/` and `docs/superpowers/specs/`).
- **Always link specs and plans together:**
  - When writing an implementation plan, set its `spec:` frontmatter field to a wikilink pointing to the associated spec (e.g. `spec: "[[2026-05-13-my-feature-design]]"`), then update the spec's `plans:` field to include a wikilink back to the new plan.
  - If the spec is written first (before a plan exists), leave `plans:` empty and fill it in once the plan is created.
  - When a PR is created as part of implementing a plan, add the PR URL to the plan's `prs:` frontmatter field.

## Authoring content

When drafting content on Luke's behalf (Slack messages, design specs, runbooks, docs), read `~/.claude/writing-voice.md` first and match his voice and structure.

## Tools

- Always use OpenTofu (not Terraform) and Helm for infrastructure as code.
- Always use uv for Python package management.
