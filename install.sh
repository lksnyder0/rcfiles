#!/bin/bash

git clone git@gist.github.com:576268fc0b81b9dd3909.git ~/.rcfile || exit 1

ln -s ~/.rcfiles/vimrc ~/.vimrc

ln -s ~/.rcfiles/zshrc ~/.zshrc

ln -s ~/.rcfiles/tmux.conf ~/.tmux.conf

