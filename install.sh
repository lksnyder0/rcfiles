#!/bin/bash

sudo apt-get install -y vim-nox tmux zsh curl git

reset

## Install Vundle
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim

## Install OhMyZSH

sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

sudo usermod -s /bin/zsh luke

git clone https://gitlab.com/lksnyder0/rcfiles.git ~/.rcfiles || exit 1
git submodule init
git submodule update

ln -f -s ~/.rcfiles/vimrc ~/.vimrc

ln -f -s ~/.rcfiles/zshrc ~/.zshrc

ln -f -s ~/.rcfiles/tmux.conf ~/.tmux.conf

vim +PluginInstall +qall
