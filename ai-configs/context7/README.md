# Context7 Configuration

Context7 provides real-time library documentation and code examples for various programming libraries and frameworks.

## Configuration Management

**Important**: Context7 is managed as a Claude Code MCP (Model Context Protocol) plugin and does not have a standalone global configuration file.

## How Context7 Works

Context7 is installed and configured through Claude Code's plugin system:

1. **Installation**: Installed via Claude Code plugins
2. **Configuration**: Managed through Claude Code settings
3. **Activation**: Enabled/disabled in `~/.claude/settings.json`

## Plugin Status

Check if Context7 is enabled:

```bash
# View Claude Code settings
cat ~/.claude/settings.json

# Look for:
# {
#   "enabledPlugins": {
#     "context7@claude-plugins-official": true
#   }
# }
```

## Plugin Location

Context7 plugin files:
- **Install Path**: `~/.claude/plugins/cache/claude-plugins-official/context7/`
- **Plugin Definition**: `.mcp.json` and `.claude-plugin/plugin.json`
- **No User Config**: Context7 doesn't use a user-editable configuration file

## Features Provided

Context7 MCP server provides:

- **Library Documentation**: Up-to-date docs for popular libraries
- **Code Examples**: Real-world usage examples
- **API Reference**: Function signatures and parameters
- **Best Practices**: Recommended patterns and approaches

Supported libraries include:
- Frontend: React, Vue, Angular, Next.js, etc.
- Backend: Express, FastAPI, Django, Rails, etc.
- Databases: MongoDB, PostgreSQL, Redis, etc.
- Cloud: AWS, GCP, Azure SDKs
- And many more...

## Usage

Context7 is accessed automatically by Claude Code when you:
- Ask questions about library APIs
- Request code examples
- Need documentation for a specific library
- Want to learn best practices

Example queries:
```
"How do I use React hooks?"
"Show me MongoDB aggregation examples"
"What's the FastAPI syntax for async endpoints?"
```

## Managing Context7

### Enable/Disable

Through Claude Code (no manual config needed):

```bash
# Plugins are managed through Claude Code UI
# Use: /plugins command in Claude conversation
```

### Update Plugin

Context7 updates automatically through Claude Code:
- Updates pulled from official plugin repository
- No manual update process needed

### Reinstall

If Context7 isn't working:

1. Ask Claude to check plugin status
2. Use `/plugins` command to reinstall
3. Restart Claude Code if needed

## No Backup Needed

Since Context7:
- Has no user-editable configuration
- Is managed entirely by Claude Code
- Auto-updates from official sources

**There is nothing to backup or deploy** for Context7.

## Security Considerations

### No Configuration to Protect

Context7 doesn't store:
- ❌ User credentials (no authentication)
- ❌ Project paths
- ❌ Sensitive settings
- ✅ Only uses publicly available documentation

### Plugin Permissions

Context7 MCP plugin:
- Reads library documentation from public sources
- No file system access
- No network access beyond documentation APIs
- No secrets or credentials required

## Troubleshooting

### Context7 not responding

```bash
# Check if plugin is enabled
cat ~/.claude/settings.json | grep context7

# Expected output:
# "context7@claude-plugins-official": true
```

### Enable Context7

Ask Claude:
```
/plugins
# Select context7 to enable
```

### Plugin errors

1. Check Claude Code logs
2. Restart Claude Code
3. Reinstall plugin through `/plugins`

### Documentation out of date

- Context7 updates automatically
- Wait for next plugin update
- Or report through Claude Code feedback

## Comparison with Other MCP Plugins

| Plugin | Has Config File | Backup Needed |
|--------|----------------|---------------|
| Serena | ✅ Yes (`~/.serena/serena_config.yml`) | ✅ Yes |
| Context7 | ❌ No | ❌ No |
| GitHub | ❌ No (uses git credentials) | ⚠️ Credentials only |
| Feature-dev | ❌ No | ❌ No |
| Code-review | ❌ No | ❌ No |

## Alternative: Standalone Context7

If you want standalone Context7 (not through Claude Code):

```bash
# Install context7 CLI (if available)
npm install -g context7-cli

# Or use context7 API directly
# See: https://context7.com/docs
```

Note: This is separate from the Claude Code MCP plugin.

## Additional Resources

- [Context7 Website](https://context7.com/)
- [Claude Code Plugins Documentation](https://docs.anthropic.com/claude/docs/plugins)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

## Summary

**Context7 requires NO backup or configuration management** for this repository because:
1. It's a Claude Code plugin, not a standalone tool
2. No user-editable configuration exists
3. Plugin is managed automatically by Claude Code
4. No sensitive data to protect

To use Context7 on a new machine:
1. Install Claude Code
2. Enable Context7 plugin
3. Done! No config deployment needed.
