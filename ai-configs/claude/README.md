# Claude Global Instructions

Global instructions that control Claude's behavior and preferences across all conversations.

## Configuration File

**Location**: `~/.claude/CLAUDE.md`

## What's Included

Claude global instructions typically contain:

- **Professional background** - Your role, expertise, focus areas
- **Programming preferences** - Language-specific practices, tooling preferences
- **Code quality standards** - Performance, security, documentation requirements
- **Project structure preferences** - File organization, naming conventions
- **Workflow preferences** - Git practices, testing approaches

## Context-Specific Files

### CLAUDE-personal.md
For personal machines and open-source work:
- Personal coding preferences
- Open-source best practices
- Home lab / infrastructure preferences
- Generic technical preferences

### CLAUDE-work.md
For work machines (NOT COMMITTED - kept local only):
- Company-specific standards
- Client requirements
- Internal tool references
- Enterprise practices

**⚠️ IMPORTANT**: Work instructions should NOT be committed to public repos

## Deployment

The deployment script creates symlinks:

```bash
# Personal machine
./deploy-ai-configs.sh personal
# Creates: ~/.claude/CLAUDE.md -> ai-configs/claude/CLAUDE-personal.md

# Work machine (local only)
./deploy-ai-configs.sh work
# Creates: ~/.claude/CLAUDE.md -> ai-configs/claude/CLAUDE-work.md
```

## Sanitization Checklist

Before committing CLAUDE-personal.md, ensure:

- [ ] No company or client names
- [ ] No work email addresses
- [ ] No internal project names
- [ ] No proprietary development practices
- [ ] No internal URLs or services
- [ ] No API endpoints or credentials
- [ ] Generic examples only
- [ ] Replaced specifics with `COMPANY_NAME`, `PROJECT_NAME`, etc.

## Example Sanitization

### ❌ DON'T Commit
```markdown
## Work Projects
- Acme Corp uses AWS account 123456789
- Always use internal npm registry at npm.acme-corp.internal
- Contact john.doe@acme-corp.com for architecture questions
```

### ✅ DO Commit
```markdown
## Project Standards
- Use appropriate cloud provider based on project requirements
- Follow company/project package registry policies
- Consult team architecture documentation
```

## Security Check

Before committing:

```bash
./scripts/check-ai-configs.sh ai-configs/claude/CLAUDE-personal.md
```

## Updating Instructions

### From Current Machine

```bash
# Copy current global instructions
cp ~/.claude/CLAUDE.md ai-configs/claude/CLAUDE-personal.md

# Review and sanitize
vim ai-configs/claude/CLAUDE-personal.md

# Security check
./scripts/check-ai-configs.sh ai-configs/claude/CLAUDE-personal.md

# Commit if clean
git add ai-configs/claude/CLAUDE-personal.md
git commit -m "Update Claude global instructions"
```

### To New Machine

```bash
# Use deployment script
./deploy-ai-configs.sh personal

# Or manual symlink
ln -sf ~/.rcfiles/ai-configs/claude/CLAUDE-personal.md ~/.claude/CLAUDE.md
```

## Testing Changes

Claude Code automatically reloads global instructions:
- Changes take effect in the next conversation
- No restart required
- Test with a simple prompt to verify preferences

## Best Practices

### Content Guidelines
- Keep instructions concise and actionable
- Use bullet points for clarity
- Organize by category (Language, Tools, Practices)
- Include rationale for non-obvious preferences
- Make preferences specific enough to be useful

### Maintenance
- Review and update quarterly
- Remove outdated preferences
- Keep file size reasonable (<50KB)
- Version control all changes
- Document breaking changes in commit messages

### Organization
Suggested structure:
```markdown
# Personal Preferences

## Professional Background
- Brief role description
- Key expertise areas

## Language Preferences
### Python
- Specific practices
### JavaScript
- Specific practices

## Tools & Infrastructure
- Preferred tools
- Configuration preferences

## Code Quality
- Testing requirements
- Documentation standards
- Security practices

## Project Structure
- File organization
- Naming conventions
```

## Troubleshooting

### Instructions not taking effect
- Verify file location: `ls -l ~/.claude/CLAUDE.md`
- Check file is not empty: `wc -l ~/.claude/CLAUDE.md`
- Start a new conversation (changes don't apply mid-conversation)
- Check for syntax errors in Markdown

### Conflicting instructions
- Be specific about when rules apply
- Use "prefer X over Y" instead of absolute mandates
- Allow for context-specific exceptions

### Instructions too long
- Claude can handle large instruction files
- But shorter, focused instructions often work better
- Consider splitting by context (personal vs work)

## Additional Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude/docs/claude-code)
- [Example Global Instructions](https://docs.anthropic.com/claude/docs/custom-instructions)
