# Security Tools Quick Start Guide

Quick reference for protecting sensitive data in AI configurations.

## Initial Setup (One-time)

```bash
# Run the automated setup script
./scripts/setup-security-tools.sh

# This will:
# - Install pre-commit, detect-secrets, gitleaks, shellcheck
# - Setup git hooks
# - Create secrets baseline
```

## Before Committing AI Configs

### 1. Manual Review

```bash
# View the file you're about to commit
cat ai-configs/claude/CLAUDE-personal.md

# Check for sensitive data patterns manually
grep -i "password\|secret\|token\|key" ai-configs/claude/CLAUDE-personal.md
```

### 2. Run Security Check

```bash
# Check specific file
./scripts/check-ai-configs.sh ai-configs/claude/CLAUDE-personal.md

# Or check all AI configs
./scripts/check-ai-configs.sh
```

### 3. Review and Fix Issues

If issues are found:
- **Critical issues (❌)**: MUST fix before committing
- **Warnings (⚠️)**: Review carefully

**Fix by replacing with placeholders:**
```yaml
# Before (❌ DON'T COMMIT)
apiKey: "sk_live_abc123def456"

# After (✓ SAFE)
apiKey: "YOUR_API_KEY_HERE"
```

### 4. Commit

```bash
git add ai-configs/
git commit -m "Add AI configurations"

# Pre-commit hooks run automatically
# If they fail, review and fix issues
```

## Common Patterns to Replace

| Real Data | Placeholder |
|-----------|-------------|
| `sk_live_abc123...` | `YOUR_API_KEY_HERE` |
| `ghp_1234567890...` | `YOUR_GITHUB_TOKEN` |
| `user@company.com` | `user@example.com` |
| `acme-corp-project` | `example-project` |
| `https://internal.company.com` | `https://internal.example.com` |
| `192.168.1.100` | `192.168.x.x` |
| `AWS_ACCOUNT_ID: 123456789012` | `AWS_ACCOUNT_ID: YOUR_ACCOUNT_ID` |

## Security Checklist

Before committing, ensure:

- [ ] No API keys or tokens
- [ ] No passwords
- [ ] No company/client names
- [ ] No internal URLs
- [ ] No private IP addresses
- [ ] No real email addresses
- [ ] No AWS/GCP/Azure account IDs
- [ ] No SSH keys or certificates
- [ ] Ran `./scripts/check-ai-configs.sh`
- [ ] Reviewed `git diff --cached`

## Quick Commands

```bash
# Check AI configs for secrets
./scripts/check-ai-configs.sh

# Run all security checks manually
pre-commit run --all-files

# Run specific check
pre-commit run check-ai-configs
pre-commit run gitleaks

# View what would be committed
git diff --cached

# Skip hooks (DANGEROUS - use with caution)
git commit --no-verify
```

## Example: Sanitizing a Config File

```bash
# 1. Copy config to ai-configs
cp ~/.config/serena/config.yml ai-configs/serena/config.yml.example

# 2. Edit and replace sensitive data
vim ai-configs/serena/config.yml.example

# Replace in file:
# - Real project names → "example-project"
# - Real paths → "/path/to/project"
# - Company names → "COMPANY_NAME"
# - Internal URLs → "https://internal.example.com"

# 3. Run security check
./scripts/check-ai-configs.sh ai-configs/serena/config.yml.example

# 4. If clean, commit
git add ai-configs/serena/config.yml.example
git commit -m "Add Serena config example"
```

## Troubleshooting

### "Permission denied" error
```bash
chmod +x scripts/check-ai-configs.sh
chmod +x scripts/setup-security-tools.sh
```

### Hooks not running
```bash
pre-commit install
```

### False positive detection
```bash
# For detect-secrets, audit baseline
detect-secrets audit .secrets.baseline

# For our script, use placeholders like:
# - YOUR_KEY_HERE
# - EXAMPLE_VALUE
# - xxx or 123 for dummy data
```

### Need to commit despite warnings
```bash
# Review carefully first!
git diff --cached

# If truly safe, bypass
git commit --no-verify
```

## Emergency: Committed a Secret

If you accidentally committed a secret:

```bash
# 1. IMMEDIATELY rotate/revoke the secret
#    (Change password, revoke token, etc.)

# 2. Remove from git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch <file-with-secret>" \
  --prune-empty --tag-name-filter cat -- --all

# 3. Force push (if already pushed)
git push origin --force --all

# 4. Consider the secret compromised
#    Even after removal, it may be cached/archived
```

## Prevention is Best

**ALWAYS** run security checks before committing:
1. Manual review
2. `./scripts/check-ai-configs.sh`
3. Review `git diff`
4. Let pre-commit hooks run

**NEVER** bypass hooks unless you're absolutely certain the file is safe.
