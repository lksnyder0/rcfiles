# AI Tool Configurations

This directory contains backup configurations for AI development tools used across machines.

## Purpose

Maintain consistent AI tool configurations across:
- **Personal machines** - Development and personal projects
- **Work machines** - Professional/client work

## Directory Structure

```
ai-configs/
├── claude/              # Claude global instructions
│   ├── CLAUDE-personal.md
│   ├── CLAUDE-work.md
│   └── README.md
├── serena/              # Serena semantic code tool config
│   ├── serena_config.yml.example
│   └── README.md
├── context7/            # Context7 library documentation tool
│   └── README.md
└── README.md            # This file
```

## AI Tools Overview

### Claude Code
**Purpose**: CLI-based AI coding assistant  
**Config Location**: `~/.claude/CLAUDE.md`  
**What it contains**: Global instructions for Claude's behavior, preferences, coding standards

### Serena
**Purpose**: Semantic code navigation and intelligent refactoring  
**Config Location**: `~/.serena/serena_config.yml`  
**What it contains**: Language backend settings, UI preferences, project configurations

### Context7
**Purpose**: Real-time library documentation and code examples  
**Config Location**: Managed as Claude Code MCP plugin (no standalone config)  
**What it contains**: Plugin is auto-configured through Claude Code

## Deployment

Use the deployment script to install configurations:

```bash
# Deploy personal machine configs
./deploy-ai-configs.sh personal

# Deploy work machine configs
./deploy-ai-configs.sh work
```

## Configuration Contexts

### Personal Context
- Personal coding preferences
- Open-source project workflows
- Home lab and infrastructure projects
- Personal DevSecOps practices

### Work Context
- Company-specific coding standards
- Client project requirements
- Enterprise security practices
- Internal tool references

## Security Considerations

### ⚠️ IMPORTANT - Review Before Committing

These configuration files may contain sensitive information:

**Claude Instructions**:
- ❌ Company/client names
- ❌ Internal project names
- ❌ Proprietary development practices
- ❌ Work email addresses
- ✅ Generic coding preferences (safe)
- ✅ Language/framework preferences (safe)

**Serena Config**:
- ❌ Project paths revealing sensitive project names
- ❌ Internal file patterns
- ❌ Company-specific settings
- ✅ Language backend choice (safe)
- ✅ UI preferences (safe)

**Context7**:
- No standalone config to manage
- Plugin-managed through Claude Code

### Before Committing

1. **Run security check**:
   ```bash
   ./scripts/check-ai-configs.sh ai-configs/
   ```

2. **Replace sensitive data** with placeholders:
   - `COMPANY_NAME` instead of actual company
   - `client-project` instead of real client names
   - `user@example.com` instead of work email
   - `/path/to/project` instead of real paths

3. **Use .example files** for configs with many secrets:
   ```bash
   # Create example file
   cp ai-configs/serena/serena_config.yml ai-configs/serena/serena_config.yml.example
   # Edit to sanitize
   vim ai-configs/serena/serena_config.yml.example
   ```

### Protected by .gitignore

These patterns are automatically excluded:
- `ai-configs/**/*.local.*`
- `ai-configs/**/*-secret*`
- `ai-configs/**/*-private*`
- `ai-configs/**/secrets/`
- `ai-configs/serena/config.yml` (use `.example`)
- `ai-configs/context7/config.json` (use `.example`)

## Updating Configurations

### Pull Latest from Machine

```bash
# Backup current configs
cp ~/.claude/CLAUDE.md ai-configs/claude/CLAUDE-personal.md
cp ~/.serena/serena_config.yml ai-configs/serena/serena_config.yml.example

# Review and sanitize
./scripts/check-ai-configs.sh ai-configs/claude/CLAUDE-personal.md
./scripts/check-ai-configs.sh ai-configs/serena/serena_config.yml.example

# Commit if clean
git add ai-configs/
git commit -m "Update AI configurations"
```

### Deploy to New Machine

```bash
# Run deployment script
./deploy-ai-configs.sh personal  # or 'work'

# Restart Claude Code or reload configs
```

## Troubleshooting

### Claude instructions not loading
```bash
# Verify file location
ls -l ~/.claude/CLAUDE.md

# Restart Claude Code
# Instructions reload automatically on next session
```

### Serena config issues
```bash
# Check config syntax
python -c "import yaml; yaml.safe_load(open('~/.serena/serena_config.yml'))"

# Check Serena dashboard
# Ask Claude to "open the Serena dashboard"
```

### Context7 not available
```bash
# Verify plugin is enabled
cat ~/.claude/settings.json | grep context7

# Reinstall plugin through Claude Code
# Use: /plugins command in Claude
```

## Best Practices

### DO
- ✅ Keep configs generic and portable
- ✅ Use example files for sensitive configs
- ✅ Run security checks before committing
- ✅ Document machine-specific quirks
- ✅ Version control your preferences
- ✅ Review git diff before pushing

### DON'T
- ❌ Commit company/client names
- ❌ Commit internal project paths
- ❌ Commit work email addresses
- ❌ Commit API keys or tokens
- ❌ Skip security validation
- ❌ Mix personal and work contexts in same file

## Additional Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude/docs/claude-code)
- [Serena Documentation](https://oraios.github.io/serena/)
- [Context7 Information](https://context7.com/)
- [Security Policy](../SECURITY.md)
- [Security Quick Start](../scripts/SECURITY-QUICKSTART.md)
