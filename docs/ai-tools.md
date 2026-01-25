# AI Development Tools

This repository includes configuration for AI-powered development tools that enhance coding productivity and code understanding.

## Tools Overview

| Tool | Purpose | Config Location |
|------|---------|----------------|
| **Claude Code** | AI coding assistant CLI | `~/.claude/CLAUDE.md` |
| **Serena** | Semantic code navigation & refactoring | `~/.serena/serena_config.yml` |
| **Context7** | Library documentation & code examples | MCP plugin (auto-configured) |

## Claude Code

**Purpose**: Command-line interface for Claude AI, providing intelligent coding assistance

**Capabilities**:
- Code generation and modification
- Bug fixing and debugging
- Code explanation and documentation
- Refactoring and optimization suggestions
- Git operations (commits, PRs)
- Multi-file context understanding

**Configuration**:
- Global instructions: `~/.claude/CLAUDE.md`
- Controls Claude's behavior, preferences, and coding standards
- Separate configs for personal vs work contexts

**Usage**:
```bash
# Start Claude Code in a project
cd ~/project
claude

# Specific tasks
claude "fix the bug in auth.py"
claude "write tests for user service"
```

## MCP Servers

Claude Code uses MCP (Model Context Protocol) servers to extend functionality:

### Serena

**Purpose**: Semantic code navigation and intelligent refactoring

**Capabilities**:
- Symbol search across codebase
- Find all references to functions/classes
- Intelligent code editing at symbol level
- Project structure understanding
- Rename refactoring with reference updates
- Language Server Protocol (LSP) integration

**Configuration**:
- Config file: `~/.serena/serena_config.yml`
- Settings: Language backend (LSP), UI preferences, performance options
- Web dashboard: `http://127.0.0.1:8765` (when enabled)

**How it helps**:
- Navigate large codebases efficiently
- Understand code relationships
- Refactor safely with reference tracking
- Find symbol definitions and usages

**Example queries to Claude**:
```
"Find all references to the User class"
"Rename the authenticate method to verify_credentials"
"Show me the definition of calculate_total"
```

### Context7

**Purpose**: Real-time library documentation and code examples

**Capabilities**:
- Up-to-date documentation for thousands of libraries
- Code examples and usage patterns
- API reference and function signatures
- Best practices for popular frameworks
- Multi-language support

**Configuration**:
- No standalone config (managed by Claude Code)
- Enabled through Claude Code plugin system
- Auto-updates documentation from official sources

**Supported Libraries** (examples):
- **Frontend**: React, Vue, Angular, Svelte, Next.js
- **Backend**: Express, FastAPI, Django, Rails, Laravel
- **Databases**: MongoDB, PostgreSQL, Redis, Prisma
- **Cloud**: AWS SDK, GCP, Azure
- **Tools**: Docker, Kubernetes, Terraform

**How it helps**:
- Get accurate, current documentation
- Learn library APIs quickly
- See real-world usage examples
- Avoid deprecated patterns

**Example queries to Claude**:
```
"How do I use React hooks for state management?"
"Show me MongoDB aggregation examples"
"What's the FastAPI syntax for async endpoints?"
"How do I configure Docker multi-stage builds?"
```

## Installation

### Claude Code

```bash
# Install Claude Code (if not already installed)
# Follow: https://docs.anthropic.com/claude/docs/claude-code

# Verify installation
claude --version
```

### MCP Servers

MCP servers are managed through Claude Code:

```bash
# Enable plugins in Claude Code
# Method 1: Through conversation
claude
# Then use: /plugins

# Method 2: Edit settings
vim ~/.claude/settings.json
# Set "enabledPlugins": { "serena@claude-plugins-official": true }
```

## Configuration Management

This repository backs up AI tool configurations for consistency across machines.

### Directory Structure

```
ai-configs/
├── claude/              # Claude global instructions
│   ├── CLAUDE-personal.md    # Personal machine config
│   ├── CLAUDE-work.md        # Work machine config (not committed)
│   └── README.md
├── serena/              # Serena configuration
│   ├── serena_config.yml.example
│   └── README.md
└── context7/            # Context7 info (plugin-managed)
    └── README.md
```

### Deployment

Deploy configurations to a machine:

```bash
# Personal machine
./deploy-ai-configs.sh personal

# Work machine
./deploy-ai-configs.sh work
```

This creates symlinks:
- `~/.claude/CLAUDE.md` → `ai-configs/claude/CLAUDE-personal.md`
- `~/.serena/serena_config.yml` ← copied from example (customizable)

### Updating Configurations

Pull latest configs from current machine:

```bash
# Copy current configs
cp ~/.claude/CLAUDE.md ai-configs/claude/CLAUDE-personal.md
cp ~/.serena/serena_config.yml ai-configs/serena/serena_config.yml.example

# Review and sanitize
./scripts/check-ai-configs.sh ai-configs/

# Commit if clean
git add ai-configs/
git commit -m "Update AI configurations"
```

