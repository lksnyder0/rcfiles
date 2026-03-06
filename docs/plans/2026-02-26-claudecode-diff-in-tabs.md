# claudecode.nvim Diff View in New Tab Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Open the claudecode.nvim diff view in a new tab instead of splitting the current window.

**Architecture:** Add `diff_opts = { open_in_new_tab = true }` to the existing `opts` table in `ai.lua`. This uses the plugin's built-in config option — no handler patching required.

**Tech Stack:** Neovim Lua config, lazy.nvim, claudecode.nvim

---

### Task 1: Add `diff_opts` to claudecode.nvim opts

**Files:**
- Modify: `nvim/config/nvim/lua/plugins/ai.lua:139-143`

**Step 1: Open the file and locate the `opts` table**

The current `opts` block starts at line 139 and looks like this:

```lua
opts = {
  terminal = {
    split_width_percentage = 0.40,
  },
},
```

**Step 2: Add `diff_opts` to the table**

Change the block to:

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

**Step 3: Verify the file looks correct**

Read `nvim/config/nvim/lua/plugins/ai.lua` lines 139–148 and confirm the structure matches exactly — no extra commas, correct nesting.

**Step 4: Manually test in Neovim**

1. Restart Neovim (or run `:Lazy reload claudecode.nvim`)
2. Open a file and ask Claude to edit it
3. Confirm the diff view opens in a **new tab** (tab bar shows a new entry) rather than splitting the current window
4. Accept the diff with `<leader>aa` and confirm the accepted file opens in a new tab

**Step 5: Commit**

```bash
git add nvim/config/nvim/lua/plugins/ai.lua
git commit -c commit.gpgsign=false -m "feat(nvim): open claudecode diff view in new tab"
```
