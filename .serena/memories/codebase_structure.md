# rcfiles - Codebase Structure

## Directory Layout

```
.rcfiles/
├── nvim/                      # Neovim configuration
│   └── config/nvim/
│       ├── init.lua           # Entry point
│       └── lua/
│           ├── core/          # Core configuration
│           │   ├── lazy.lua   # lazy.nvim bootstrap
│           │   ├── keymaps.lua # General keybindings
│           │   └── options.lua # Vim options
│           ├── plugins/       # Plugin specifications (lazy.nvim)
│           │   ├── lsp.lua
│           │   ├── cmp.lua
│           │   ├── treesitter.lua
│           │   ├── telescope.lua
│           │   ├── git.lua
│           │   ├── neo-tree.lua
│           │   ├── themes.lua
│           │   ├── formatting.lua
│           │   ├── databases.lua
│           │   ├── ai.lua
│           │   ├── misc.lua
│           │   ├── bufferline.lua
│           │   ├── lualine.lua
│           │   ├── which-key.lua
│           │   └── comments.lua
│           └── helpers/       # Utility modules
│               ├── buffers.lua
│               ├── keys.lua
│               └── colorscheme.lua
├── zshrc                      # Main ZSH configuration
├── zfunc/                     # Custom ZSH functions (autoloaded)
│   ├── avs                    # aws-vault wrapper
│   ├── liftoff                # Spacelift authentication
│   ├── update_rcfiles         # Pull latest rcfiles
│   ├── commit_rcfiles         # Commit rcfiles changes
│   └── g_branch_clean         # Git branch cleanup
├── tmux.conf                  # tmux configuration
├── conky/                     # Conky configurations (Linux)
│   ├── conky-ac.conf
│   ├── conky-battery.conf
│   └── conky-power-aware.sh
├── hostspecific/zsh/          # Machine-specific configs (NOT committed)
├── tool-versions              # asdf version definitions
├── cheatsheets/               # Git submodule
├── docs/                      # Documentation
│   ├── zsh.md
│   ├── neovim.md
│   ├── tmux.md
│   └── conky.md
├── install-arch.sh            # Automated installation script (Arch Linux)
├── test-environment.sh        # Environment verification script
└── .claude/CLAUDE.md          # Project instructions for Claude
```

## Key Files

### Neovim
- **init.lua**: Loads core modules (lazy, keymaps, options)
- **plugins/*.lua**: Each file is a lazy.nvim plugin spec
- Plugin system uses lazy.nvim (auto-bootstraps on first launch)

### ZSH
- **zshrc**: Main configuration with oh-my-zsh framework
- **zfunc/***: Custom functions loaded via `autoload -Uz`

### Configuration Files
- **.gitignore**: Excludes `*.swp` and `hostspecific/zsh/*.sh`
- **tool-versions**: asdf version manager definitions
