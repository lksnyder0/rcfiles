# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this directory.

# Neovim Configuration

Modern Neovim config using lazy.nvim, LSP via Mason, Treesitter, and Telescope. The actual config lives in `config/nvim/` and is symlinked to `~/.config/nvim`.

## Directory Structure

```
config/nvim/
├── init.lua                  # Entry point: loads core.lazy, core.keymaps, core.options
├── lua/
│   ├── core/
│   │   ├── lazy.lua          # lazy.nvim bootstrap and plugin loading
│   │   ├── keymaps.lua       # Global keymaps (non-plugin leader bindings)
│   │   └── options.lua       # Editor options (tabs, numbers, etc.)
│   ├── helpers/
│   │   ├── buffers.lua       # Buffer delete utilities
│   │   ├── colorscheme.lua   # Colorscheme loading logic
│   │   └── keys.lua          # map(), lsp_map(), ai_map() helper functions
│   └── plugins/              # One lazy.nvim spec file per plugin group
└── lazy-lock.json            # Plugin version lockfile (commit changes to this)
```

## Adding or Modifying Plugins

1. Create or edit a file in `lua/plugins/` — each file returns a lazy.nvim spec table
2. Use the `map()` / `lsp_map()` helpers from `helpers/keys.lua` for keymaps
3. Reload with `:Lazy sync` or restart Neovim

Plugin files and their contents:

| File | Plugin(s) |
|------|-----------|
| `lsp.lua` | mason.nvim, nvim-lspconfig, fidget, neodev, barbecue, vim-illuminate, lsp-format |
| `cmp.lua` | nvim-cmp, luasnip, friendly-snippets |
| `treesitter.lua` | nvim-treesitter (+ textobjects, movement) |
| `telescope.lua` | telescope.nvim, telescope-fzf-native |
| `git.lua` | gitsigns.nvim, vim-fugitive, git-conflict.nvim |
| `formatting.lua` | formatter.nvim, tidy.nvim |
| `neo-tree.lua` | neo-tree.nvim |
| `themes.lua` | NeoSolarized (default), catppuccin, gruvbox, others |
| `ai.lua` | claudecode.nvim (coder/claudecode.nvim), snacks.nvim |
| `comments.lua` | Comment.nvim |
| `misc.lua` | mini.move, vim-sleuth, vim-illuminate, barbecue |
| `bufferline.lua` | bufferline.nvim |
| `lualine.lua` | lualine.nvim |
| `which-key.lua` | which-key.nvim |
| `databases.lua` | vim-dadbod, vim-dadbod-ui |

## Key Patterns

**Keymap helpers** (`helpers/keys.lua`):
```lua
local map = require("helpers.keys").map
map("n", "<leader>fw", "<cmd>w<cr>", "Write")  -- global keymap

local lsp_map = require("helpers.keys").lsp_map
lsp_map("gd", vim.lsp.buf.definition, bufnr, "Goto Definition")  -- buffer-local LSP keymap
```

**lazy.nvim plugin spec** (typical pattern):
```lua
return {
  "author/plugin-name",
  dependencies = { ... },
  config = function()
    require("plugin-name").setup({ ... })
  end,
}
```

## Leader Key: `<Space>`

### Global Keymaps (`core/keymaps.lua`)

| Key | Action |
|-----|--------|
| `<leader>fw` / `<leader>fa` | Save / save all |
| `<leader>qq` / `<leader>qa` | Quit / force quit all |
| `<leader>dw` | Close window |
| `<leader>db` / `<leader>do` / `<leader>da` | Delete buffer / others / all |
| `<S-h>` / `<S-l>` | Previous / next buffer |
| `<C-h/j/k/l>` | Navigate windows (works in normal and terminal mode) |
| `<C-Up/Down/Left/Right>` | Resize window |
| `<M-h>` / `<M-l>` | Beginning / end of line |
| `<leader>ut` | Toggle dark/light theme |
| `<leader>ur` | Clear search highlights |

### Plugin Keymaps

