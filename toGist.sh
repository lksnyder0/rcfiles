#!/bin/bash

DATE=`date "+%F %T"`

echo "Updating zshrc"
cp ~/.zshrc zshrc
echo "Updating vimrc"
cp ~/.vimrc vimrc
echo "Updating tmux"
cp ~/.tmux.conf tmux.conf
git add .
git commit -m "Update: $DATE"
git push origin master
