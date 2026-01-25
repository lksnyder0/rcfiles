# rcfiles - Key Technologies and Patterns

## Neovim Plugin System

### lazy.nvim
- **Plugin manager**: Lazy-loading plugin manager
- **Bootstrap location**: `nvim/config/nvim/lua/core/lazy.lua`
- **Plugin specs**: Each file in `nvim/config/nvim/lua/plugins/` is auto-loaded
- **Lock file**: `lazy-lock.json` tracks installed plugin versions
- **UI access**: `<leader>L` opens lazy.nvim interface

### Plugin Loading Pattern
```lua
-- Each plugin file returns a spec table or array of specs
return {
  "author/plugin-name",
  dependencies = { "other/plugin" },
  config = function()
    require("plugin-name").setup({ ... })
  end,
  lazy = true,  -- Lazy load
  keys = { ... },  -- Load on keypress
  cmd = { ... },   -- Load on command
}
```

### LSP Configuration (Mason)
- **Mason**: LSP server installer
- **Auto-installed servers**: dockerls, gopls, jsonls, marksman, lua_ls, ruff, solargraph, terraformls, yamlls
- **Configuration**: `nvim/config/nvim/lua/plugins/lsp.lua`
- **Access**: `:Mason` command

### Treesitter
- **Purpose**: Syntax highlighting and parsing
- **Ensured parsers**: go, lua, python, vim, ruby, terraform, dockerfile, git_config, git_rebase, gitattributes, gitcommit, gitignore, json, make, markdown_inline
- **Configuration**: `nvim/config/nvim/lua/plugins/treesitter.lua`

### Formatters
| Language | Formatter | Plugin |
|----------|-----------|--------|
| Go | gofmt | formatter.nvim |
| Python | black | formatter.nvim |
| Ruby | rubocop | formatter.nvim |
| Terraform/HCL/OpenTofu | tofu fmt / packer fmt | formatter.nvim |
| JSON | jq | formatter.nvim |
| Lua | stylua | formatter.nvim |
| XML | xmlformatter | formatter.nvim |

## ZSH Framework

### oh-my-zsh
- **Framework**: Popular ZSH configuration framework
- **Theme**: bira
- **Installation**: Via official install script
- **Plugins used**: alias-finder, archlinux, asdf, aws, docker, git, github, gpg-agent, kubectl, kubectx, ssh-agent, terraform, tmux, zsh-interactive-cd, zsh-navigation-tools

### Function Autoloading
- **Pattern**: Functions in `zfunc/` are autoloaded
- **Mechanism**: `autoload -Uz <function_name>` in zshrc
- **Execution**: Functions run in subshells for isolation

## tmux Configuration

### Key Bindings
- **Prefix**: Changed from default `C-b` to `C-a`
- **Pane navigation**: vim-style `hjkl`
- **Splitting**: `|` for horizontal, `-` for vertical
- **Color scheme**: Solarized-inspired

## asdf Version Manager

### Purpose
- Manage runtime versions for multiple languages/tools
- Single `.tool-versions` file for all tools
- **Tools managed**: ruby, nodejs, yarn, packer, aws-vault, python

### Usage Pattern
```bash
asdf install          # Install all versions from .tool-versions
asdf list            # Show installed versions
asdf current         # Show active versions
```

## Conky (Linux-only)

### Power-Aware Design
- Two configurations: `conky-ac.conf` (AC power), `conky-battery.conf` (battery)
- Launcher script: `conky-power-aware.sh` selects appropriate config
- Displays: hostname, kernel, uptime, system resources, time/date

## Git Submodules

### Cheatsheets
- **Location**: `cheatsheets/` directory
- **Purpose**: vim and tmux reference cheatsheets
- **Update**: `git submodule update && git submodule sync`

## Symlink-Based Deployment

### Pattern
- Source files remain in `~/.rcfiles/`
- Symlinks created in expected locations (`~/.zshrc`, `~/.config/nvim`, etc.)
- Allows easy updates via `git pull` without moving files
- Changes immediately reflected in active configuration

### Benefits
- Single source of truth in git repository
- Easy to update across machines
- Simple rollback via git
