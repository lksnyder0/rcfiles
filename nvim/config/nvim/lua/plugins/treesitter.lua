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

			-- nvim-treesitter (archived master) registers query directives with
			-- `{ all = false }` as a Neovim 0.10 compat shim. On 0.12 that option
			-- is silently ignored: `match[capture_id]` is always TSNode[], so the
			-- legacy handlers crash with "attempt to call method 'range' (a nil
			-- value)" when they treat the array as a single node. Re-register the
			-- offenders (#set-lang-from-info-string! used by markdown,
			-- #downcase! used by hcl/bash/ruby/php) with array-aware versions.
			local tsq = vim.treesitter.query
			local function unwrap(nodes)
				return type(nodes) == "table" and nodes[1] or nodes
			end
			local lang_aliases = {
				ex = "elixir",
				pl = "perl",
				sh = "bash",
				uxn = "uxntal",
				ts = "typescript",
			}
			tsq.add_directive("set-lang-from-info-string!", function(match, _, bufnr, pred, metadata)
				local node = unwrap(match[pred[2]])
				if not node then
					return
				end
				local alias = vim.treesitter.get_node_text(node, bufnr):lower()
				local ft = vim.filetype.match({ filename = "a." .. alias })
				metadata["injection.language"] = ft or lang_aliases[alias] or alias
			end, { force = true })
			tsq.add_directive("downcase!", function(match, _, bufnr, pred, metadata)
				local id = pred[2]
				local node = unwrap(match[id])
				if not node then
					return
				end
				local text = vim.treesitter.get_node_text(node, bufnr, { metadata = metadata[id] }) or ""
				if not metadata[id] then
					metadata[id] = {}
				end
				metadata[id].text = string.lower(text)
			end, { force = true })

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
