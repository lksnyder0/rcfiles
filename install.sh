#!/bin/bash


## Setup Terraform for later
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt-get update
sudo apt-get install -y python3-pip python3-dev tmux git zsh stow squashfuse npm terraform terraform-ls ruby ruby-dev python3-venv

## Install OhMyZSH

sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

## Install NPM
curl -qL https://www.npmjs.com/install.sh | sh

## Install Go
curl -o go.tar.gz https://dl.google.com/go/go1.21.6.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go.tar.gz

## Install Neovim
mkdir ~/.local/bin
curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim.appimage
chmod u+x nvim.appimage
mv nvim.appimage ~/.local/bin/

## Get Solargraph (ruby lsp)
sudo gem install solargraph

git clone https://gitlab.com/lksnyder0/rcfiles.git ~/.rcfiles || exit 1

cd ~/.rcfiles

git submodule init
git submodule update

mkdir -p ~/.config

ln -f -s ~/.rcfiles/nvim/config/nvim ~/.config/nvim

ln -f -s ~/.rcfiles/zshrc ~/.zshrc

ln -f -s ~/.rcfiles/tmux.conf ~/.tmux.conf

ln -f -s ~/.rcfiles/p10k.zsh ~/.p10k.zsh

ln -f -s ~/.rcfiles/tool-versions ~/.tool-versions

cd nvim

python3 -m pip install requirements.devbox.txt

cd ~/.config/nvim