## Security Considerations

AI configurations may contain sensitive information. See [SECURITY.md](../SECURITY.md) for details.

### Before Committing

Always run security checks:

```bash
./scripts/check-ai-configs.sh ai-configs/
```

### What to Sanitize

| Config | Sensitive Data | Safe to Commit |
|--------|----------------|----------------|
| Claude | Company/client names, work email, internal projects | Generic preferences, language choices |
| Serena | Project paths, client names, internal settings | Language backend, UI preferences |
| Context7 | N/A (plugin-managed) | N/A |

### Example Sanitization

**Before** (❌ DON'T commit):
```markdown
## Work Projects
- Acme Corp uses internal npm registry at npm.acme.internal
- Contact john.doe@acme.com for questions
```

**After** (✅ DO commit):
```markdown
## Project Standards
- Follow company package registry policies
- Consult team documentation for standards
```

## Troubleshooting

### Claude Code

**Issue**: Global instructions not taking effect
```bash
# Verify file exists
ls -l ~/.claude/CLAUDE.md

# Start new conversation (changes don't apply mid-conversation)
claude
```

**Issue**: Claude not starting
```bash
# Check Claude Code installation
claude --version

# Check for errors
claude --debug
```

### Serena

**Issue**: Serena not finding symbols
```bash
# Check Serena dashboard
# Ask Claude: "open the Serena dashboard"

# Verify config
cat ~/.serena/serena_config.yml

# Check language servers are installed
# (Mason in Neovim, or system-wide)
```

**Issue**: Dashboard not opening
```bash
# Check configuration
grep web_dashboard ~/.serena/serena_config.yml

# Verify port 8765 is free
lsof -i :8765

# Manually visit
firefox http://127.0.0.1:8765
```

### Context7

**Issue**: Context7 not responding
```bash
# Check if plugin is enabled
cat ~/.claude/settings.json | grep context7

# Enable through Claude
claude
# Then: /plugins
# Select and enable context7
```

**Issue**: Outdated documentation
```bash
# Context7 auto-updates
# Wait for next plugin update
# Or report through Claude Code feedback
```

## Best Practices

### Using Claude Code Effectively

1. **Provide context**: Share relevant files and error messages
2. **Be specific**: Clear task descriptions get better results
3. **Iterate**: Refine requests based on Claude's responses
4. **Use tools**: Leverage Serena for navigation, Context7 for docs
5. **Review output**: Always review generated code before committing

### Configuring Global Instructions

1. **Keep it concise**: Focus on most important preferences
2. **Be specific**: "Prefer X over Y" rather than vague guidelines
3. **Organize by topic**: Languages, tools, practices
4. **Include rationale**: Explain why for non-obvious choices
5. **Update regularly**: Review quarterly, remove outdated items

### Managing Configurations

1. **Separate contexts**: Personal vs work configs
2. **Version control**: Commit sanitized configs
3. **Security first**: Always run checks before committing
4. **Test deployments**: Verify on new machines
5. **Document quirks**: Note machine-specific requirements

## Workflows

### Starting a New Project

```bash
# 1. Navigate to project
cd ~/code/new-project

# 2. Start Claude Code
claude

# 3. Ask Claude to explore
"Analyze the codebase structure"

# 4. Use Serena for navigation
"Find all database models"

# 5. Use Context7 for learning
"Show me FastAPI best practices"
```

### Debugging Issues

```bash
# 1. Share error with context
claude "I'm getting this error: [paste error]
The error occurs in auth.py when calling verify_user"

# 2. Let Claude use Serena to find references
# Claude can search codebase automatically

# 3. Get Context7 docs if needed
# Claude can fetch library documentation

# 4. Implement fix
# Claude generates solution with full context
```

### Code Review

```bash
# Use code-review plugin (if enabled)
claude /review-pr 123

# Or manual review
claude "Review the changes in src/auth.py
Focus on security and performance"
```

## Additional Resources

### Documentation
- [Claude Code Official Docs](https://docs.anthropic.com/claude/docs/claude-code)
- [Serena Documentation](https://oraios.github.io/serena/)
- [Context7 Website](https://context7.com/)
- [MCP Protocol](https://modelcontextprotocol.io/)

### Repository Files
- [AI Configs README](../ai-configs/README.md)
- [Security Policy](../SECURITY.md)
- [Security Quick Start](../scripts/SECURITY-QUICKSTART.md)
- [Deployment Script](../deploy-ai-configs.sh)

### Getting Help
- Claude Code: Use `/help` command
- Serena: Check dashboard logs
- Context7: Query through Claude
- General: See main [README](../README.md)
