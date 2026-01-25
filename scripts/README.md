# Scripts Directory

This directory contains utility scripts for maintaining and securing the rcfiles repository.

## Security Scripts

### check-ai-configs.sh

**Purpose**: Scan AI configuration files for potentially sensitive data before committing to Git.

**Usage**:
```bash
# Scan all files in ai-configs/
./scripts/check-ai-configs.sh

# Scan specific files
./scripts/check-ai-configs.sh ai-configs/claude/CLAUDE-personal.md

# Run as part of git workflow
git add ai-configs/
./scripts/check-ai-configs.sh
```

**What it detects**:

**Critical Issues** (will prevent commit):
- API keys and access tokens
- Bearer tokens
- Passwords (non-placeholder)
- AWS Access Key IDs (AKIA...)
- SSH private keys
- JWT tokens

**Warnings** (review before committing):
- AWS account IDs (12-digit numbers)
- Email addresses (non-example domains)
- Internal/private URLs
- .local domains
- Private IP addresses
- Database connection strings with credentials
- Certificates

**Exit codes**:
- `0` - No issues or only warnings (safe to commit with review)
- `1` - Critical issues found (DO NOT COMMIT)
- `2` - Script error

## Pre-commit Hooks

This repository uses [pre-commit](https://pre-commit.com/) to automatically check for security issues before commits.

### Installation

```bash
# Install pre-commit (if not already installed)
pip install pre-commit

# Install the git hooks
cd ~/.rcfiles
pre-commit install
```

### What gets checked

1. **detect-secrets** - Yelp's secret detection tool
2. **gitleaks** - Comprehensive secret scanner
3. **check-ai-configs** - Custom AI config security check (our script)
4. **General checks**:
   - Large files (>1MB)
   - Merge conflicts
   - YAML/JSON syntax
   - Private keys
   - Shell script linting (shellcheck)
   - Lua formatting (stylua)

### Usage

Pre-commit hooks run automatically when you commit:

```bash
git add ai-configs/claude/CLAUDE-personal.md
git commit -m "Add Claude instructions"
# Pre-commit hooks run automatically
```

**Manual execution**:

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run check-ai-configs --all-files
pre-commit run gitleaks --all-files

# Run on staged files only
pre-commit run

# Skip hooks (use cautiously)
git commit --no-verify
```

### Updating hooks

```bash
# Update hook versions
pre-commit autoupdate

# Clear cache and re-run
pre-commit clean
pre-commit run --all-files
```

## Secret Detection Baseline

The `.secrets.baseline` file contains a baseline of known false positives for the detect-secrets tool.

### Creating/updating the baseline

```bash
# Create initial baseline
detect-secrets scan > .secrets.baseline

# Audit the baseline (mark false positives)
detect-secrets audit .secrets.baseline

# Update baseline with new files
detect-secrets scan --baseline .secrets.baseline
```

## Bypassing Security Checks

**⚠️ Use with extreme caution!**

If you absolutely need to bypass security checks:

```bash
# Skip pre-commit hooks
git commit --no-verify

# Skip specific hook
SKIP=check-ai-configs git commit
```

**When to bypass** (rarely):
- You've manually verified the file is safe
- The detection is a false positive you've confirmed
- You're committing an encrypted file that triggers detection

**Never bypass for**:
- Real API keys or tokens
- Actual passwords or credentials
- Private SSH keys
- Company/client names you shouldn't expose

## Troubleshooting

### "Permission denied" when running check-ai-configs.sh

```bash
chmod +x scripts/check-ai-configs.sh
```

### Pre-commit hooks not running

```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install

# Verify installation
pre-commit run --all-files
```

### False positives in secret detection

1. For **detect-secrets**: Update `.secrets.baseline` using audit command
2. For **check-ai-configs.sh**: Use placeholder patterns like `YOUR_KEY_HERE`, `EXAMPLE_`, or `xxx`
3. For **gitleaks**: Create `.gitleaksignore` file with patterns to exclude

### Hook is too slow

```bash
# Run only fast hooks
SKIP=gitleaks,detect-secrets git commit

# Or update .pre-commit-config.yaml to disable slow hooks
```

## Best Practices

### Before committing AI configs

1. **Review the file manually** - Read through it first
2. **Run security check** - `./scripts/check-ai-configs.sh <file>`
3. **Replace sensitive data** with placeholders:
   - `YOUR_API_KEY_HERE`
   - `COMPANY_NAME`
   - `example-project`
   - `user@example.com`
4. **Use .example files** for configs with many secrets
5. **Check git diff** - `git diff --cached` before commit
6. **Let pre-commit run** - Don't bypass unless necessary

### Creating .example files

```bash
# Copy real config
cp ai-configs/serena/config.yml ai-configs/serena/config.yml.example

# Edit to replace sensitive data
vim ai-configs/serena/config.yml.example

# Add to git
git add ai-configs/serena/config.yml.example

# The real config.yml is gitignored
```

### Security checklist

- [ ] No API keys or tokens
- [ ] No passwords
- [ ] No company/client names
- [ ] No internal URLs
- [ ] No private IP addresses
- [ ] No real email addresses
- [ ] No AWS account IDs
- [ ] No SSH keys or certificates
- [ ] Used placeholders for all sensitive fields
- [ ] Ran security check script
- [ ] Reviewed git diff

## Additional Security Tools

### git-secrets (AWS focused)

```bash
# Install
brew install git-secrets  # macOS
# or: yay -S git-secrets  # Arch Linux

# Setup in repo
git secrets --install
git secrets --register-aws

# Scan
git secrets --scan
```

### truffleHog (Deep history scan)

```bash
# Install
pip install truffleHog

# Scan git history
trufflehog git file://. --only-verified
```

### GitHub Secret Scanning

If you push to GitHub, they automatically scan for known secret patterns. Review any alerts immediately.

## References

- [pre-commit documentation](https://pre-commit.com/)
- [detect-secrets](https://github.com/Yelp/detect-secrets)
- [gitleaks](https://github.com/gitleaks/gitleaks)
- [git-secrets](https://github.com/awslabs/git-secrets)
