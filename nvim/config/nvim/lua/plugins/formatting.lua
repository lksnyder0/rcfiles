return {
	{
		"mcauley-penney/tidy.nvim",
		opts = {
			filetype_exclude = { "markdown", "diff" }
		},
		init = function()
			vim.keymap.set('n', "<leader>te", require("tidy").toggle, { desc = "Toggle Tidy" })
		end
	},
	{
		"mhartington/formatter.nvim",
		config = function()
			-- local util = require("formatter.util")
			require("formatter").setup({
				logging = true,
				log_level = vim.log.levels.DEBUG,
				filetype = {
					go = {
						require("formatter.filetypes.go").gofmt
					},
					json = {
						require("formatter.filetypes.json").jq
					},
					lua = {
						require("formatter.filetypes.lua").stylus
					},
					python = {
						require("formatter.filetypes.python").black
					},
					ruby = {
						require("formatter.filetypes.ruby").rubocup
					},
					terraform = {
					function()
						return {
							exe = "tofu",
							args = {
								"fmt",
								"-",
							},
							stdin = true,
						}
					end
				},
				tf = {
					function()
						return {
							exe = "tofu",
							args = {
								"fmt",
								"-",
							},
							stdin = true,
						}
					end
				},
					hcl = {
						function()
							return {
								exe = "packer",
								args = {
									"fmt",
									"-",
								},
								stdin = true,
							}
						end
					},
					xml = {
						require("formatter.filetypes.xml").xmlformatter
					},
					["*"] = {
						require("formatter.filetypes.any").remove_trailing_whitespace
					}
				}
			})
		end,
	}
}
