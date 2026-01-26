-- Highlight, edit, and navigate code
return {
	{
		"nvim-treesitter/nvim-treesitter",
		build = function()
			pcall(require("nvim-treesitter.install").update({ with_sync = true }))
		end,
		dependencies = {
			-- "nvim-treesitter/nvim-treesitter-textobjects",
			"nvim-treesitter/nvim-treesitter-context",
		},
		config = function()
			require("nvim-treesitter").setup({
				-- Add languages to be installed here that you want installed for treesitter
				ensure_installed = {
					"go",
					"lua",
					"python",
					"vim",
					"ruby",
					"terraform",
					"dockerfile",
					"git_config",
					"git_rebase",
					"gitattributes",
					"gitcommit",
					"gitignore",
					"json",
					"make",
					"markdown_inline"
				},

				highlight = { enable = true },
				indent = { enable = true, disable = { "gitignore", "git_config", "git_rebase", "gitattributes", "gitcommit" } },
				incremental_selection = {
					enable = true,
					keymaps = {
						init_selection = "<c-space>",
						node_incremental = "<c-space>",
						scope_incremental = "<c-s>",
						node_decremental = "<c-backspace>",
					},
				},
				-- I need to understand this more.
				-- textobjects = {
				-- 	select = {
				-- 		enable = true,
				-- 		lookahead = true, -- Automatically jump forward to textobj, similar to targets.vim
				-- 		keymaps = {
				-- 			-- You can use the capture groups defined in textobjects.scm
				-- 			["aa"] = "@parameter.outer",
				-- 			["ia"] = "@parameter.inner",
				-- 			["af"] = "@function.outer",
				-- 			["if"] = "@function.inner",
				-- 			["ac"] = "@class.outer",
				-- 			["ic"] = "@class.inner",
				-- 		},
				-- 	},
				-- 	move = {
				-- 		enable = true,
				-- 		set_jumps = true, -- whether to set jumps in the jumplist
				-- 		goto_next_start = {
				-- 			["]m"] = "@function.outer",
				-- 			["]]"] = "@class.outer",
				-- 		},
				-- 		goto_next_end = {
				-- 			["]M"] = "@function.outer",
				-- 			["]["] = "@class.outer",
				-- 		},
				-- 		goto_previous_start = {
				-- 			["[m"] = "@function.outer",
				-- 			["[["] = "@class.outer",
				-- 		},
				-- 		goto_previous_end = {
				-- 			["[M"] = "@function.outer",
				-- 			["[]"] = "@class.outer",
				-- 		},
				-- 	},
				-- },
			})
		end,
	},
}
