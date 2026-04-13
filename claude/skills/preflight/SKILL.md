---
name: preflight
description: Run blocking pre-work checks before starting implementation — verifies git repo, worktree state, branch lineage from main, and clean working tree
---

# Preflight Checks

Run these four checks in sequence before starting any implementation work. If ANY check fails, STOP and report the failure. Do NOT proceed with implementation until all checks pass.

**Announce at start:** "Running preflight checks..."

## Check 1: Working Directory

Run:
```bash
git rev-parse --is-inside-work-tree
```

- If this fails, STOP: "Not inside a git repository. Navigate to the correct repo before proceeding."

## Check 2: Worktree Awareness

Run:
```bash
git worktree list
git rev-parse --show-toplevel
```

- Report the current worktree path and whether this is the main working tree or a linked worktree.
- If inside a linked worktree, report which branch it's on and ask the user to confirm this is the intended worktree.
- If the user says it's wrong, STOP: "Wrong worktree. Switch to the correct one before proceeding."

## Check 3: Branch Lineage

Run:
```bash
CURRENT=$(git branch --show-current)
# Determine default branch
DEFAULT=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
# Fetch latest to avoid stale refs
git fetch origin "$DEFAULT" --quiet 2>/dev/null || true
```

- If `$CURRENT` equals `$DEFAULT` (e.g., on `main`), this check PASSES — the user is about to create a branch.
- If on a feature branch, run:
  ```bash
  MERGE_BASE=$(git merge-base HEAD "origin/$DEFAULT")
  DEFAULT_TIP=$(git rev-parse "origin/$DEFAULT")
  ```
  - If `$MERGE_BASE` equals `$DEFAULT_TIP`, PASS — branch is cut from current tip of the default branch.
  - If they differ, STOP: "Branch `$CURRENT` diverges from `$DEFAULT`. Merge-base is `$MERGE_BASE` but `$DEFAULT` tip is `$DEFAULT_TIP`. Rebase onto `$DEFAULT` or create a fresh branch."

## Check 4: Clean State

Run:
```bash
git status --porcelain
```

- If output is empty, PASS.
- If there are uncommitted changes, STOP: "Uncommitted changes detected:" followed by the list of dirty files. "Commit, stash, or discard these changes before proceeding."

## Output

After all four checks pass, print a summary:

```
Preflight checks passed:
  Repo:     <repo name from basename of toplevel>
  Branch:   <current branch>
  Base:     <default branch> (up to date)
  Worktree: <main | linked at /path/to/worktree>
  State:    clean
```

Then proceed with the requested work.
