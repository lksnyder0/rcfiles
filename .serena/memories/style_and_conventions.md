# rcfiles - Style and Conventions

## Lua (Neovim Configuration)

### File Organization
- Each plugin gets its own file in `nvim/config/nvim/lua/plugins/`
- Each file returns a lazy.nvim plugin spec table
- Core configuration separated into `lua/core/` directory
- Helper functions in `lua/helpers/` directory

### Naming Conventions
- Files: lowercase with hyphens (e.g., `which-key.lua`, `neo-tree.lua`)
- Module structure follows Neovim conventions

### Plugin Specification Structure
```lua
return {
  "author/plugin-name",
  dependencies = { ... },
  config = function()
    -- Plugin configuration
  end,
  keys = { ... },  -- Lazy-loaded keybindings
}
```

### Configuration Patterns
- Use `vim.opt` for setting options
- Use `vim.keymap.set()` for keybindings
- Leader key is `<Space>`
- Lazy-load plugins where possible using `keys`, `cmd`, or `ft`

## Bash/Shell (ZSH Functions)

### Function Structure
- Functions defined in separate files in `zfunc/` directory
- Use subshell syntax: `function_name () ( ... )` for isolation
- Functions are autoloaded via `autoload -Uz` in zshrc

### Naming Conventions
- Lowercase with underscores (e.g., `update_rcfiles`, `commit_rcfiles`)
- Prefix with context where appropriate (e.g., `g_branch_clean` for git)

## Markdown Documentation

### Structure
- Use tables for structured information
- Include code blocks with language specification
- Maintain consistency with existing documentation format
- Update multiple doc files when changes affect multiple tools

### Documentation Update Requirements
- Adding/modifying aliases → Update `docs/zsh.md`
- Adding/modifying keybindings → Update relevant doc
- Adding/removing plugins → Update plugin tables
- Adding zfunc functions → Update `docs/zsh.md`
- Changing LSP servers/formatters → Update `docs/neovim.md`
- Conky changes → Update `docs/conky.md`

## Git Conventions

### Branches
- Main branch: `master`
- Direct commits to master for dotfiles changes

### Commit Messages
- Clear, descriptive messages
- Reference tool being modified (e.g., "Add neovim plugin for...", "Update zsh alias for...")

### Files to Ignore
- `*.swp` - Vim swap files
- `hostspecific/zsh/*.sh` - Machine-specific configs (ephemeral)
