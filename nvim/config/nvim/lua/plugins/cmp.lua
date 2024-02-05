-- Autocompletion
return {
	{
		"hrsh7th/nvim-cmp",
		dependencies = {
			"hrsh7th/cmp-nvim-lsp",
			"hrsh7th/cmp-nvim-lua",
			"hrsh7th/cmp-buffer",
			"FelipeLema/cmp-async-path",
			"L3MON4D3/LuaSnip",
			"saadparwaiz1/cmp_luasnip",
			"rafamadriz/friendly-snippets",
			"petertriho/cmp-git",
		},
		config = function()
			local cmp = require("cmp")
			local luasnip = require("luasnip")
			local format = require("cmp_git.format")
			local sort = require("cmp_git.sort")

			require("luasnip/loaders/from_vscode").lazy_load()

			require("cmp_git").setup({
				filetypes = { "gitcommit", "octo" },
				remotes = { "origin", "upstream" },
				enableRemoteUrlRewrites = false,
				git = {
					commits = {
						limit = 100,
						sort_by = sort.git.commits,
						format = format.git.commits,
					},
				},
				github = {
					issues = {
						fields = { "title", "number", "body", "updatedAt", "state" },
						filter = "all", -- assigned, created, mentioned, subscribed, all, repos
						limit = 100,
						state = "open", -- open, closed, all
						sort_by = sort.github.issues,
						format = format.github.issues,
					},
					mentions = {
						limit = 100,
						sort_by = sort.github.mentions,
						format = format.github.mentions,
					},
					pull_requests = {
						fields = { "title", "number", "body", "updatedAt", "state" },
						limit = 100,
						state = "open", -- open, closed, merged, all
						sort_by = sort.github.pull_requests,
						format = format.github.pull_requests,
					},
				},
				trigger_actions = {
					{
						debug_name = "git_commits",
						trigger_character = ":",
						action = function(sources, trigger_char, callback, params, git_info)
							return sources.git:get_commits(callback, params, trigger_char)
						end,
					},
					{
						debug_name = "github_issues_and_pr",
						trigger_character = "#",
						action = function(sources, trigger_char, callback, params, git_info)
							return sources.github:get_issues_and_prs(callback, git_info, trigger_char)
						end,
					},
					{
						debug_name = "github_mentions",
						trigger_character = "@",
						action = function(sources, trigger_char, callback, params, git_info)
							return sources.github:get_mentions(callback, git_info, trigger_char)
						end,
					},
				},
			})

			local kind_icons = {
				Text = "",
				Method = "m",
				Function = "",
				Constructor = "",
				Field = "",
				Variable = "",
				Class = "",
				Interface = "",
				Module = "",
				Property = "",
				Unit = "",
				Value = "",
				Enum = "",
				Keyword = "",
				Snippet = "",
				Color = "",
				File = "",
				Reference = "",
				Folder = "",
				EnumMember = "",
				Constant = "",
				Struct = "",
				Event = "",
				Operator = "",
				TypeParameter = "",
			}

			cmp.setup({
				snippet = {
					expand = function(args)
						luasnip.lsp_expand(args.body)
					end,
				},
				mapping = cmp.mapping.preset.insert({
					["<C-k>"] = cmp.mapping.select_prev_item(),
					["<C-j>"] = cmp.mapping.select_next_item(),
					["<C-d>"] = cmp.mapping.scroll_docs(-4),
					["<C-f>"] = cmp.mapping.scroll_docs(4),
					["<CR>"] = cmp.mapping.confirm({
						behavior = cmp.ConfirmBehavior.Replace,
						select = false,
					}),
					["<Tab>"] = cmp.mapping(function(fallback)
						if cmp.visible() then
							cmp.select_next_item()
						elseif luasnip.expand_or_jumpable() then
							luasnip.expand_or_jump()
						else
							fallback()
						end
					end, { "i", "s" }),
					["<S-Tab>"] = cmp.mapping(function(fallback)
						if cmp.visible() then
							cmp.select_prev_item()
						elseif luasnip.jumpable(-1) then
							luasnip.jump(-1)
						else
							fallback()
						end
					end, { "i", "s" }),
				}),
				formatting = {
					fields = { "kind", "abbr", "menu" },
					format = function(entry, vim_item)
						-- Kind icons
						vim_item.kind = string.format("%s", kind_icons[vim_item.kind])
						vim_item.menu = ({
							nvim_lsp = "[LSP]",
							luasnip = "[Snippet]",
							buffer = "[Buffer]",
							path = "[Path]",
						})[entry.source.name]
						return vim_item
					end,
				},
				sources = {
					{ name = "nvim_lsp" },
					{ name = "luasnip" },
					{ name = "buffer" },
					{ name = "async_path" },
					{ name = "git" },
				},
			})
		end,
	},
}
