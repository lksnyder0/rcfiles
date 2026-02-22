# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# rcfiles - Dotfiles Repository

Personal dotfiles for Linux and macOS environments.

## Repository

https://github.com/lksnyder0/rcfiles

## Common Commands

```bash
# Verify environment after installation
./test-environment.sh

# Install everything on Arch Linux
./install-arch.sh

# Deploy AI tool configs (Claude global CLAUDE.md, Serena)
./deploy-ai-configs.sh personal   # personal machine
./deploy-ai-configs.sh work       # work machine (configs not committed)

# Scan AI configs for secrets/sensitive data
./scripts/check-ai-configs.sh

# Check git security setup
./scripts/setup-security-tools.sh
```

## Project Structure

```
.rcfiles/
├── nvim/config/nvim/     # Neovim config (symlinked to ~/.config/nvim)
│   └── lua/plugins/      # lazy.nvim plugin specs (one file per plugin group)
├── zshrc                 # ZSH config (oh-my-zsh + bira theme)
├── zfunc/                # Custom ZSH functions (autoloaded)
├── tmux.conf             # Tmux config
├── conky/                # Conky configs (Linux-only, power-aware)
├── ai-configs/           # AI tool configs (Claude, Serena, Context7)
│   ├── claude/           # CLAUDE-personal.md / CLAUDE-work.md
│   └── serena/           # serena_config.yml.example
├── scripts/              # Security and setup utility scripts
├── hostspecific/zsh/     # Machine-specific ZSH (ephemeral, NOT committed)
├── docs/                 # Per-tool documentation
├── deploy-ai-configs.sh  # Deploys AI configs to global locations (~/.claude/, ~/.serena/)
├── install-arch.sh       # Full automated install for Arch Linux
└── test-environment.sh   # Post-install environment verification
```

## Deployment

Configs are deployed via symlinks:
- `~/.zshrc` -> `~/.rcfiles/zshrc`
- `~/.tmux.conf` -> `~/.rcfiles/tmux.conf`
- `~/.config/nvim` -> `~/.rcfiles/nvim/config/nvim`
- `~/.tool-versions` -> `~/.rcfiles/tool-versions`
- `~/.config/conky/` -> `~/.rcfiles/conky/` (Linux only)

AI configs are deployed differently - `deploy-ai-configs.sh` symlinks `ai-configs/claude/CLAUDE-personal.md` (or `-work.md`) to `~/.claude/CLAUDE.md`.

---

## Neovim Configuration

### Plugin Manager
- **lazy.nvim** - auto-bootstraps on first launch
- Leader key: `<Space>`

### Plugin Structure
Each file in `nvim/config/nvim/lua/plugins/` is a lazy.nvim plugin spec:

| File | Purpose |
|------|---------|
| `lsp.lua` | LSP configuration via Mason |
| `cmp.lua` | Autocompletion (nvim-cmp) |
| `treesitter.lua` | Syntax highlighting/parsing |
| `telescope.lua` | Fuzzy finder |
| `git.lua` | Git integration (gitsigns, fugitive, git-conflict) |
| `neo-tree.lua` | File explorer |
| `themes.lua` | Colorschemes |
| `formatting.lua` | Code formatters (formatter.nvim, tidy.nvim) |
| `databases.lua` | Database UI (vim-dadbod) |
| `ai.lua` | GitHub Copilot |
| `misc.lua` | Comment.nvim, mini.move, vim-sleuth |
| `bufferline.lua` | Buffer tabs |
| `lualine.lua` | Statusline |
| `which-key.lua` | Keybinding hints |

### LSP Servers (via Mason)
Automatically installed: `dockerls`, `gopls`, `jsonls`, `marksman`, `lua_ls`, `ruff`, `solargraph`, `terraformls`, `yamlls`

### Formatters
| Language | Formatter |
|----------|-----------|
| Go | gofmt |
| Python | black |
| Ruby | rubocop |
| Terraform/HCL | terraform fmt / packer fmt |
| JSON | jq |
| Lua | stylua |
| XML | xmlformatter |

### Adding New Plugins
1. Create a new `.lua` file in `nvim/config/nvim/lua/plugins/`
2. Return a lazy.nvim plugin spec table
3. Restart neovim or run `:Lazy sync`

---

## ZSH Configuration

- **Framework**: oh-my-zsh with **bira** theme
- **Functions** (`zfunc/`): autoloaded via `autoload -Uz` in zshrc
- **Host-specific**: `hostspecific/zsh/*.sh` sourced automatically - **do NOT commit these files**

### Custom Functions
| Function | Purpose |
|----------|---------|
| `avs` | aws-vault exec wrapper: `avs <profile> <command>` |
| `liftoff` | Spacelift authentication and jets launcher |
| `update_rcfiles` | Pull latest rcfiles |
| `commit_rcfiles` | Commit rcfiles changes |
| `g_branch_clean` | Clean up git branches |

### Key Aliases
- `c_nvim`, `c_zsh` - Edit configs
- `r_zsh` - Reload zshrc
- `prc`, `prcd`, `prv`, `prm` - GitHub PR workflow shortcuts
- `neo` - cd to ~/code and start tmux
- `incognito` / `cognito` - Toggle shell history

---

## Tmux Configuration

- **Prefix**: `C-a` (not default C-b)
- Pane navigation: vim-style `hjkl`
- Split: `|` (horizontal), `-` (vertical)
- New named window: `C-a C`
- Reload config: `C-a r`

---

## Documentation Maintenance

When making changes, keep docs in sync:

| Change | Update |
|--------|--------|
| Aliases / ZSH functions | `docs/zsh.md` |
| Neovim keybindings, LSP, formatters | `docs/neovim.md` |
| Tmux keybindings | `docs/tmux.md` |
| Conky configuration | `docs/conky.md` |
| AI tool configs | `docs/ai-tools.md` |

---

## AI Agent Workflow (Serena)

1. Run the `activate_project` tool from Serena before making any edits.
2. Work in two distinct phases:
   - **PLANNING**: use `switch_modes` with `["planning", "one-shot", "no-onboarding"]`
   - **EXECUTION**: use `switch_modes` with `["editing", "interactive", "no-onboarding"]`
