---
name: huntress:pr
description: Push the current branch and open a draft pull request with the ai-assisted label. Use this skill when you need to push changes and create a PR.
allowed-tools: Bash(git push:*), Bash(git log:*), Bash(git diff:*), Bash(git status:*), Bash(git branch:*), Bash(git remote:*), Bash(gh pr create:*), Bash(gh pr view:*)
---

## Context

- Current branch: !`git branch --show-current`
- Remote tracking: !`git status -sb`
- Commits on this branch not on main: !`git log --oneline main..HEAD`
- Diff from base branch: !`git diff main...HEAD --stat`

## Your task

Push the current branch and open a pull request.

### Rules

- Pull requests must include a **summary** and a **test plan** in the description.
- Always add the `ai-assisted` label to the pull request.
- Always open the pull request in **draft** state.

### Steps

1. Verify you are NOT on `main`. If you are, stop and inform the user.
2. Push the current branch to the remote with the `-u` flag:
   ```
   git push -u origin <branch-name>
   ```
3. Analyze all commits on this branch (compared to main) to draft the PR title and body.
   - Keep the PR title short (under 70 characters).
   - The body must include a `## Summary` section with 1-3 bullet points and a `## Test plan` section with a checklist.
4. Create the PR using `gh pr create` in draft mode with the `ai-assisted` label:
   ```
   gh pr create --draft --label "ai-assisted" --title "the pr title" --body "$(cat <<'EOF'
   ## Summary
   <1-3 bullet points>

   ## Test plan
   - [ ] ...

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```
5. Return the PR URL to the user.
