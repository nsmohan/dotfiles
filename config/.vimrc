"----Display------
colorscheme desert 

"---Settings-----
set hlsearch
set tabstop=4
set shiftwidth=4
set expandtab
set list
set listchars=tab:>-
filetype indent plugin on

"------Brackets---------
inoremap {{ {<CR>}<Esc>ko
inoremap [[ []<Esc>i
inoremap (( ()<Esc>i
inoremap "" ""<Esc>i

"--Set numbering format
set number relativenumber
augroup numbertoggle
  autocmd!
  autocmd BufEnter,FocusGained,InsertLeave * set relativenumber
  autocmd BufLeave,FocusLost,InsertEnter   * set norelativenumber
augroup END

"---Show Tab number-----
set guitablabel=%N:%M%t

"---Keymappings-------
nmap <S-Enter> O<Esc>j
nmap <CR> o<Esc>k

"--Enable Ctrl C for clip board--
vnoremap cc "+y
vnoremap cx "+x
map cv "+gP
