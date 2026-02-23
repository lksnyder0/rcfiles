return {
	{
		"coder/claudecode.nvim",
		dependencies = { "folke/snacks.nvim" },
		config = function(_, opts)
			-- Patch openFile to open files in new tabs instead of replacing the current buffer.
			-- Must run before setup() so the patched handler gets registered via register_all().
			local open_file = require("claudecode.tools.open_file")
			open_file.handler = function(params)
				if not params.filePath then
					error({ code = -32602, message = "Invalid params", data = "Missing filePath parameter" })
				end

				local file_path = vim.fn.expand(params.filePath)

				if vim.fn.filereadable(file_path) == 0 then
					error({ code = -32000, message = "File operation error", data = "File not found: " .. file_path })
				end

				local preview = params.preview or false
				local make_frontmost = params.makeFrontmost ~= false
				local select_to_end_of_line = params.selectToEndOfLine or false
				local message = "Opened file: " .. file_path

				if preview then
					vim.cmd("pedit " .. vim.fn.fnameescape(file_path))
				else
					vim.cmd("tabedit " .. vim.fn.fnameescape(file_path))
					-- tabedit reuses an existing buffer without reloading from disk.
					-- Re-read the file so external writes (e.g. by Claude) are visible.
					if not vim.bo.modified then
						vim.cmd("edit")
					end
				end

				if not make_frontmost then
					vim.cmd("tabprevious")
				end

				-- Handle text selection by line numbers
				if params.startLine or params.endLine then
					local start_line = params.startLine or 1
					local end_line = params.endLine or start_line

					local start_pos = { start_line - 1, 0 }
					local end_pos = { end_line - 1, -1 }

					vim.api.nvim_buf_set_mark(0, "<", start_pos[1], start_pos[2], {})
					vim.api.nvim_buf_set_mark(0, ">", end_pos[1], end_pos[2], {})
					vim.cmd("normal! gv")

					message = "Opened file and selected lines " .. start_line .. " to " .. end_line
				end

				-- Handle text pattern selection
				if params.startText then
					local buf = vim.api.nvim_get_current_buf()
					local lines = vim.api.nvim_buf_get_lines(buf, 0, -1, false)
					local start_line_idx, start_col_idx
					local end_line_idx, end_col_idx

					for line_idx, line in ipairs(lines) do
						local col_idx = string.find(line, params.startText, 1, true)
						if col_idx then
							start_line_idx = line_idx - 1
							start_col_idx = col_idx - 1
							break
						end
					end

					if start_line_idx then
						if params.endText then
							for line_idx = start_line_idx + 1, #lines do
								local line = lines[line_idx]
								if line then
									local col_idx = string.find(line, params.endText, 1, true)
									if col_idx then
										end_line_idx = line_idx
										end_col_idx = col_idx + string.len(params.endText) - 1
										if select_to_end_of_line then
											end_col_idx = string.len(line)
										end
										break
									end
								end
							end

							if end_line_idx then
								message = 'Opened file and selected text from "'
									.. params.startText
									.. '" to "'
									.. params.endText
									.. '"'
							else
								end_line_idx = start_line_idx
								end_col_idx = start_col_idx + string.len(params.startText) - 1
								message = 'Opened file and positioned at "'
									.. params.startText
									.. '" (end text "'
									.. params.endText
									.. '" not found)'
							end
						else
							end_line_idx = start_line_idx
							end_col_idx = start_col_idx + string.len(params.startText) - 1
							message = 'Opened file and selected text "' .. params.startText .. '"'
						end

						vim.api.nvim_win_set_cursor(0, { start_line_idx + 1, start_col_idx })
						vim.api.nvim_buf_set_mark(0, "<", start_line_idx, start_col_idx, {})
						vim.api.nvim_buf_set_mark(0, ">", end_line_idx, end_col_idx, {})
						vim.cmd("normal! gv")
						vim.cmd("normal! zz")
					else
						message = 'Opened file, but text "' .. params.startText .. '" not found'
					end
				end

				if make_frontmost then
					return {
						content = { { type = "text", text = message } },
					}
				else
					local buf = vim.api.nvim_get_current_buf()
					local detailed_info = {
						success = true,
						filePath = file_path,
						languageId = vim.api.nvim_buf_get_option(buf, "filetype"),
						lineCount = vim.api.nvim_buf_line_count(buf),
					}
					return {
						content = { { type = "text", text = vim.json.encode(detailed_info, { indent = 2 }) } },
					}
				end
			end

			require("claudecode").setup(opts)
		end,
		opts = {
			terminal = {
				split_width_percentage = 0.40,
			},
		},
		keys = {
			{ "<leader>ac", "<cmd>ClaudeCode<cr>", desc = "Toggle Claude" },
			{ "<leader>af", "<cmd>ClaudeCodeFocus<cr>", desc = "Focus Claude" },
			{ "<leader>ar", "<cmd>ClaudeCode --resume<cr>", desc = "Resume Claude" },
			{ "<leader>aC", "<cmd>ClaudeCode --continue<cr>", desc = "Continue Claude" },
			{ "<leader>am", "<cmd>ClaudeCodeSelectModel<cr>", desc = "Select model" },
			{ "<leader>ab", "<cmd>ClaudeCodeAdd %<cr>", desc = "Add buffer" },
			{ "<leader>as", "<cmd>ClaudeCodeSend<cr>", mode = "v", desc = "Send selection" },
			{ "<leader>aa", "<cmd>ClaudeCodeDiffAccept<cr>", desc = "Accept diff" },
			{ "<leader>ad", "<cmd>ClaudeCodeDiffDeny<cr>", desc = "Reject diff" },
		},
	},
}