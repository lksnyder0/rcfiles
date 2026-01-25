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

### Install Dependencies

#### Arch Linux

```bash
# Core tools
sudo pacman -S neovim zsh tmux git curl

# oh-my-zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Neovim dependencies
sudo pacman -S ripgrep fd make gcc npm python go

# LSP and formatter dependencies
sudo pacman -S python-black stylua jq rubygems terraform

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
└── docs/                 # Tool-specific documentation
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
| terraform | formatter.nvim | `pacman -S terraform` / `brew install terraform` |

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
