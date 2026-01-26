# Implementation Plan for rcfiles TODO Items

## Overview
This plan covers four main tasks:
1. Add AI tools configuration backup system
2. Create macOS installation script
3. Update test script for macOS support
4. Add Docker status panel to Conky

---

## TASK 1: Add AI Tools Configuration Backup

### Objectives
- Backup global Claude instructions (machine-specific: personal vs work)
- Backup global Serena configuration (shared)
- Backup global Context7 configuration (shared)
- Document AI setup in README
- Add tools to the tools list

### File Structure Plan

```
.rcfiles/
├── ai-configs/
│   ├── README.md                    # Documentation for AI configs
│   ├── claude/
│   │   ├── CLAUDE-personal.md       # Personal machine instructions
│   │   ├── CLAUDE-work.md           # Work machine instructions
│   │   └── .gitignore               # Ignore sensitive overrides
│   ├── serena/
│   │   ├── config.yml               # Global Serena config
│   │   └── README.md                # Serena config notes
│   └── context7/
│       ├── config.json              # Global Context7 config
│       └── README.md                # Context7 config notes
├── deploy-ai-configs.sh             # Deployment script for AI configs
└── ...
```

### Implementation Steps

#### 1.1: Research Global Config Locations
**Action**: Verify standard locations for AI tool configurations
- Claude global instructions: `~/.claude/CLAUDE.md`
- Serena global config: Check `~/.config/serena/` or `~/.serena/`
- Context7 global config: Check `~/.config/context7/` or similar
- Document findings in ai-configs/README.md

#### 1.2: Create Directory Structure
**Action**: Create ai-configs directory with subdirectories
- Create `ai-configs/claude/`, `ai-configs/serena/`, `ai-configs/context7/`
- Create placeholder README files in each subdirectory

#### 1.3: Create Claude Instructions Templates
**Action**: Create separate Claude instruction files for different contexts
- `ai-configs/claude/CLAUDE-personal.md` - Personal machine instructions
- `ai-configs/claude/CLAUDE-work.md` - Work machine instructions
- Copy current global instructions as starting point
- Add clear headers indicating which context each is for
- Add security note about not including secrets

#### 1.4: Security Review
**Action**: Review configurations for security considerations
- **Serena config**: May contain:
  - Project paths (potentially revealing sensitive project names)
  - Custom project configurations
  - File patterns or exclusions
  - **Decision needed**: User should review before committing
  
- **Context7 config**: May contain:
  - API keys or authentication tokens
  - Personal preferences
  - Usage history or cached data
  - **Decision needed**: User should review and potentially use .gitignore for sensitive parts
  
- **Recommendations to document**:
  - Use `.env` or separate untracked files for secrets
  - Add `.gitignore` entries for any token/key files
  - Consider using example config files (`.example` suffix) for sensitive configs

#### 1.5: Create Deployment Script
**Action**: Create `deploy-ai-configs.sh` script
- **Purpose**: Deploy AI configurations to global locations
- **Features**:
  - Accept argument for context (personal/work)
  - Backup existing configs before overwriting
  - Create symlinks from ai-configs to global locations
  - Validate configs before deploying
- **Structure** (following install-arch.sh style):
  - Color-coded output functions
  - Modular functions for each tool
  - Error handling and rollback capability
  - Usage instructions

```bash
#!/bin/bash
# deploy-ai-configs.sh
# Usage: ./deploy-ai-configs.sh [personal|work]

# Functions to implement:
# - check_prerequisites()      # Verify AI tools are installed
# - backup_existing_configs()  # Backup current global configs
# - deploy_claude_config()     # Deploy appropriate Claude instructions
# - deploy_serena_config()     # Deploy Serena config
# - deploy_context7_config()   # Deploy Context7 config
# - verify_deployment()        # Verify symlinks and configs
```

#### 1.6: Update .gitignore
**Action**: Add entries to prevent committing sensitive data
```gitignore
# AI configuration secrets
ai-configs/claude/CLAUDE-*.local.md
ai-configs/serena/*.local.*
ai-configs/context7/*.local.*
ai-configs/**/secrets/
ai-configs/**/*token*
ai-configs/**/*key*
```

