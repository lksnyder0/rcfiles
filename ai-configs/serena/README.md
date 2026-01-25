# Serena Configuration

Serena is a semantic code navigation and intelligent refactoring tool that provides deep code understanding capabilities.

## Configuration File

**Location**: `~/.serena/serena_config.yml`

## What's Included

Serena configuration typically contains:

- **Language backend** - LSP or JetBrains integration
- **UI preferences** - GUI log window, web dashboard settings
- **Project configurations** - Project-specific settings
- **LSP settings** - Language server configurations
- **Performance options** - Caching, indexing preferences

## Files in This Directory

### serena_config.yml.example
Example configuration with common settings:
- Language backend: LSP (free, works everywhere)
- Web dashboard enabled
- Performance settings
- Logging preferences

### serena_config.yml (NOT COMMITTED)
Your actual config (gitignored). May contain:
- Project paths with company/client names
- Internal tool configurations
- Custom LSP setups
- Performance tuning specific to your projects

## Deployment

The deployment script handles Serena config:

```bash
./deploy-ai-configs.sh personal
# Creates: ~/.serena/serena_config.yml (symlink or copy)
```

## Configuration Options

### Language Backend
```yaml
language_backend: LSP
# Options: LSP, JetBrains
# LSP: Free, works everywhere, uses standard language servers
# JetBrains: Requires Serena plugin in JetBrains IDE
```

### Web Dashboard
```yaml
web_dashboard: true
# Provides browser-based access to:
# - Configuration viewer
# - Session logs
# - Tool usage statistics
# - Project state
```

### GUI Log Window
```yaml
gui_log_window: false
# Desktop window with logs (Windows/Linux only, not macOS)
# Alternative: use web_dashboard instead
```

### Dashboard Settings
```yaml
web_dashboard_listen_address: 127.0.0.1
web_dashboard_port: 8765
web_dashboard_open_on_launch: true
```

## Security Considerations

### ⚠️ Sensitive Data in Serena Config

Review before committing:

**Project configurations**:
- ❌ Project paths: `/home/user/work/acme-corp/backend`
- ❌ Client names in project IDs
- ❌ Internal tool paths
- ✅ Generic examples: `/path/to/project`

**LSP settings**:
- ❌ Internal language server endpoints
- ❌ Custom authentication
- ✅ Standard LSP configurations

**Performance settings**:
- ✅ Generally safe to commit

### Example Sanitization

#### ❌ DON'T Commit
```yaml
projects:
  - name: "acme-internal-api"
    path: "/home/user/work/acme-corp/backend"
  - name: "client-secret-project"
    path: "/home/user/clients/bigcorp/app"
```

#### ✅ DO Commit
```yaml
# Example project configuration
# projects:
#   - name: "example-project"
#     path: "/path/to/project"
```

## Security Check

Before committing:

```bash
./scripts/check-ai-configs.sh ai-configs/serena/serena_config.yml.example
```

## Updating Configuration

### From Current Machine

```bash
# Copy current config
cp ~/.serena/serena_config.yml ai-configs/serena/serena_config.yml.example

# Review and sanitize
vim ai-configs/serena/serena_config.yml.example
# Remove: project paths, client names, internal settings
# Keep: language backend, UI settings, general preferences

# Security check
./scripts/check-ai-configs.sh ai-configs/serena/serena_config.yml.example

# Commit if clean
git add ai-configs/serena/serena_config.yml.example
git commit -m "Update Serena configuration example"
```

### To New Machine

```bash
# Use deployment script
./deploy-ai-configs.sh personal

# Or manual copy
cp ai-configs/serena/serena_config.yml.example ~/.serena/serena_config.yml
# Edit ~/.serena/serena_config.yml with machine-specific settings
```

## Testing Changes

1. **Verify config syntax**:
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('~/.serena/serena_config.yml'))"
   ```

2. **Check Serena dashboard**:
   - Ask Claude: "open the Serena dashboard"
   - Verify settings appear correctly

3. **Test code navigation**:
   - Try finding symbols in your project
   - Verify LSP backend is working

## Common Configurations

### Minimal Config
```yaml
language_backend: LSP
web_dashboard: true
gui_log_window: false
```

### Development Config
```yaml
language_backend: LSP
web_dashboard: true
web_dashboard_open_on_launch: false  # Don't auto-open browser
gui_log_window: false
```

### Performance Optimized
```yaml
language_backend: LSP
web_dashboard: true
gui_log_window: false
# Additional LSP performance settings
lsp_timeout: 30
max_workers: 4
```

## Troubleshooting

### Serena not finding symbols
- Check language backend is LSP
- Verify language servers are installed
- Check dashboard logs for errors
- Restart Claude Code

### Dashboard not opening
- Check `web_dashboard: true` in config
- Verify port 8765 is not in use
- Check firewall settings
- Manually visit: http://127.0.0.1:8765

### Config changes not applying
- Restart Claude Code
- Check config syntax with YAML validator
- Review dashboard for configuration errors

### LSP backend issues
- Verify language servers are installed (Mason in Neovim, or system-wide)
- Check LSP logs in dashboard
- Test individual language servers manually

## Project-Specific Configuration

Serena supports project-specific configs in `.serena/project.yml`:

```yaml
# .serena/project.yml (in project root)
name: "my-project"
language: "python"
# Project-specific settings
```

This file is committed to the project repo, not rcfiles.

## Additional Resources

- [Serena Documentation](https://oraios.github.io/serena/)
- [Serena GitHub](https://github.com/oraios/serena)
- [LSP Configuration](https://oraios.github.io/serena/02-usage/030_lsp.html)
- [Dashboard Usage](https://oraios.github.io/serena/02-usage/060_dashboard.html)
