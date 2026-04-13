---
name: using-worktrunk
description: Use when setting up isolated workspaces for feature work, before executing implementation plans - replaces raw git worktree commands with the worktrunk (wt) CLI
---

# Using Worktrunk (`wt`)

## Overview

Worktrunk (`wt`) manages git worktrees with branch-name addressing, automated hooks, and built-in merge workflows. **Use `wt` instead of raw `git worktree` commands.**

**Announce at start:** "I'm using the using-worktrunk skill to set up an isolated workspace."

## Quick Reference

| Task | Command |
|------|---------|
| Create worktree + branch | `wt switch --create <branch> -y` |
| Create from non-default base | `wt switch --create <branch> --base <base> -y` |
| Switch to existing worktree | `wt switch <branch>` |
| Switch to previous worktree | `wt switch -` |
| Switch to default branch | `wt switch ^` |
| Check out a PR | `wt switch pr:<number>` |
| List all worktrees | `wt list` |
| List with CI status + summaries | `wt list --full` |
| Merge to default branch | `wt merge -y` |
| Merge to specific branch | `wt merge <target> -y` |
| Merge without squashing | `wt merge --no-squash -y` |
| Remove current worktree | `wt remove -y` |
| Remove specific worktree | `wt remove <branch> -y` |
| Force-remove unmerged | `wt remove <branch> -D -y` |

**Always use `-y` flag** in automation to skip interactive prompts.

## Creating a Worktree (replaces `git worktree add`)

```bash
# CORRECT - creates worktree AND branch, switches to it
wt switch --create feat/add-user-auth -y

# With a non-default base branch
wt switch --create hotfix/login --base production -y

# WRONG - these subcommands do not exist:
# wt add, wt create, wt new
```

`wt switch --create` does everything:
1. Creates the branch from base (default branch unless `--base` specified)
2. Creates the worktree at the configured path
3. Runs post-create hooks (dependency install, etc.)
4. Changes directory to the new worktree

**No manual setup needed** — hooks handle `npm install`, `pip install`, etc.

## Merging Back (replaces manual git merge + cleanup)

```bash
# Squash-merge to default branch, remove worktree, delete branch
wt merge -y
```

`wt merge` does everything in one command:
1. Squashes all commits into one
2. Rebases onto target if behind
3. Runs pre-merge hooks (tests, lint)
4. Fast-forward merges to target
5. Removes worktree and deletes branch

**Do NOT manually:**
- `git merge` or `git rebase`
- `git branch -d`
- `git worktree remove`
- `git worktree prune`

Use `--no-squash` to preserve individual commits. Use `--no-remove` to keep the worktree after merge.

## Removing Without Merging

```bash
# Remove current worktree (deletes branch if merged)
wt remove -y

# Remove specific worktree
wt remove feat/abandoned-feature -y

# Force-delete unmerged branch
wt remove feat/experimental -D -y
```

`wt remove` automatically deletes the branch if it's been merged. No need for `git branch -d` or `git worktree prune`.

## Shortcuts

| Shortcut | Meaning |
|----------|---------|
| `^` | Default branch (main/master) |
| `-` | Previous worktree (like `cd -`) |
| `@` | Current branch/worktree |
| `pr:123` | GitHub PR #123's branch |

## Workflow Integration

This skill replaces `superpowers:using-git-worktrees` in the development workflow:

1. **Brainstorm** -> **Plan** -> **Create worktree:**
   ```bash
   wt switch --create feat/my-feature -y
   ```
2. **Implement** (TDD, subagent-driven)
3. **Self-review** -> **Finish:**
   - If merging locally: `wt merge -y`
   - If PR workflow: push branch, create PR, then `wt switch ^` (back to default branch) and `wt remove <branch> -y` after merge

**Called by:**
- **brainstorming** (Phase 4) — when design is approved
- **subagent-driven-development** — before executing tasks
- **executing-plans** — before executing tasks

**Pairs with:**
- **finishing-a-development-branch** — for cleanup after work complete

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `wt add` | Use `wt switch --create` |
| Using `wt create`, `wt new`, or `wt exit` | These don't exist. Use `wt switch --create` / `wt switch ^` |
| Manual `git branch -d` after merge | `wt merge` or `wt remove` handles this |
| Manual `git worktree remove/prune` | `wt remove` handles this |
| Forgetting `-y` in automation | Always pass `-y` to skip prompts |
| Using raw `git worktree add` | Use `wt switch --create` |
| Manual `npm install` in worktree | Configure post-create hook instead |

## Red Flags — STOP

- About to run `git worktree add` → Use `wt switch --create` instead
- About to run `git worktree remove` → Use `wt remove` instead
- About to run `git branch -d` after worktree work → `wt merge`/`wt remove` handles this
- Manually running package install in new worktree → Configure a hook
