# Neovim Configuration

Modern Neovim configuration with LSP support, Treesitter, and lazy-loaded plugins.

## Configuration Structure

```
nvim/config/nvim/
├── init.lua                    # Entry point
├── lua/
│   ├── core/
│   │   ├── lazy.lua            # Plugin manager bootstrap
│   │   ├── keymaps.lua         # Global keymaps
│   │   └── options.lua         # Editor options
│   ├── helpers/
│   │   ├── buffers.lua         # Buffer management utilities
│   │   ├── colorscheme.lua     # Colorscheme loading
│   │   └── keys.lua            # Keymap helper functions
│   └── plugins/                # Plugin specifications (one per category)
│       ├── ai.lua              # GitHub Copilot
│       ├── bufferline.lua      # Buffer tabs
│       ├── cmp.lua             # Autocompletion
│       ├── comments.lua        # Comment.nvim
│       ├── databases.lua       # vim-dadbod
│       ├── formatting.lua      # formatter.nvim, tidy.nvim
│       ├── git.lua             # gitsigns, git-conflict, fugitive
│       ├── graph.lua           # ASCII diagrams
│       ├── lsp.lua             # LSP configuration via Mason
│       ├── lualine.lua         # Statusline
│       ├── misc.lua            # Comment, mini.move, vim-sleuth
│       ├── neo-tree.lua        # File explorer
│       ├── telescope.lua       # Fuzzy finder
│       ├── themes.lua          # Colorschemes
│       ├── treesitter.lua      # Syntax highlighting/parsing
│       └── which-key.lua       # Keybinding hints
```

## Plugin Manager

**lazy.nvim** - Modern plugin manager with lazy-loading support.

- Auto-bootstraps on first launch
- Keybinding: `<leader>L` to open lazy.nvim UI
- Plugins are defined in `lua/plugins/*.lua`

### Adding New Plugins

1. Create or edit a `.lua` file in `nvim/config/nvim/lua/plugins/`
2. Return a lazy.nvim plugin spec table
3. Restart Neovim or run `:Lazy sync`

## Plugins with Dependencies

| Plugin | Purpose | External Dependencies |
|--------|---------|----------------------|
| telescope.nvim | Fuzzy finder | ripgrep, fd, make |
| telescope-fzf-native.nvim | Fast sorting | make, C compiler |
| nvim-treesitter | Syntax parsing | C compiler (gcc/clang) |
| mason.nvim | LSP installer | npm, python3, go |
| copilot.vim | AI assistance | Node.js, GitHub account |
| formatter.nvim | Code formatting | black, rubocop, gofmt, jq, stylua, opentofu |
| vim-dadbod | Database UI | Database clients (psql, mysql, etc.) |

## Keybindings

Leader key: `<Space>`

### File Operations

| Keybinding | Mode | Description |
|------------|------|-------------|
| `<leader>fw` | n | Write (save) current file |
| `<leader>fa` | n | Write all files |
| `<leader>qq` | n | Quit |
| `<leader>qa` | n | Quit all (force) |
| `<leader>dw` | n | Close window |

### Buffer Management

| Keybinding | Mode | Description |
|------------|------|-------------|
| `<S-l>` | n | Next buffer |
| `<S-h>` | n | Previous buffer |
| `<leader>db` | n | Delete current buffer |
| `<leader>do` | n | Delete other buffers |
| `<leader>da` | n | Delete all buffers |
| `<leader><space>` | n | Open buffer list (Telescope) |

### Window Navigation

| Keybinding | Mode | Description |
|------------|------|-------------|
| `<C-h>` | n | Navigate window left |
| `<C-j>` | n | Navigate window down |
| `<C-k>` | n | Navigate window up |
| `<C-l>` | n | Navigate window right |
| `<S-Left>` | n | Move window left |
| `<S-Down>` | n | Move window down |
| `<S-Up>` | n | Move window up |
| `<S-Right>` | n | Move window right |
| `<C-Up>` | n | Resize window (increase height) |
| `<C-Down>` | n | Resize window (decrease height) |
| `<C-Left>` | n | Resize window (increase width) |
| `<C-Right>` | n | Resize window (decrease width) |

