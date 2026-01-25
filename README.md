# rcfiles

Personal dotfiles for Linux and macOS environments featuring Neovim, ZSH with oh-my-zsh, tmux, and Conky (Linux-only).

**Repository**: https://gitlab.com/lksnyder0/rcfiles

## Tools Covered

| Tool | Description |
|------|-------------|
| [Neovim](docs/neovim.md) | Primary editor with LSP, Treesitter, and modern plugins |
| [ZSH](docs/zsh.md) | Shell configuration with oh-my-zsh framework |
| [tmux](docs/tmux.md) | Terminal multiplexer with vim-style navigation |
| [Conky](docs/conky.md) | System monitor for Linux desktops (power-aware) |
| [AI Tools](docs/ai-tools.md) | Claude Code, Serena, Context7 for AI-powered development |

## Prerequisites

- **Git** - For cloning the repository and submodules
- **curl** - For downloading dependencies

## Installation

### Clone the Repository

```bash
git clone https://gitlab.com/lksnyder0/rcfiles.git ~/.rcfiles
cd ~/.rcfiles
git submodule init
git submodule update
```

### Automated Installation (Arch Linux)

For Arch Linux users, an automated installation script is provided that handles all dependencies, symlinks, and configuration:

```bash
cd ~/.rcfiles
./install-arch.sh
```

This script will:
- Install all required packages (Neovim, ZSH, tmux, Conky, etc.)
- Install all Neovim dependencies (ripgrep, fd, LSP servers, formatters)
- Install development tools (kubectl, docker, gh, kubecolor, aws-vault)
- Install version managers (asdf, nvm, rvm, poetry)
- Install oh-my-zsh framework
- Create all necessary symlinks
- Initialize git submodules
- Set ZSH as the default shell
- Bootstrap Neovim plugins
- Install tools from .tool-versions via asdf

After running the script, restart your shell or run `source ~/.zshrc`.

#### Verify Installation

After installation, run the test script to verify everything is configured correctly:

```bash
cd ~/.rcfiles
./test-environment.sh
```

This test script checks:
- All core tools are installed (Neovim, ZSH, tmux, etc.)
- Neovim dependencies (ripgrep, fd, LSP servers, formatters)
- Development tools (kubectl, docker, gh, kubecolor)
- Version managers (asdf, nvm, rvm, poetry)
- Symlinks are correctly configured
- Git submodules are initialized
- ZSH configuration loads without errors
- Neovim configuration is valid
- tmux configuration is valid

The script provides a detailed report with pass/fail status for each component.

### Manual Installation

#### Arch Linux

```bash
# Core tools
sudo pacman -S neovim zsh tmux git curl

# oh-my-zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Neovim dependencies
sudo pacman -S ripgrep fd make gcc npm python go

# LSP and formatter dependencies
sudo pacman -S python-black stylua jq rubygems opentofu

# Optional: Ruby LSP
sudo gem install solargraph

# Optional: asdf version manager
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.14.0

# Optional: Conky (Linux desktop only)
sudo pacman -S conky lm_sensors
```

#### macOS (Homebrew)

```bash
# Core tools
brew install neovim zsh tmux git curl

# oh-my-zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Neovim dependencies
brew install ripgrep fd make gcc npm python go

# LSP and formatter dependencies
brew install black stylua jq terraform

# Optional: Ruby LSP
gem install solargraph

# Optional: asdf version manager
brew install asdf
```

### Deploy Configuration (Symlinks)

Create symlinks to deploy configurations:

```bash
# ZSH configuration
ln -sf ~/.rcfiles/zshrc ~/.zshrc

# tmux configuration
ln -sf ~/.rcfiles/tmux.conf ~/.tmux.conf

# Neovim configuration
mkdir -p ~/.config
ln -sf ~/.rcfiles/nvim/config/nvim ~/.config/nvim

# asdf tool versions (optional)
ln -sf ~/.rcfiles/tool-versions ~/.tool-versions

# Conky configuration (Linux only)
ln -sf ~/.rcfiles/conky ~/.config/conky
```

