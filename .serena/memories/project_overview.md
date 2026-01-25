# rcfiles - Project Overview

## Purpose
Personal dotfiles repository for configuring development environment across Linux and macOS systems. Manages configurations for:
- Neovim (primary text editor)
- ZSH (shell with oh-my-zsh framework)
- tmux (terminal multiplexer)
- Conky (system monitor, Linux-only)
- asdf (tool version manager)

**Repository**: https://gitlab.com/lksnyder0/rcfiles

## Tech Stack
- **Lua**: Neovim configuration (lazy.nvim plugin manager)
- **Bash/Shell**: ZSH functions, installation scripts
- **Markdown**: Documentation
- **Git submodules**: Cheatsheets repository

## Deployment Method
Configurations are deployed via symlinks:
- `~/.zshrc` → `~/.rcfiles/zshrc`
- `~/.tmux.conf` → `~/.rcfiles/tmux.conf`
- `~/.config/nvim` → `~/.rcfiles/nvim/config/nvim`
- `~/.tool-versions` → `~/.rcfiles/tool-versions`
- `~/.config/conky/` → `~/.rcfiles/conky/` (Linux only)

## Target Systems
- **Primary**: Arch Linux
- **Secondary**: macOS (via Homebrew)

## Version Control
- **Main branch**: master
- **Git submodules**: cheatsheets directory
- **Gitignored**: `hostspecific/zsh/*.sh` (machine-specific configs), `*.swp` (vim swap files)