#### 1.7: Update README - Tools List
**Action**: Add AI tools to the "Tools Covered" table
```markdown
| Tool | Description |
|------|-------------|
| ... existing tools ... |
| [Claude Code](docs/ai-tools.md) | AI-powered coding assistant with MCP servers |
```

#### 1.8: Create docs/ai-tools.md
**Action**: Create comprehensive AI tools documentation
**Content structure**:
- Overview of AI setup
- Claude Code usage
  - Installation
  - Global instructions management
  - Commands and shortcuts
- Installed MCP Servers
  - **Serena**:
    - Purpose: Semantic code navigation and editing
    - Capabilities: Symbol search, refactoring, code understanding
    - Configuration location and options
  - **Context7**:
    - Purpose: Library documentation and API reference
    - Capabilities: Up-to-date docs, code examples, best practices
    - Configuration location and options
- Deployment instructions (using deploy-ai-configs.sh)
- Troubleshooting section

#### 1.9: Add AI Setup Section to README
**Action**: Add new section after "Quick Reference" and before "Documentation"
```markdown
## AI Development Tools

This repository includes configuration for AI-powered development tools:

- **Claude Code**: CLI-based AI coding assistant
- **MCP Servers**:
  - **Serena**: Semantic code navigation, symbol search, and intelligent refactoring
  - **Context7**: Real-time library documentation and code examples

See [AI Tools Documentation](docs/ai-tools.md) for detailed setup and usage.

### Deploying AI Configurations

```bash
# For personal machines
./deploy-ai-configs.sh personal

# For work machines
./deploy-ai-configs.sh work
```
```

---

## TASK 2: Add macOS Installation Script

### Objectives
- Create install-macos.sh matching install-arch.sh style
- Support all tools that work on macOS
- Skip Linux-only features (Conky, systemd)
- Handle package name differences

### Implementation Steps

#### 2.1: Create Script Skeleton
**Action**: Create `install-macos.sh` with same structure as install-arch.sh
- Copy helper functions (color codes, print functions)
- Create main() function with same flow
- Add macOS detection check

#### 2.2: Platform Detection
**Action**: Implement check_macos() function
```bash
check_macos() {
    if [[ "$OSTYPE" != "darwin"* ]]; then
        print_error "This script is designed for macOS only"
        exit 1
    fi
    print_success "Running on macOS $(sw_vers -productVersion)"
}
```

#### 2.3: Homebrew Prerequisite
**Action**: Implement check_homebrew() and install_homebrew() functions
- Check if brew is installed
- Offer to install Homebrew if missing
- Verify installation

#### 2.4: Package Manager Adaptation
**Action**: Replace all pacman commands with brew equivalents

**Package mapping** (to be verified during implementation):
| Arch (pacman) | macOS (brew) | Notes |
|---------------|--------------|-------|
| base-devel | - | Not needed (Xcode CLI tools) |
| neovim | neovim | Same name |
| python | python@3.12 | Version-specific |
| python-pip | - | Included with python |
| python-black | black | Different package name |
| npm | node | node includes npm |
| opentofu | opentofu/tap/opentofu | Requires tap |
| lm_sensors | - | Skip (Linux-only) |
| conky | - | Skip (Linux-only) |

#### 2.5: Functions to Adapt

**Functions to implement** (matching install-arch.sh structure):
1. `update_system()` - Run brew update & upgrade
2. `install_core_tools()` - brew install core packages
3. `install_neovim_deps()` - brew install neovim dependencies
4. `install_lsp_formatter_deps()` - brew install LSP/formatters
   - Handle different package names
   - Use gem/pip/npm for language-specific tools
5. `install_dev_tools()` - brew install kubectl, gh, etc.
6. `skip_conky()` - Print info that Conky is Linux-only
7. `install_oh_my_zsh()` - Same as Arch
8. `install_asdf()` - brew install asdf (simpler than Arch)
9. `install_nvm()` - Same as Arch
10. `install_rvm()` - Same as Arch
11. `install_poetry()` - Same as Arch
12. `create_symlinks()` - Adapt for macOS paths
    - Skip Conky symlink
    - Verify other paths work on macOS
