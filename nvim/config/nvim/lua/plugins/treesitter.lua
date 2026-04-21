-- Highlight, edit, and navigate code
return {
	{
		"nvim-treesitter/nvim-treesitter",
		build = ":TSUpdate",
		dependencies = {
			"nvim-treesitter/nvim-treesitter-context",
		},
		config = function()
			-- nvim-treesitter main branch (rewritten for 0.12+) only handles parser installation.
			-- Highlighting and indentation are now native Neovim features that activate
			-- automatically when a parser is installed.
			require("nvim-treesitter").setup({
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
					"markdown_inline",
				},
			})

			require("treesitter-context").setup({
				enable = true,
				on_attach = function(buf)
					return vim.bo[buf].filetype ~= "terraform"
				end,
			})

			-- Disable treesitter highlighting for terraform — the HCL parser
			-- chokes on mixed heredoc syntax (Terraform + Handlebars templates)
			vim.api.nvim_create_autocmd("FileType", {
				pattern = "terraform",
				callback = function(args)
					vim.treesitter.stop(args.buf)
				end,
			})
		end,
	},
}