### Line Navigation

| Keybinding | Mode | Description |
|------------|------|-------------|
| `<M-h>` | n | Go to beginning of line |
| `<M-l>` | n | Go to end of line |

### UI Toggles

| Keybinding | Mode | Description |
|------------|------|-------------|
| `<leader>ut` | n | Toggle light/dark theme |
| `<leader>ur` | n | Clear search highlights |
| `<leader>?` | n | Show buffer local keymaps (which-key) |
| `<leader>L` | n | Open lazy.nvim UI |
| `<leader>M` | n | Open Mason (LSP installer) |
| `<leader>e` | n, v | Toggle file explorer (Neo-tree) |

### Telescope (Fuzzy Finder)

| Keybinding | Mode | Description |
|------------|------|-------------|
| `<leader>sf` | n | Find files |
| `<leader>sg` | n | Live grep (requires ripgrep) |
| `<leader>sw` | n | Search current word |
| `<leader>sh` | n | Search help tags |
| `<leader>sd` | n | Search diagnostics |
| `<leader>fr` | n | Recently opened files |
| `<leader>/` | n | Search in current buffer |
| `<C-p>` | n | Search keymaps |

### LSP

| Keybinding | Mode | Description |
|------------|------|-------------|
| `gd` | n | Go to definition |
| `gD` | n | Go to declaration |
| `gr` | n | Go to references (Telescope) |
| `gI` | n | Go to implementation |
| `gx` | n | Show diagnostics under cursor |
| `K` | n | Hover documentation |
| `<leader>lr` | n | Rename symbol |
| `<leader>la` | n | Code action |
| `<leader>ld` | n | Type definition |
| `<leader>ls` | n | Document symbols |
| `<leader>ff` | n | Format buffer |

### Git (gitsigns)

| Keybinding | Mode | Description |
|------------|------|-------------|
| `]c` | n | Next hunk |
| `[c` | n | Previous hunk |
| `<leader>gh` | n, v | Stage hunk |
| `<leader>gr` | n | Reset hunk |
| `<leader>gs` | n | Stage buffer |
| `<leader>gu` | n | Undo stage hunk |
| `<leader>gp` | n | Preview hunk |
| `<leader>gB` | n | Blame line (full) |
| `<leader>gtb` | n | Toggle current line blame |
| `<leader>gd` | n | Diff this |
| `<leader>gD` | n | Diff from ~ |
| `<leader>gtd` | n | Toggle deleted lines |
| `ih` | o, x | Select hunk text object |

### Git Conflict Resolution

| Keybinding | Mode | Description |
|------------|------|-------------|
| `co` | n | Choose ours |
| `ct` | n | Choose theirs |
| `c0` | n | Choose none |
| `cb` | n | Choose both |
| `cn` | n | Next conflict |
| `cp` | n | Previous conflict |

### Treesitter

#### Incremental Selection

| Keybinding | Mode | Description |
|------------|------|-------------|
| `<C-space>` | n | Init/increase selection |
| `<C-s>` | n | Scope incremental |
| `<C-backspace>` | n | Decrease selection |

#### Text Objects

| Keybinding | Mode | Description |
|------------|------|-------------|
| `af` / `if` | o, x | Around/inside function |
| `ac` / `ic` | o, x | Around/inside class |
| `aa` / `ia` | o, x | Around/inside parameter |

#### Movement

| Keybinding | Mode | Description |
|------------|------|-------------|
| `]m` | n | Next function start |
| `]M` | n | Next function end |
| `]]` | n | Next class start |
| `][` | n | Next class end |
| `[m` | n | Previous function start |
| `[M` | n | Previous function end |
| `[[` | n | Previous class start |
| `[]` | n | Previous class end |

### GitHub Copilot

| Keybinding | Mode | Description |
|------------|------|-------------|
| `<C-l>` | i | Accept AI suggestion |
| `<C-]>` | i | Next AI suggestion |
| `<C-\>` | i | Dismiss AI suggestion |
| `<leader>ai` | n | Open AI suggestions panel |
| `<leader>ad` | n | Disable AI suggestions |
| `<leader>ae` | n | Enable AI suggestions |

### Comment.nvim