### Post-Installation

1. **Restart your shell** or run `source ~/.zshrc`
2. **Open Neovim** - plugins will auto-install via lazy.nvim on first launch
3. **Start tmux** - configuration loads automatically

## Project Structure

```
.rcfiles/
├── nvim/                 # Neovim configuration
│   └── config/nvim/      # Symlinked to ~/.config/nvim
├── zshrc                 # ZSH configuration (oh-my-zsh)
├── zfunc/                # Custom ZSH functions (autoloaded)
├── tmux.conf             # tmux configuration
├── conky/                # Conky configs (Linux-only)
├── hostspecific/zsh/     # Machine-specific configs (ephemeral, not committed)
├── tool-versions         # asdf version definitions
├── cheatsheets/          # Git submodule with vim/tmux cheatsheets
├── docs/                 # Tool-specific documentation
├── install-arch.sh       # Automated installation script for Arch Linux
└── test-environment.sh   # Environment verification script
```

## Quick Reference

### Neovim
- **Leader key**: `<Space>`
- **Plugin manager**: lazy.nvim (auto-bootstraps)
- **File explorer**: `<leader>e`
- **Find files**: `<leader>sf`
- **Live grep**: `<leader>sg`
- **Format**: `<leader>ff`

### ZSH
- **Theme**: bira
- **Edit config**: `c_zsh`
- **Reload config**: `r_zsh`
- **Update rcfiles**: `update_rcfiles`

### tmux
- **Prefix**: `C-a` (not C-b)
- **Split horizontal**: `C-a |`
- **Split vertical**: `C-a -`
- **Pane navigation**: `C-a h/j/k/l`
- **Reload config**: `C-a r`

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

# For work machines (configs not committed to repo)
./deploy-ai-configs.sh work
```

**Security Note**: AI configurations are protected with automated security scanning. See [SECURITY.md](SECURITY.md) for details.

## Documentation

See the `docs/` directory for detailed documentation:

- [ZSH Configuration](docs/zsh.md) - Aliases, functions, plugins, environment
- [Neovim Configuration](docs/neovim.md) - Plugins, keybindings, LSP, formatters
- [tmux Configuration](docs/tmux.md) - Keybindings, options, status bar
- [Conky Configuration](docs/conky.md) - Power-aware system monitor (Linux)

## External Dependencies

### Neovim Plugins

| Dependency | Required By | Install |
|------------|-------------|---------|
| ripgrep | telescope.nvim | `pacman -S ripgrep` / `brew install ripgrep` |
| fd | telescope.nvim | `pacman -S fd` / `brew install fd` |
| make | telescope-fzf-native | `pacman -S make` / `brew install make` |
| C compiler | nvim-treesitter | `pacman -S gcc` / `brew install gcc` |
| npm | mason.nvim (LSP) | `pacman -S npm` / `brew install npm` |
| Node.js | copilot.vim | `pacman -S nodejs` / `brew install node` |
| black | formatter.nvim | `pacman -S python-black` / `brew install black` |
| stylua | formatter.nvim | `pacman -S stylua` / `brew install stylua` |
| jq | formatter.nvim | `pacman -S jq` / `brew install jq` |
| gofmt | formatter.nvim | Included with Go |
| rubocop | formatter.nvim | `gem install rubocop` |
| opentofu | formatter.nvim | `pacman -S opentofu` / `brew install opentofu` |

### ZSH

| Dependency | Required By | Install |
|------------|-------------|---------|
| oh-my-zsh | zshrc | See installation above |
| asdf | asdf plugin | `pacman -S asdf` / `brew install asdf` |
| aws-vault | avs function | `asdf install aws-vault` |
| kubecolor | kubectl alias | `pacman -S kubecolor` / `brew install kubecolor` |

## Host-Specific Configuration

Machine-specific ZSH configs can be placed in `hostspecific/zsh/*.sh` and are sourced automatically. These files are **ephemeral** and should NOT be committed.

## License

MIT
