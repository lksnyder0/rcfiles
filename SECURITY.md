# Security Policy

## Protecting Sensitive Data

This repository contains tools to help protect sensitive information before committing to Git. This is especially important for AI tool configurations that may contain:

- API keys and tokens
- Passwords and credentials  
- Company/client names
- Internal URLs and IP addresses
- SSH keys and certificates

## Security Tools

We use multiple layers of protection:

1. **Custom security scanner** (`scripts/check-ai-configs.sh`)
2. **Pre-commit hooks** (`.pre-commit-config.yaml`)
3. **Secret detection** (detect-secrets, gitleaks)
4. **Comprehensive .gitignore** patterns

## Quick Start

### Initial Setup

```bash
# Run automated setup (installs all tools)
./scripts/setup-security-tools.sh
```

This installs:
- pre-commit framework
- detect-secrets
- gitleaks (optional)
- shellcheck (optional)
- Git hooks

### Before Every Commit

1. **Manual review** - Read the file you're committing
2. **Run security check**:
   ```bash
   ./scripts/check-ai-configs.sh ai-configs/your-file.md
   ```
3. **Fix any issues** - Replace real secrets with placeholders
4. **Commit** - Pre-commit hooks run automatically

## What to Replace

| Don't Commit | Use Instead |
|--------------|-------------|
| Real API keys | `YOUR_API_KEY_HERE` |
| Real passwords | `YOUR_PASSWORD_HERE` |
| Company names | `COMPANY_NAME` or `example-company` |
| Work email | `user@example.com` |
| Internal URLs | `https://internal.example.com` |
| Private IPs | `192.168.x.x` or `10.x.x.x` |
| Client names | `client-name` or `customer-name` |

## Documentation

- **Quick Start**: `scripts/SECURITY-QUICKSTART.md`
- **Detailed Guide**: `scripts/README.md`
- **Setup Script**: `scripts/setup-security-tools.sh`
- **Check Script**: `scripts/check-ai-configs.sh`

## Pre-commit Hooks

Hooks run automatically before each commit. They check for:

- Secrets and credentials
- Large files (>1MB)
- Merge conflicts
- YAML/JSON syntax errors
- Shell script issues
- Lua formatting

### Manual Execution

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run check-ai-configs --all-files
pre-commit run gitleaks --all-files
```

### Bypassing Hooks

⚠️ **Use with extreme caution!**

```bash
# Skip all hooks (DANGEROUS)
git commit --no-verify

# Skip specific hook
SKIP=check-ai-configs git commit
```

Only bypass if you've manually verified the file is safe.

## Reporting a Security Issue

If you discover a security vulnerability in this repository:

1. **Do NOT open a public issue**
2. **Do NOT commit the vulnerability**
3. Contact the repository owner directly
4. Provide details about the vulnerability
5. Wait for confirmation before disclosing publicly

## If You Accidentally Commit a Secret

1. **IMMEDIATELY** rotate/revoke the credential
2. Remove from git history:
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch <file>" \
     --prune-empty --tag-name-filter cat -- --all
   ```
3. Force push if already pushed:
   ```bash
   git push origin --force --all
   ```
4. **Consider the secret compromised** - Even after removal, it may be cached

## Best Practices

- ✅ **DO** use placeholder values in configs
- ✅ **DO** create `.example` files for sensitive configs
- ✅ **DO** run security checks before committing
- ✅ **DO** review `git diff` before committing
- ✅ **DO** use .gitignore for files with real secrets
- ❌ **DON'T** commit real API keys or tokens
- ❌ **DON'T** commit real passwords
- ❌ **DON'T** commit company/client information
- ❌ **DON'T** bypass pre-commit hooks without review
- ❌ **DON'T** commit files you haven't personally reviewed

## Files Protected by .gitignore

The following patterns are automatically excluded:

```
ai-configs/**/*.local.*
ai-configs/**/*-secret*
ai-configs/**/*-private*
ai-configs/**/secrets/
ai-configs/**/*token*
ai-configs/**/*credential*
ai-configs/serena/config.yml  # Use config.yml.example
ai-configs/context7/config.json  # Use config.json.example
```

## Security Checklist

Before committing AI configurations:

- [ ] Manually reviewed the file
- [ ] No API keys or tokens
- [ ] No passwords
- [ ] No company/client names (or genericized)
- [ ] No internal URLs (or genericized)
- [ ] No private IP addresses
- [ ] No real email addresses (use @example.com)
- [ ] No AWS/cloud account IDs
- [ ] No SSH keys or certificates
- [ ] Ran `./scripts/check-ai-configs.sh <file>`
- [ ] Reviewed `git diff --cached`
- [ ] All placeholders use obvious patterns (YOUR_, EXAMPLE_, etc.)

## Additional Resources

- [Pre-commit Documentation](https://pre-commit.com/)
- [detect-secrets](https://github.com/Yelp/detect-secrets)
- [gitleaks](https://github.com/gitleaks/gitleaks)
- [git-secrets](https://github.com/awslabs/git-secrets)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)

## Contact

For security questions or concerns, contact the repository maintainer.