13. `init_git_submodules()` - Same as Arch
14. `change_default_shell()` - Adapt for macOS
    - May need to add zsh to /etc/shells
    - Use chsh differently
15. `install_nvim_plugins()` - Same as Arch
16. `install_asdf_tools()` - Same as Arch
17. `create_hostspecific_dir()` - Same as Arch

#### 2.6: macOS-Specific Considerations
**Action**: Handle macOS-specific differences
- Xcode Command Line Tools may be required: `xcode-select --install`
- Different default shell location: `/bin/zsh` vs `/usr/bin/zsh`
- Homebrew permissions (may need sudo in some cases)
- Path additions for Homebrew (/opt/homebrew/bin on M1, /usr/local/bin on Intel)

#### 2.7: Final Instructions
**Action**: Adapt final instructions for macOS
- Remove references to systemd services
- Remove references to Conky
- Add macOS-specific notes (e.g., terminal restart, permissions)

---

## TASK 3: Update Test Script for macOS Support

### Objectives
- Make test-environment.sh work on both Arch Linux and macOS
- Skip platform-specific tests appropriately
- Maintain same output format and test structure

### Implementation Steps

#### 3.1: Add Platform Detection
**Action**: Add platform detection at script start
```bash
# Detect platform
PLATFORM=""
if [ -f /etc/arch-release ]; then
    PLATFORM="arch"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
else
    print_error "Unsupported platform"
    exit 1
fi

print_info "Detected platform: $PLATFORM"
```

#### 3.2: Create Platform-Aware Helper Functions
**Action**: Add functions to handle platform differences

```bash
# Check if package is installed (platform-aware)
package_installed() {
    local package="$1"
    if [ "$PLATFORM" = "arch" ]; then
        pacman -Qi "$package" &> /dev/null
    elif [ "$PLATFORM" = "macos" ]; then
        brew list "$package" &> /dev/null
    fi
}

# Skip test based on platform
skip_if_not_platform() {
    local required_platform="$1"
    local test_name="$2"
    if [ "$PLATFORM" != "$required_platform" ]; then
        print_info "Skipping $test_name (requires $required_platform)"
        return 0  # true (should skip)
    fi
    return 1  # false (don't skip)
}
```

#### 3.3: Update Test Functions
**Action**: Modify test functions to be platform-aware

**Functions to modify**:

1. **test_core_tools()** - Add platform-specific checks
   - neovim command is same on both
   - Verify version output format on both platforms

2. **test_neovim_deps()** - Handle package name differences
   - python vs python3 naming
   - Different version output formats

3. **test_lsp_formatters()** - Check correct packages per platform
   - opentofu package location differs
   - stylua installation method may differ

4. **test_dev_tools()** - Same tools, different install methods
   - kubecolor may be brew-only or AUR-only

5. **test_conky()** - Skip entirely on macOS
```bash
test_conky() {
    if skip_if_not_platform "arch" "Conky tests"; then
        return
    fi
    
    print_header "Testing Conky (Linux-only)"
    # ... existing tests ...
}
```

6. **test_version_managers()** - Handle asdf differently
   - asdf on macOS installed via brew, not git clone
   - Check in /opt/homebrew or /usr/local instead of ~/.asdf

7. **test_symlinks()** - Skip Conky symlink on macOS

8. **test_file_permissions()** - Add check for install-macos.sh
```bash
if [ "$PLATFORM" = "macos" ] && [ -x "$HOME/.rcfiles/install-macos.sh" ]; then
    test_pass "install-macos.sh is executable"
elif [ "$PLATFORM" = "macos" ]; then
    test_warn "install-macos.sh is not executable"
fi
```

#### 3.4: Update Summary Output
**Action**: Include platform info in summary
```bash
print_header "Test Summary ($PLATFORM)"
```

#### 3.5: Update Final Instructions
**Action**: Provide platform-specific next steps
```bash
print_next_steps() {
    if [ $TESTS_FAILED -gt 0 ]; then
        echo -e "${YELLOW}Recommended Next Steps:${NC}"
        if [ "$PLATFORM" = "arch" ]; then
            echo -e "  1. Run ${BLUE}./install-arch.sh${NC} to install missing components"
        elif [ "$PLATFORM" = "macos" ]; then
            echo -e "  1. Run ${BLUE}./install-macos.sh${NC} to install missing components"
        fi
        # ... rest of instructions ...
    fi
}
```

