---
name: huntress:commit
description: Create a git commit. Use this skill whenever you need to commit code changes.
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git commit:*)
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, prepare and create a git commit.

### Steps

1. Stage the relevant files using `git add` (prefer adding specific files by name rather than `git add -A` or `git add .`).
2. Analyze all staged changes and draft a commit message:
   - Use [Conventional Commits](https://www.conventionalcommits.org/) format: `<type>: <description>` (e.g., `feat: add user login`, `fix: resolve null pointer in parser`, `chore: update dependencies`)
   - Keep the message concise (1-2 sentences) and focus on the "why" rather than the "what"
3. Run the commit using `--no-gpg-sign`:
   ```
   git commit --no-gpg-sign -m "<message>"
   ```
4. Run `git status` to confirm the commit succeeded.
