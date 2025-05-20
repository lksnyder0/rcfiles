-- Fetch and setup colorscheme if available, otherwise just return 'default'
-- This should prevent Neovim from complaining about missing colorschemes on first boot
local function get_if_available(name, opts)
	local lua_ok, colorscheme = pcall(require, name)
	if lua_ok then
		colorscheme.setup(opts)
		return name
	end

	local vim_ok, _ = pcall(vim.cmd.colorscheme, name)
	if vim_ok then
		return name
	end

	return "default"
end

local neosolarized_opts = {
	-- style = "light",
	style = "dark",
	transparent = false,
	terminal_colors = false,
	enable_italics = true,
	styles = {
		-- Style to be applied to different syntax groups
		comments = { italic = true },
		keywords = { italic = true },
		functions = { bold = true },
		variables = {},
		string = { italic = true },
		underline = true, -- true/false; for global underline
		undercurl = true, -- true/false; for global undercurl
	},
	-- Add specific hightlight groups
	on_highlights = function(highlights, colors)
		-- highlights.Include.fg = colors.red -- Using `red` foreground for Includes
	end,
}
-- Uncomment the colorscheme to use
-- local colorscheme = get_if_available("catppuccin")
-- local colorscheme = get_if_available('gruvbox')
-- local colorscheme = get_if_available('rose-pine')
-- local colorscheme = get_if_available('everforest')
-- local colorscheme = get_if_available('melange')
local colorscheme = get_if_available("NeoSolarized", neosolarized_opts)
return colorscheme