---

## TASK 4: Add Docker Status Panel to Conky

### Objectives
- Add Docker memory usage display
- List running Docker containers
- Only show panel when Docker is running
- Update both AC and battery configs

### Implementation Steps

#### 4.1: Create Docker Stats Helper Script
**Action**: Create `conky/docker-stats.sh`

**Purpose**: Extract Docker stats in Conky-compatible format

**Script functionality**:
```bash
#!/bin/bash
# docker-stats.sh - Get Docker statistics for Conky

# Check if Docker is running
if ! docker info &>/dev/null; then
    echo "Docker not running"
    exit 1
fi

# Get Docker memory usage
# Output format suitable for Conky display
docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}\t{{.CPUPerc}}" | tail -n +2
```

#### 4.2: Create Docker Detection Function
**Action**: Add Docker status check to Conky configs

**Approach**: Use Conky's `${if_running}` or `${exec}` to conditionally show section

**Detection methods**:
1. Check if Docker daemon is running: `pgrep dockerd`
2. Check if Docker socket exists: `test -S /var/run/docker.sock`
3. Try docker info command: `docker info &>/dev/null`

#### 4.3: Design Panel Layout
**Action**: Design Docker panel appearance

**Layout structure**:
```
${color1}DOCKER STATUS${color}
${if_running dockerd}
Memory Used: ${exec docker stats --no-stream --format "{{.MemUsage}}" | awk '{sum+=$1} END {print sum " MB"}'}

${color1}Running Containers${color}
${exec docker ps --format "table {{.Names}}\t{{.Status}}" | tail -n +2 | head -5}

${else}
${color3}Docker daemon not running${color}
${endif}
```

**Considerations**:
- Limit container list to 5-10 to avoid cluttering display
- Use `${execigraph}` for memory usage trend
- Color-code based on usage levels
- Consider CPU % alongside memory

#### 4.4: Update conky-ac.conf
**Action**: Add Docker panel to AC power config

**Placement**: After VRAM section, before Temperatures

**Panel content** (1-second update interval):
```conky
${color1}Docker Status${color}
${if_running dockerd}Memory: ${execi 5 docker info --format '{{.MemTotal}}' 2>/dev/null || echo "N/A"}

${color1}Running Containers (${execi 5 docker ps -q | wc -l})${color}
${execi 5 docker ps --format "{{.Names}}: {{.Status}}" | head -5}
${else}${color3}Docker not available${color}${endif}
${hr 1}
```

**Update interval**: 5 seconds (execi 5) to balance freshness with performance

#### 4.5: Update conky-battery.conf
**Action**: Add Docker panel to battery config

**Placement**: Same as AC config

**Differences from AC config**:
- May want longer update interval (10-15 seconds) to save battery
- Consider making it optional/collapsible on battery

**Panel content** (battery-optimized):
```conky
${color1}Docker Status${color}
${if_running dockerd}${execi 15 docker ps -q | wc -l} containers running
${execi 15 docker ps --format "{{.Names}}" | head -3}
${else}${color3}Docker not available${color}${endif}
${hr 1}
```

#### 4.6: Handle Docker Not Installed
**Action**: Gracefully handle systems without Docker

**Approach**: Use conditional display
```conky
${if_existing /usr/bin/docker}
${if_running dockerd}
  # Show full Docker stats
${else}
  ${color3}Docker installed but not running${color}
${endif}
${else}
  # Don't show Docker section at all
${endif}
```

**Alternative**: Always include section but show "Not installed" message

#### 4.7: Optimize Performance
**Action**: Ensure Docker checks don't slow down Conky

**Optimizations**:
1. Use `execi` with reasonable intervals (5-15 seconds)
2. Cache Docker daemon status check
3. Use lightweight Docker commands
4. Avoid expensive operations like `docker stats` without --no-stream
5. Limit output with `head` to prevent large text blocks

#### 4.8: Test Docker Panel
**Action**: Test panel in different scenarios

