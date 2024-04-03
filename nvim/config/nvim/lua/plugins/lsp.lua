-- LSP Configuration & Plugins
return {
	{
		"neovim/nvim-lspconfig",
		dependencies = {
			"williamboman/mason.nvim",
			"williamboman/mason-lspconfig.nvim",
			{ "j-hui/fidget.nvim", branch = "legacy" },
			"folke/neodev.nvim",
			"RRethy/vim-illuminate",
			"hrsh7th/cmp-nvim-lsp",
			"lukas-reineke/lsp-format.nvim",
			"utilyre/barbecue.nvim",
			"SmiteshP/nvim-navic",
			"nvim-tree/nvim-web-devicons",
		},
		config = function()
			-- Set up Mason before anything else
			require("mason").setup()
			require("mason-lspconfig").setup({
				ensure_installed = {
					"dockerls",
					-- "docker_compose_language_service",
					"gopls",
					"jsonls",
					"marksman",
					"lua_ls",
					"pylsp",
					"solargraph",
					"terraformls",
				},
				automatic_installation = true,
			})

			-- Quick access via keymap
			require("helpers.keys").map("n", "<leader>M", "<cmd>Mason<cr>", "Show Mason")

			-- Neodev setup before LSP config
			require("neodev").setup()

			-- Turn on LSP status information
			require("fidget").setup()

			-- Barbecue Setup
			vim.opt.updatetime = 200 -- triggers CursorHold event faster
			require("barbecue").setup({
				attach_navic = false, -- prevent barbecue from automatically attaching nvim-navic
				create_autocmd = false,
				show_modified = true,
			})
			vim.api.nvim_create_autocmd({
				"WinResized", -- For nvim >0.9
				"BufWinEnter",
				"CursorHold",
				"InsertLeave",
				"BufModifiedSet", -- If show_modified is true
			}, {
				group = vim.api.nvim_create_augroup("barbecue.updater", {}),
				callback = function()
					require("barbecue.ui").update()
				end,
			})


			-- Set up cool signs for diagnostics
			local signs = { Error = " ", Warn = " ", Hint = " ", Info = " " }
			for type, icon in pairs(signs) do
				local hl = "DiagnosticSign" .. type
				vim.fn.sign_define(hl, { text = icon, texthl = hl, numhl = "" })
			end

			-- Diagnostic config
			local config = {
				virtual_text = false,
				signs = {
					active = signs,
				},
				update_in_insert = true,
				underline = true,
				severity_sort = true,
				float = {
					focusable = true,
					style = "minimal",
					border = "rounded",
					source = "always",
					header = "",
					prefix = "",
				},
			}
			vim.diagnostic.config(config)

			-- This function gets run when an LSP connects to a particular buffer.
			local on_attach = function(client, bufnr)
				local lsp_map = require("helpers.keys").lsp_map

				lsp_map("<leader>lr", vim.lsp.buf.rename, bufnr, "Rename symbol")
				lsp_map("<leader>la", vim.lsp.buf.code_action, bufnr, "Code action")
				lsp_map("<leader>ld", vim.lsp.buf.type_definition, bufnr, "Type definition")
				lsp_map("<leader>ls", require("telescope.builtin").lsp_document_symbols, bufnr, "Document symbols")

				lsp_map("gd", vim.lsp.buf.definition, bufnr, "Goto Definition")
				lsp_map("gr", require("telescope.builtin").lsp_references, bufnr, "Goto References")
				lsp_map("gI", vim.lsp.buf.implementation, bufnr, "Goto Implementation")
				lsp_map("K", vim.lsp.buf.hover, bufnr, "Hover Documentation")
				lsp_map("gD", vim.lsp.buf.declaration, bufnr, "Goto Declaration")

				-- Create a command `:Format` local to the LSP buffer
				vim.api.nvim_buf_create_user_command(bufnr, "Format", function(_)
					vim.lsp.buf.format()
				end, { desc = "Format current buffer with LSP" })

				lsp_map("<leader>ff", "<cmd>Format<cr>", bufnr, "Format")

				-- Attach and configure vim-illuminate
				require("illuminate").on_attach(client)
				require("lsp-format").on_attach(client, bufnr)
				if client.server_capabilities.documentSymbolProvider then
					require("nvim-navic").attach(client, bufnr)
				end
			end

			-- nvim-cmp supports additional completion capabilities, so broadcast that to servers
			local capabilities = vim.lsp.protocol.make_client_capabilities()
			capabilities = require("cmp_nvim_lsp").default_capabilities(capabilities)

			local default_lsp_config = {
				"dockerls", -- Docker
				"docker_compose_language_service",
				"gopls", -- Go
				"marksman", -- Markdown
				"solargraph", -- Ruby
				"terraformls", -- Terraform
				"lemminx", -- XML
				"jsonls", -- JSON
			}
			for _, v in ipairs(default_lsp_config) do
				require("lspconfig")[v].setup({
					on_attach = on_attach,
					capabilities = capabilities,
				})
			end

			-- Go
			-- require("lspconfig")["gopls"].setup({
			-- 	on_attach = on_attach,
			-- 	capabilities = capabilities,
			-- })

			-- JSON
			-- require("lspconfig")["jsonls"].setup({
			-- 	on_attach = on_attach,
			-- 	capabilities = capabilities,
			-- })

			-- Markdown
			-- require("lspconfig")["marksman"].setup({
			-- 	on_attach = on_attach,
			-- 	capabilities = capabilities,
			-- })

			-- Lua
			require("lspconfig")["lua_ls"].setup({
				on_attach = on_attach,
				capabilities = capabilities,
				settings = {
					Lua = {
						completion = {
							callSnippet = "Replace",
						},
						diagnostics = {
							globals = { "vim" },
						},
						workspace = {
							library = {
								[vim.fn.expand("$VIMRUNTIME/lua")] = true,
								[vim.fn.stdpath("config") .. "/lua"] = true,
							},
						},
					},
				},
			})

			-- Python
			require("lspconfig")["pylsp"].setup({
				on_attach = on_attach,
				capabilities = capabilities,
				settings = {
					pylsp = {
						plugins = {
							flake8 = {
								enabled = true,
								maxLineLength = 88, -- Black's line length
							},
							-- Disable plugins overlapping with flake8
							pycodestyle = {
								enabled = false,
							},
							mccabe = {
								enabled = false,
							},
							pyflakes = {
								enabled = false,
							},
							-- Use Black as the formatter
							autopep8 = {
								enabled = false,
							},
						},
					},
				},
			})

			-- Ruby
			-- require("lspconfig")["solargraph"].setup({
			-- 	on_attach = on_attach,
			-- 	capabilities = capabilities,
			-- })

			-- Terraform
			-- require("lspconfig")["terraformls"].setup({
			-- 	on_attach = on_attach,
			-- 	capabilities = capabilities,
			-- })
		end,
	},
}
