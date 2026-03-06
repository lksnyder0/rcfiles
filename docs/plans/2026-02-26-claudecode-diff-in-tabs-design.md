# Design: claudecode.nvim Diff View in New Tab

**Date:** 2026-02-26

## Problem

When Claude proposes an edit, the diff view (before/after split) opens in the current tab, splitting the existing window. After accepting, `openFile` fires and opens the file in yet another split panel. The result is an increasingly fragmented window layout.

## Goal

The diff view should open in a new tab, keeping the workflow tab-based and consistent with the existing `openFile` override (which already uses `tabedit`).

## Solution

Use the built-in `diff_opts.open_in_new_tab` configuration option in `claudecode.nvim`.

### Change

In `nvim/config/nvim/lua/plugins/ai.lua`, add `diff_opts` to the existing `opts` table:

```lua
opts = {
  terminal = {
    split_width_percentage = 0.40,
  },
  diff_opts = {
    open_in_new_tab = true,
  },
},
```

### Expected Flow After Change

1. Claude proposes edit → diff opens in a **new tab** with before/after split
2. `<leader>aa` (accept) → diff tab closes, `openFile` fires → file opens in a new tab via existing handler
3. `<leader>ad` (reject) → diff tab closes, returns to previous tab

## Scope

- **File changed:** `nvim/config/nvim/lua/plugins/ai.lua`
- **Lines changed:** Add 3 lines to the `opts` table
- **No other changes required**

## Alternatives Considered

- **Patch `open_diff` handler** (like the existing `openFile` patch): Maximum control but high maintenance burden; rejected in favor of the official config API.
- **Suppress post-accept `openFile`**: Could reduce tab count but requires controlling Claude's MCP call flow; not straightforward.