**Test cases**:
1. Docker installed and running with containers
2. Docker installed but daemon not running
3. Docker not installed at all
4. No containers running
5. Many containers running (10+)
6. High memory usage scenarios

#### 4.9: Update Documentation
**Action**: Update docs/conky.md

**Additions**:
- Document Docker panel functionality
- Explain conditional display logic
- Note update intervals and performance considerations
- Add troubleshooting for Docker detection issues

---

## Implementation Order

### Phase 1: AI Configurations (Lowest Risk)
1. Create ai-configs directory structure
2. Research and document global config locations
3. Create deployment script
4. Update documentation

### Phase 2: macOS Install Script (Medium Complexity)
1. Create install-macos.sh skeleton
2. Adapt functions one by one
3. Test on macOS system (if available)
4. Document macOS-specific quirks

### Phase 3: Test Script Updates (Depends on Phase 2)
1. Add platform detection
2. Update test functions
3. Test on both platforms
4. Update documentation

### Phase 4: Docker Panel (Standalone)
1. Create docker-stats.sh helper
2. Update conky configs
3. Test with/without Docker
4. Update documentation

---

## Verification Checklist

### Task 1: AI Configs
- [ ] ai-configs directory structure created
- [ ] Deployment script functional
- [ ] Security review completed (user approval needed)
- [ ] README updated with AI tools section
- [ ] docs/ai-tools.md created and comprehensive
- [ ] .gitignore updated for sensitive files

### Task 2: macOS Install Script
- [ ] install-macos.sh created and executable
- [ ] All functions adapted for macOS
- [ ] Homebrew detection and installation works
- [ ] Package names verified on macOS
- [ ] Symlinks work correctly
- [ ] Error handling robust
- [ ] Final instructions accurate

### Task 3: Test Script Updates
- [ ] Platform detection working
- [ ] All tests adapted for macOS
- [ ] Linux-only tests skipped on macOS
- [ ] macOS-only checks added
- [ ] Test output clear and accurate
- [ ] Summary shows platform info
- [ ] Both platforms tested successfully

### Task 4: Docker Panel
- [ ] docker-stats.sh created and functional
- [ ] conky-ac.conf updated with Docker panel
- [ ] conky-battery.conf updated with Docker panel
- [ ] Conditional display works (Docker on/off)
- [ ] Performance acceptable
- [ ] docs/conky.md updated
- [ ] All test scenarios pass

---

## Security Considerations Summary

### Critical Security Items Requiring User Review

1. **Serena Configuration**
   - May contain project paths revealing sensitive project names
   - Review before committing to public repo
   - Consider using .gitignore for sensitive paths

2. **Context7 Configuration**
   - May contain API keys or authentication tokens
   - Review for any credentials before committing
   - Use environment variables or separate secret files for tokens
   - Add token/key patterns to .gitignore

3. **Claude Instructions**
   - Should not contain hardcoded secrets
   - May reference work-specific projects or internal tools
   - Separate personal/work contexts to avoid leaking proprietary info

### Recommended Security Practices
- Add comprehensive .gitignore entries for AI config secrets
- Use .example files for configs with sensitive fields
- Document secret management in ai-configs/README.md
- Never commit API keys, tokens, or credentials
- Review git diff before committing AI configs
- Consider pre-commit hooks to detect secrets

---

## Dependencies and Prerequisites

### External Dependencies to Verify
- macOS package availability (brew search for each package)
- Docker installation status
- Global AI config file locations
- MCP server installation verification

### Files to Create
- `ai-configs/` directory structure (multiple files)
- `deploy-ai-configs.sh`
- `install-macos.sh`
- `conky/docker-stats.sh`
- `docs/ai-tools.md`

### Files to Modify
- `README.md` (add AI section, update tools table)
- `test-environment.sh` (add macOS support)
- `conky/conky-ac.conf` (add Docker panel)
- `conky/conky-battery.conf` (add Docker panel)
- `docs/conky.md` (document Docker panel)
- `.gitignore` (add AI config exclusions)

### Total Estimated Changes
- **New files**: ~8-10
- **Modified files**: ~6-8
- **Lines of code**: ~1500-2000 (mostly bash scripts)
