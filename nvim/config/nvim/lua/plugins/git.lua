-- Git related plugins
return {
	{
		"lewis6991/gitsigns.nvim",
		opts = {},
		config = function()
			require("gitsigns").setup {
				on_attach = function(client, bufnr)
					local gs = package.loaded.gitsigns

					local function map(mode, l, r, opts)
						opts = opts or {}
						opts.buffer = bufnr
						vim.keymap.set(mode, l, r, opts)
					end

					-- Navigation
					map('n', ']c', function()
						if vim.wo.diff then return ']c' end
						vim.schedule(function() gs.next_hunk() end)
						return '<Ignore>'
					end, { expr = true })

					map('n', '[c', function()
						if vim.wo.diff then return '[c' end
						vim.schedule(function() gs.prev_hunk() end)
						return '<Ignore>'
					end, { expr = true })

					-- Actions
					map('n', '<leader>gh', gs.stage_hunk, { desc = "Stage hunk" })
					map('n', '<leader>gr', gs.reset_hunk, { desc = "Reset hunk" })
					map('v', '<leader>gh', function() gs.stage_hunk { vim.fn.line('.'), vim.fn.line('v') } end,
						{ desc = "Stage highlighted hunk" })
					map('v', '<leader>gr', function() gs.reset_hunk { vim.fn.line('.'), vim.fn.line('v') } end,
						{ desc = "Reset highlighted hunk" })
					map('n', '<leader>gs', gs.stage_buffer, { desc = "Stage buffer" })
					map('n', '<leader>gu', gs.undo_stage_hunk, { desc = "Undo stage hunk" })
					map('n', '<leader>gr', gs.reset_buffer, { desc = "Reset buffer" })
					map('n', '<leader>gp', gs.preview_hunk, { desc = "Preview hunk" })
					map('n', '<leader>gB', function() gs.blame_line { full = true } end,
						{ desc = "Peak current line blame" })
					map('n', '<leader>gtb', gs.toggle_current_line_blame, { desc = "Toggle current line blame" })
					map('n', '<leader>gd', gs.diffthis, { desc = "Show diff" })
					map('n', '<leader>gD', function() vim.cmd("Gdiffsplit HEAD") end, { desc = "Diff current changes" })
					map('n', '<leader>gtd', gs.toggle_deleted, { desc = "Toggle deleted lines" })

					-- Text object
					map({ 'o', 'x' }, 'ih', ':<C-U>Gitsigns select_hunk<CR>')
				end
			}
		end
	},
	{
		"akinsho/git-conflict.nvim",
		opts = {
			default_mappings = {
				ours = "co",
				theirs = "ct",
				none = "c0",
				both = "cb",
				next = "cn",
				prev = "cp",
			},
			highlights = { -- They must have background color, otherwise the default color will be used
				incoming = 'DiffAdd',
				current = 'DiffText',
			},
			debug = false,
			disable_diagnostics = false
		},
	},
	{
		"tpope/vim-fugitive",
		-- config = function()
		-- 	local map = require("helpers.keys").map
		-- 	map("n", "<leader>ga", "<cmd>Git add %<cr>", "Stage the current file")
		-- 	map("n", "<leader>gb", "<cmd>Git blame<cr>", "Show the blame")
		-- end
	}
}
