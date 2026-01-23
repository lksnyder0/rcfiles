-- See current buffers at the top of the editor
return {
	{
		"github/copilot.vim",
		config = function()
			-- Set CopilotSuggestion highlight for solarized colorscheme
			-- This makes the suggestion text a darker gray for better visibility
			-- on ColorScheme event, set the highlight for CopilotSuggestion
			-- You can change the color values as per your preference
			--
			vim.api.nvim_create_autocmd('ColorScheme', {
				pattern = '*',
				callback = function()
					vim.api.nvim_set_hl(0, 'CopilotSuggestion', { fg = '#b58900', ctermfg = 8, force = true })
				end,
			})
		end
	},
}