| Key | Plugin | Action |
|-----|--------|--------|
| `<leader>e` | neo-tree | Toggle file explorer |
| `<leader>sf` | Telescope | Find files |
| `<leader>sg` | Telescope | Live grep (requires ripgrep) |
| `<leader>sw` | Telescope | Search current word |
| `<leader>sh` | Telescope | Search help tags |
| `<leader>sd` | Telescope | Search diagnostics |
| `<leader>fr` | Telescope | Recently opened files |
| `<leader>/` | Telescope | Fuzzy search in current buffer |
| `<leader><space>` | Telescope | Open buffer list |
| `<C-p>` | Telescope | Search keymaps |
| `<leader>L` | lazy.nvim | Open plugin manager UI |
| `<leader>M` | Mason | Open LSP installer UI |
| `<leader>ff` | LSP | Format buffer (`:Format` command) |
| `<leader>lr` / `<leader>la` | LSP | Rename symbol / code action |
| `<leader>ld` / `<leader>ls` | LSP | Type definition / document symbols |
| `gd` / `gD` / `gI` | LSP | Definition / declaration / implementation |
| `gr` | LSP + Telescope | References |
| `K` | LSP | Hover documentation |
| `gx` | LSP | Show diagnostics under cursor |
| `]c` / `[c` | gitsigns | Next / prev hunk |
| `<leader>gh` / `<leader>gr` | gitsigns | Stage / reset hunk |
| `<leader>gs` / `<leader>gu` | gitsigns | Stage buffer / undo stage hunk |
| `<leader>gp` / `<leader>gB` | gitsigns | Preview hunk / blame line |
| `<leader>gtb` / `<leader>gtd` | gitsigns | Toggle line blame / toggle deleted |
| `<leader>gd` | gitsigns | Diff this (working vs index) |
| `<leader>gD` | vim-fugitive | Diff current changes vs HEAD (side-by-side) |
| `co` / `ct` / `c0` / `cb` | git-conflict | Choose ours / theirs / none / both |
| `cn` / `cp` | git-conflict | Next / prev conflict |
| `<leader>te` | tidy.nvim | Toggle trailing whitespace removal |
| `<leader>ac` | claudecode.nvim | Toggle Claude terminal |
| `<leader>af` | claudecode.nvim | Focus Claude |
| `<leader>ar` | claudecode.nvim | Resume Claude (session picker) |
| `<leader>aC` | claudecode.nvim | Continue Claude (last session) |
| `<leader>am` | claudecode.nvim | Select model |
| `<leader>ab` | claudecode.nvim | Add current buffer to context |
| `<leader>as` | claudecode.nvim | Send visual selection |
| `<leader>aa` | claudecode.nvim | Accept diff |
| `<leader>ad` | claudecode.nvim | Reject diff |

### Treesitter Text Objects

| Key | Action |
|-----|--------|
| `af` / `if` | Around/inside function |
| `ac` / `ic` | Around/inside class |
| `aa` / `ia` | Around/inside parameter |
| `]m` / `[m` | Next / prev function start |
| `]]` / `[[` | Next / prev class start |
| `<C-space>` | Expand selection |
| `<C-backspace>` | Shrink selection |

### mini.move

| Key | Action |
|-----|--------|
| `<M-j>` / `<M-k>` | Move line/selection down / up |
| `<M-h>` / `<M-l>` | Move line/selection left / right |

## LSP Servers (auto-installed by Mason)

`dockerls`, `gopls`, `jsonls`, `marksman`, `lua_ls`, `ruff`, `solargraph`, `terraformls`, `yamlls`

## Formatters (formatter.nvim, triggered via LSP `:Format`)

| Language | Tool |
|----------|------|
| Go | gofmt |
| Python | black |
| Ruby | rubocop |
| Terraform/HCL | `tofu fmt` / `packer fmt` |
| JSON | jq |
| Lua | stylua |
| XML | xmlformatter |

tidy.nvim also strips trailing whitespace on save (except markdown and diff files).

## Colorscheme

Default: **NeoSolarized** dark. Toggle with `<leader>ut`. Config in `lua/helpers/colorscheme.lua`. Alternatives in `lua/plugins/themes.lua` (catppuccin, gruvbox, rose-pine, everforest, melange) — uncomment to use.

## Editor Defaults (`lua/core/options.lua`)

4-space indentation, spaces not tabs, no line wrap, relative line numbers, 24-bit color.
