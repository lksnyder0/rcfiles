#!/bin/bash

git pull

echo "Updating zshrc"
cp zshrc ~/.zshrc
echo "Updating vimrc"
cp vimrc ~/.vimrc
echo "Updating tmux"
cp tmux.conf ~/.tmux.conf