| Keybinding | Mode | Description |
|------------|------|-------------|
| `gcc` | n | Toggle line comment |
| `gbc` | n | Toggle block comment |
| `gc` | v | Toggle line comment (selection) |
| `gb` | v | Toggle block comment (selection) |
| `gco` | n | Comment below and insert |
| `gcO` | n | Comment above and insert |
| `gcA` | n | Comment at end of line |
| `gc{motion}` | n | Comment with motion |
| `gb{motion}` | n | Block comment with motion |

### mini.move

| Keybinding | Mode | Description |
|------------|------|-------------|
| `<M-j>` | n, v | Move line/selection down |
| `<M-k>` | n, v | Move line/selection up |
| `<M-h>` | n, v | Move line/selection left |
| `<M-l>` | n, v | Move line/selection right |

### Formatting

| Keybinding | Mode | Description |
|------------|------|-------------|
| `<leader>te` | n | Toggle tidy.nvim (trailing whitespace) |

## LSP Servers (via Mason)

Automatically installed and configured:

| Server | Language |
|--------|----------|
| dockerls | Dockerfile |
| gopls | Go |
| jsonls | JSON |
| marksman | Markdown |
| lua_ls | Lua |
| ruff | Python |
| solargraph | Ruby |
| terraformls | Terraform/OpenTofu |
| yamlls | YAML |

## Treesitter Languages

Ensured installed for syntax highlighting and code navigation:

- go, lua, python, vim, ruby, terraform
- dockerfile, json, make, markdown_inline
- git_config, git_rebase, gitattributes, gitcommit, gitignore

## Formatters

Configured via formatter.nvim:

| Filetype | Formatter | External Tool |
|----------|-----------|---------------|
| Go | gofmt | Included with Go |
| JSON | jq | `jq` |
| Lua | stylua | `stylua` |
| Python | black | `black` |
| Ruby | rubocop | `rubocop` |
| Terraform/OpenTofu | tofu fmt | `tofu` (opentofu) |
| HCL | packer fmt | `packer` |
| XML | xmlformatter | `xmlformatter` |
| * | Remove trailing whitespace | Built-in |

Additionally, **tidy.nvim** automatically removes trailing whitespace on save (except for markdown and diff files).

## Colorscheme

Default: **NeoSolarized** (dark mode)

Configuration in `lua/helpers/colorscheme.lua`:
- Style: dark (toggle with `<leader>ut`)
- Italics enabled for comments, keywords, strings
- Bold for function names

Available alternatives (uncomment to use):
- catppuccin
- gruvbox
- rose-pine
- everforest
- melange

## Editor Options

Configured in `lua/core/options.lua`:

| Option | Value | Description |
|--------|-------|-------------|
| shiftwidth | 4 | Indent width |
| tabstop | 4 | Tab character width |
| expandtab | true | Use spaces instead of tabs |
| wrap | false | No line wrapping |
| number | true | Show line numbers |
| relativenumber | true | Relative line numbers |
| termguicolors | true | 24-bit color support |

## Plugin Details

### telescope.nvim
Fuzzy finder for files, buffers, grep, and more. Uses fzf-native for fast sorting when available.

### nvim-treesitter
Advanced syntax highlighting and code navigation using tree-sitter parsers. Includes textobjects for selecting functions, classes, and parameters.

### mason.nvim + nvim-lspconfig
LSP server management and configuration. Mason handles installation, lspconfig handles setup.

### gitsigns.nvim
Git decorations in the sign column, inline blame, and hunk operations.

### neo-tree.nvim
File explorer sidebar with git status integration.

### copilot.vim
GitHub Copilot integration with custom highlight colors for solarized theme.

### Comment.nvim
Smart commenting with support for multiple languages via treesitter.

### which-key.nvim
Popup showing available keybindings when pressing leader key.

### lualine.nvim
Statusline with file info, git branch, and diagnostics.

### bufferline.nvim
Buffer tabs at the top of the editor.

### barbecue.nvim
VSCode-like breadcrumbs showing current location in file (via nvim-navic).

### vim-illuminate
Highlights other uses of the word under cursor.

### vim-sleuth
Automatically detects buffer indentation settings.
