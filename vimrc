set nocompatible

filetype indent plugin on
" filetype off

" Enable syntax highlighting
syntax on

" Font setting
" set guifont=Sauce\ Code\ Powerline\ Regular\ 10

let data_dir = has('nvim') ? stdpath('data') . '/site' : '~/.vim'
if empty(glob(data_dir . '/autoload/plug.vim'))
  silent execute '!curl -fLo '.data_dir.'/autoload/plug.vim --create-dirs  https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

call plug#begin('~/.vim/plugged')
" Install the Asynchronous Lint Engine (ALE)
Plug 'dense-analysis/ale'
" Fuzzy file, buffer, mru, tag, etc.
Plug 'ctrlpvim/ctrlp.vim'
" File tree pane
Plug 'scrooloose/nerdtree'
" Useful modeline
Plug 'bling/vim-airline'
" " Syntax checker
" Plug 'scrooloose/syntastic'
" Python autocomplete
Plug 'davidhalter/jedi-vim'
" Worlds best git integration
Plug 'tpope/vim-fugitive'
" Auto inserts/delete brackets, parens, quote pairs.
Plug 'jiangmiao/auto-pairs'
" Add Black support for python projects
Plug 'psf/black', {'branch': 'stable'}

call plug#end()

filetype plugin indent on

" -----------------------------------------------------------
" End Vundle

" " Start Syntastic
"
" set statusline+=%#warningmsg#
" set statusline+=%{SyntasticStatuslineFlag()}
" set statusline+=%*
"
" let g:syntastic_always_populate_loc_list = 1
" let g:syntastic_auto_loc_list = 1
" let g:syntastic_check_on_open = 1
" let g:syntastic_check_on_wq = 0
" let g:syntastic_quiet_messages = { "type": "style"  }
"
" " End Syntastic

" Start Airline
"
let g:airline_powerline_fonts = 1
"
" End Airline

" Start NERDTree

autocmd vimenter * NERDTree
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTreeType") && b:NERDTreeType == "primary") | q | endif

" End NERDTree

" Start ALE
let g:ale_linters = {'python': ['flake8', 'bandit', 'pydocstyle']}
let g:ale_fixers = {'*': ['remove_trailing_lines', 'trim_whitespace'], 'python': ['black', 'isort']}
" Set this variable to 1 to fix files when you save them.
let g:ale_python_flake8_options = '--max-line-length=88'
let g:ale_fix_on_save = 1
let g:ale_python_pyls_executable = "pylsp"
let g:ale_python_pyls_config = {
\   'pylsp': {
\     'plugins': {
\       'pycodestyle': {
\         'enabled': v:false,
\       },
\       'pyflakes': {
\         'enabled': v:false,
\       },
\       'pydocstyle': {
\         'enabled': v:false,
\       },
\     },
\   },
\}
" End ALE

" Start Black
" " Automatically run black on save
" augroup black_on_save
"   autocmd!
"   autocmd BufWritePre *.py Black
" augroup end
" " Run black on F9
" nnoremap <F9> :Black<CR>
" End Black
"
"Allows the reuse of a window without saving the buffer. BE CAREFUL!
set hidden

" Better command-line completion
set wildmenu

" Show partial commands in the last line of the screen
set showcmd

" Highlight searches (use <C-L> to temporarily turn off highlighting; see the
" mapping of <C-L> below)
set hlsearch

" Use case insensitive search, except when using capital letters
set ignorecase
set smartcase

" Allow backspacing over autoindent, line breaks and start of insert action
set backspace=indent,eol,start

" When opening a new line and no filetype-specific indenting is enabled, keep
" the same indent as the line you're currently on. Useful for READMEs, etc.
set autoindent

" Stop certain movements from always going to the first character of a line.
" While this behaviour deviates from that of Vi, it does what most users
" coming from other editors would expect.
set nostartofline

" Display the cursor position on the last line of the screen or in the status
" line of a window
set ruler

" Always display the status line, even if only one window is displayed
set laststatus=2

" Instead of failing a command because of unsaved changes, instead raise a
" dialogue asking if you wish to save changed files.
set confirm

" Use visual bell instead of beeping when doing something wrong
set visualbell

" And reset the terminal code for the visual bell. If visualbell is set, and
" this line is also included, vim will neither flash nor beep. If visualbell
" is unset, this does nothing.
" set t_vb=

" Enable use of the mouse for all modes
" set mouse=a

" Set the command window height to 2 lines, to avoid many cases of having to
" press <Enter> to continue"
" set cmdheight=2

" Display relative line numbers as well as the current line number.
" When in insert mode, only absolute line numbers are displayed
" Display line numbers on the left when in insert mode
set number relativenumber

" Quickly time out on keycodes, but never time out on mappings
set notimeout ttimeout ttimeoutlen=200

" Use <F5> to toggle between 'paste' and 'nopaste'
set pastetoggle=<f5>


"------------------------------------------------------------
" Indentation options
"
" Indentation settings for using 4 spaces instead of tabs.
" Do not change 'tabstop' from its default value of 8 with this setup.
set shiftwidth=4
set softtabstop=4
set expandtab

augroup langindention
  autocmd!
  autocmd FileType yaml setlocal shiftwidth=2 softtabstop=2
  autocmd FileType vim setlocal shiftwidth=2 softtabstop=2
  autocmd FileType python setlocal shiftwidth=4 softtabstop=4
augroup END

"------------------------------------------------------------
" Mappings
"
" Useful mappings

" Map Y to act like D and C, i.e. to yank until EOL, rather than act as yy,
" which is the default
map Y y$

" Map <C-L> (redraw screen) to also turn off search highlighting until the
" next search
nnoremap <C-L> :nohl<CR><C-L>

"------------------------------------------------------------
" Setting view options

set viewoptions=cursor,folds,slash,unix

" Edit vimr configuration file
nnoremap confe :e $MYVIMRC<CR>
" Reload vims configuration file
nnoremap confr :source $MYVIMRC<CR>

" Load all plugins now.
" Plugins need to be added to runtimepath before helptags can be generated.
packloadall
" Load all of the helptags now, after plugins have been loaded.
" All messages and errors will be ignored.
silent! helptags ALL
