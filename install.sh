#!/bin/bash

sudo aptitude install vim-nox tmux zsh curl git

## Install Vundle
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim

## Install OhMyZSH

sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

git clone https://gist.github.com/576268fc0b81b9dd3909.git ~/.rcfiles || exit 1

ln -f -s ~/.rcfiles/vimrc ~/.vimrc

ln -f -s ~/.rcfiles/zshrc ~/.zshrc

ln -f -s ~/.rcfiles/tmux.conf ~/.tmux.conf

vim +PluginInstall +qall
