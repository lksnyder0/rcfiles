# rcfiles - Dotfiles Repository

Personal dotfiles for Linux and macOS environments.

**Repository**: https://gitlab.com/lksnyder0/rcfiles

## Project Structure

```
.rcfiles/
├── nvim/                 # Neovim configuration (primary editor)
│   └── config/nvim/      # Symlinked to ~/.config/nvim
├── zshrc                 # ZSH configuration (oh-my-zsh)
├── zfunc/                # Custom ZSH functions (autoloaded)
├── tmux.conf             # Tmux configuration
├── conky/                # Conky configs (Linux-only)
├── hostspecific/zsh/     # Machine-specific configs (ephemeral, not committed)
├── tool-versions         # asdf version definitions
├── cheatsheets/          # Git submodule with vim/tmux cheatsheets
└── docs/                 # Tool-specific documentation
```

## Deployment

Configs are deployed via symlinks:
- `~/.zshrc` -> `~/.rcfiles/zshrc`
- `~/.tmux.conf` -> `~/.rcfiles/tmux.conf`
- `~/.config/nvim` -> `~/.rcfiles/nvim/config/nvim`
- `~/.tool-versions` -> `~/.rcfiles/tool-versions`
- `~/.config/conky/` -> `~/.rcfiles/conky/` (Linux only)

---

## Neovim Configuration

### Plugin Manager
- **lazy.nvim** - Plugins auto-bootstrap on first launch
- Leader key: `<Space>`
- Access lazy.nvim UI: `<leader>L`

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

### Treesitter Languages
Ensured: go, lua, python, vim, ruby, terraform, dockerfile, git_config, git_rebase, gitattributes, gitcommit, gitignore, json, make, markdown_inline

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

### Framework & Theme
- **oh-my-zsh** with **bira** theme
- Completion waiting dots enabled

### oh-my-zsh Plugins
alias-finder, archlinux, asdf, aws, docker, git, github, gpg-agent, kubectl, kubectx, ssh-agent, terraform, tmux, zsh-interactive-cd, zsh-navigation-tools

### Custom Functions (zfunc/)
| Function | Purpose |
|----------|---------|
| `avs` | aws-vault exec wrapper: `avs <profile> <command>` |
| `liftoff` | Spacelift authentication and jets launcher |
| `update_rcfiles` | Pull latest rcfiles |
| `commit_rcfiles` | Commit rcfiles changes |
| `g_branch_clean` | Clean up git branches |

Functions are autoloaded via `autoload -Uz <function_name>` in zshrc.

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
- Solarized-inspired color scheme
- Status bar shows: hostname, kernel, uptime, time/date

---

## Conky (Linux-only)

Power-aware configuration:
- `conky-ac.conf` - Used when on AC power
- `conky-battery.conf` - Used when on battery
- `conky-power-aware.sh` - Launcher that selects appropriate config

---

## asdf Tool Versions

Managed versions (in `tool-versions`):
- ruby, nodejs, yarn, packer, aws-vault, python

---

## Host-Specific Configuration

Machine-specific ZSH configs are placed in `hostspecific/zsh/*.sh` and sourced automatically. These files are **ephemeral** and should NOT be committed.

---

## Documentation Maintenance

When making changes to this repository, keep documentation in sync:

### Update Triggers
- **Adding/modifying aliases** → Update `docs/zsh.md`
- **Adding/modifying keybindings** → Update relevant doc (`docs/neovim.md`, `docs/tmux.md`)
- **Adding/removing plugins** → Update plugin tables in relevant docs
- **Adding new zfunc functions** → Update `docs/zsh.md`
- **Changing LSP servers or formatters** → Update `docs/neovim.md`
- **Conky configuration changes** → Update `docs/conky.md`

### Documentation Structure
- `README.md` - Primary entry point, installation instructions
- `docs/zsh.md` - ZSH configuration details
- `docs/neovim.md` - Neovim configuration details
- `docs/tmux.md` - Tmux configuration details
- `docs/conky.md` - Conky configuration details (Linux-only)

### Guidelines
1. Follow existing documentation patterns and table formats
2. Include descriptions for all aliases and keybindings
3. Document external dependencies for plugins
4. Mark work-specific configurations as examples
5. Run the `activate_project` tool from serena before making any considerations about or edits to the project.
6. Work in two distinct phases. Start in the PLANNING phase before moving to the EXECUTION phase.
7. When in the PLANNING phase use the `switch_modes` tool to set the modes to `["planning", "one-shot", "no-onboarding"]`.
8. When in the EXECUTION phase use the `switch_modes` tool to set the modes to `["editing", "interactive", "no-onboarding"]`.
9. Review this list to ensure you're ready to work successfully.

