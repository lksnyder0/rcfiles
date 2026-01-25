# rcfiles - Task Completion Checklist

## After Making Changes

### 1. Documentation Updates (CRITICAL)
When making changes, update the appropriate documentation files:

#### ZSH Changes
- Added/modified aliases → Update `docs/zsh.md`
- Added/modified functions in `zfunc/` → Update `docs/zsh.md`
- Added/modified environment variables → Update `docs/zsh.md`
- Changed oh-my-zsh plugins → Update `docs/zsh.md`

#### Neovim Changes
- Added/removed plugins → Update `docs/neovim.md` plugin tables
- Added/modified keybindings → Update `docs/neovim.md`
- Changed LSP servers → Update `docs/neovim.md`
- Changed formatters → Update `docs/neovim.md`
- Modified leader key or core mappings → Update `docs/neovim.md` and `README.md`

#### tmux Changes
- Added/modified keybindings → Update `docs/tmux.md`
- Changed prefix key → Update `docs/tmux.md` and `README.md`
- Modified appearance/status bar → Update `docs/tmux.md`

#### Conky Changes (Linux-only)
- Modified configurations → Update `docs/conky.md`

#### README Updates
- Changes affecting quick reference section → Update `README.md`
- New dependencies added → Update `README.md` dependency tables
- Installation steps changed → Update `README.md`

### 2. Verify Syntax (Language-Specific)

#### Lua Files (Neovim)
```bash
# Test Neovim configuration loads without errors
nvim --headless +qall
# Or open Neovim and check for errors
nvim
:checkhealth
```

#### Shell Scripts/Functions
```bash
# Source and test ZSH functions
source ~/.rcfiles/zfunc/<function_name>
# Or reload entire zshrc
source ~/.zshrc
```

### 3. Test Configuration Changes

#### ZSH
```bash
# Reload configuration
source ~/.zshrc

# Test new functions/aliases
<function_name>
<alias_name>

# Verify no errors in shell startup
zsh -c "echo 'Shell loaded successfully'"
```

#### Neovim
```bash
# Launch Neovim and verify plugins load
nvim

# Inside Neovim, check:
:Lazy sync           # Sync plugins
:checkhealth         # Verify health
:Mason               # Check LSP servers
```

#### tmux
```bash
# Start tmux or reload config in existing session
tmux
# OR (inside tmux):
C-a r               # Reload config
```

### 4. Git Workflow

```bash
# Check status
git status

# Review changes
git diff

# Stage changes
git add <files>

# Commit with descriptive message
git commit -m "Add/Update/Fix: description of changes"

# Push to remote
git push origin main
```

### 5. No Linting/Formatting Required
- This repository has no automated linting or formatting checks
- Manual review of code quality is sufficient
- Stylua can be used optionally for Lua files: `stylua nvim/config/nvim/`
- Shellcheck can be used optionally for shell scripts: `shellcheck <script>`

### 6. No Automated Tests
- No test suite to run
- Testing is manual verification that configurations work as expected
- Test by actually using the modified configuration

## Special Considerations

### Breaking Changes
If making breaking changes (e.g., changing leader key, removing widely-used aliases):
- Document in `CHANGELOG.md`
- Consider backward compatibility
- Update all affected documentation

### Machine-Specific Configs
- Never commit files in `hostspecific/zsh/*.sh`
- Verify `.gitignore` excludes these files

### Git Submodules
If updating cheatsheets submodule:
```bash
cd cheatsheets
git pull origin master
cd ..
git add cheatsheets
git commit -m "Update cheatsheets submodule"
```

## Deployment/Testing Workflow

1. Make changes to configuration files
2. Update documentation (see section 1)
3. Test locally by reloading config
4. Verify no errors or unexpected behavior
5. (Optional) Run `./test-environment.sh` to verify all components
6. Commit changes with descriptive message
7. Push to remote repository
8. On other machines, run `update_rcfiles` to pull changes
9. On new machines, run `./install-arch.sh` for full setup (Arch Linux)

## Installation Scripts

### install-arch.sh
Automated installation script for Arch Linux that:
- Installs all required packages and dependencies
- Creates all symlinks
- Installs version managers (asdf, nvm, rvm, poetry)
- Bootstraps Neovim plugins
- Sets up oh-my-zsh

### test-environment.sh
Comprehensive test script that verifies:
- All tools and dependencies are installed
- Symlinks are correctly configured
- Configurations load without errors
- LSP servers and formatters are available
- Git submodules are initialized
- File permissions are correct

Run after installation or when troubleshooting issues.
