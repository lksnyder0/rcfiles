# User Instructions

## Git Workflow

- Always create a new git branch before starting any code changes or writing any files. Name the branch descriptively based on the task (e.g., `feat/add-login-page`, `fix/null-pointer-error`). Do not make changes directly on the current branch unless explicitly instructed otherwise.
- Never commit directly to `main`. Always work on a separate branch and use a pull request workflow.

## Tools

- Always use OpenTofu (not Terraform) and Helm for infrastructure as code.
- Always use uv for Python package management.
