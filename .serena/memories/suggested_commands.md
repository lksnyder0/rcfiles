# rcfiles - Suggested Commands

## Git Commands

### Version Control
```bash
git status                    # Check repository status
git add <file>                # Stage specific file
git commit -m "message"       # Commit changes
git push origin master        # Push to remote
git pull origin master        # Pull latest changes
git submodule update          # Update git submodules
git submodule sync            # Sync submodule URLs
```

### Custom Functions (via zfunc/)
```bash
update_rcfiles                # Pull latest changes and update submodules
commit_rcfiles                # Stage all and commit (interactive)
```

## File Operations

### Listing and Navigation
```bash
ls -la                        # List files with details
find . -name "*.lua"          # Find Lua files
cd ~/.rcfiles                 # Navigate to rcfiles directory
```

### File Viewing
```bash
cat <file>                    # View file contents
less <file>                   # Page through file
head -n 20 <file>             # View first 20 lines
tail -n 20 <file>             # View last 20 lines
```

### File Search
```bash
grep -r "pattern" .           # Recursive search
grep -n "pattern" file        # Search with line numbers
```

## Symlink Management

### Create Symlinks
```bash
ln -sf ~/.rcfiles/zshrc ~/.zshrc
ln -sf ~/.rcfiles/tmux.conf ~/.tmux.conf
ln -sf ~/.rcfiles/nvim/config/nvim ~/.config/nvim
ln -sf ~/.rcfiles/tool-versions ~/.tool-versions
ln -sf ~/.rcfiles/conky ~/.config/conky  # Linux only
```

### Verify Symlinks
```bash
ls -l ~/.zshrc                # Check zshrc symlink
ls -l ~/.config/nvim          # Check neovim symlink
```

## Testing Configuration Changes

### ZSH
```bash
source ~/.zshrc               # Reload ZSH configuration
zsh                           # Start new shell with updated config
```

### Neovim
```bash
nvim                          # Launch Neovim (plugins auto-install)
# Inside Neovim:
:Lazy sync                    # Sync plugins
:checkhealth                  # Check Neovim health
:Mason                        # Open Mason LSP installer
```

### tmux
```bash
tmux                          # Start tmux
# Inside tmux:
C-a r                         # Reload tmux config (prefix + r)
```

## Development Tools

### asdf Version Manager
```bash
asdf list                     # List installed versions
asdf install                  # Install versions from .tool-versions
asdf current                  # Show current versions
```

## System-Specific Commands (Linux)

### Package Management (Arch Linux)
```bash
sudo pacman -S <package>      # Install package
sudo pacman -Syu              # Update system
sudo pacman -Qs <query>       # Search installed packages
```

### Conky
```bash
conky -c ~/.config/conky/conky-ac.conf        # Start Conky (AC power)
killall conky                                  # Stop Conky
```

## Linting and Formatting

### Lua (Neovim configs)
```bash
stylua nvim/config/nvim/      # Format Lua files (if installed)
```

### Shell Scripts
```bash
shellcheck <script>           # Lint shell scripts (if installed)
```

## No Automated Testing
This is a dotfiles repository with no automated test suite. Testing is done by:
1. Applying configuration changes via symlinks
2. Reloading the affected tool (source zshrc, restart neovim, etc.)
3. Verifying expected behavior manually

## No Build Process
No compilation or build steps required. Configuration files are used directly.

## Installation

### Automated Installation (Arch Linux)
```bash
cd ~/.rcfiles
./install-arch.sh              # Comprehensive automated installation
```

The install-arch.sh script handles:
- All package installations (core tools, Neovim deps, LSP servers, formatters)
- Development tools (kubectl, docker, gh, kubecolor, aws-vault)
- Version managers (asdf, nvm, rvm, poetry)
- oh-my-zsh installation
- Symlink creation
- Git submodule initialization
- Default shell change to ZSH
- Neovim plugin bootstrapping
- asdf tool installation from .tool-versions

### Verify Installation
```bash
cd ~/.rcfiles
./test-environment.sh          # Run comprehensive environment tests
```

The test script verifies:
- All core tools and dependencies are installed
- Symlinks are correctly configured
- Git submodules are initialized
- Configurations load without errors
- LSP servers and formatters are available
- Version managers are properly installed

### Manual Installation Steps
See README.md for manual installation instructions for Arch Linux or macOS.
