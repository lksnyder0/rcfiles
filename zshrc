# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
# if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
#   source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
# fi

if (( ! ${fpath[(I)/usr/local/share/zsh/site-functions]}  )); then
      FPATH=/usr/local/share/zsh/site-functions:$FPATH
fi
# Path to your oh-my-zsh installation.
export ZSH=$HOME/.oh-my-zsh

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
#ZSH_THEME="blinks"
# ZSH_THEME="bira"
ZSH_THEME="powerlevel10k/powerlevel10k"
# ZSH_THEME="robbyrussell"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"
COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# ssh-agent settings
zstyle :omz:plugins:ssh-agent agent-forwarding on

# tmux settings
export ZSH_TMUX_AUTOSTART=false

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
  docker
  tmux
  zsh-navigation-tools
  ssh-agent
  archlinux
  zsh-interactive-cd
  git
  github
  terraform
  gpg-agent
)

source $ZSH/oh-my-zsh.sh

# User configuration

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:${HOME}/.local/bin:/usr/local/go/bin:${HOME}/go/bin"
# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

export EDITOR='nvim'

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
alias config_zsh="$EDITOR ~/.zshrc"
alias config_ohmyzsh="$EDITOR ~/.oh-my-zsh"
alias config_nvim="$EDITOR ~/.config/nvim"

alias reload_zsh="source ~/.zshrc"
alias reload_p10k="p10k reload"
alias lah="ls -lah"
alias incognito=" unset HISTFILE"
alias cognito="set HISTFILE=~/.zsh_history"
alias rex_ttt="ttt roll -port 443 https://ttt.stotlers.com rampart ${USERNAME}"
alias rex_ttt2="ttt roll -port 443 https://ttt.stotlers.com rampart2 ${USERNAME}"
alias rex_review="gh pr edit --add-reviewer 'huntresslabs/infra-devex'"

alias pr_create="gh pr create -a '@me' --draft"
alias pr_ready="gh pr ready"

alias enter_the_matrix="cd ${HOME}/code && tmux"

for FILE in `find ~/.rcfiles/hostspecific/zsh -name "*.sh"`; do
    source $FILE
done

# Add RVM to PATH for scripting. Make sure this is the last PATH variable change.
export PATH="$PATH:$HOME/.rvm/bin"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
# export PYENV_ROOT="$HOME/.pyenv"
# command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
# eval "$(pyenv init -)"
# aws-vault completions
eval "$(curl -fs https://raw.githubusercontent.com/99designs/aws-vault/master/contrib/completions/zsh/aws-vault.zsh)"

export PIPENV_VENV_IN_PROJECT=1

export PATH="$HOME/.poetry/bin:$PATH"

# export AWS_VAULT_BACKEND="file"
export AWS_VAULT_BACKEND="secret-service"
. "$HOME/.asdf/asdf.sh"
# append completions to fpath
fpath=(${ASDF_DIR}/completions $fpath)
# initialise completions with ZSH's compinit
autoload -Uz compinit && compinit

## Add custom functions
FPATH=${HOME}/.rcfiles/zfunc:$FPATH
autoload -Uz update_rcfiles
autoload -Uz commit_rcfiles
autoload -Uz avs
autoload -Uz liftoff
autoload -Uz g_branch_clean

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
