# ZSH Configuration

ZSH configuration using [oh-my-zsh](https://ohmyz.sh/) framework with custom aliases, functions, and settings.

## Framework & Theme

- **Framework**: oh-my-zsh
- **Theme**: bira (chosen over powerlevel10k for simplicity and faster startup)

## Custom Aliases

### Configuration Editing

| Alias | Command | Description |
|-------|---------|-------------|
| `c_nvim` | `$EDITOR ~/.config/nvim` | Edit Neovim configuration |
| `c_zsh` | `$EDITOR ~/.zshrc` | Edit ZSH configuration |
| `c_ohmyzsh` | `$EDITOR ~/.oh-my-zsh` | Edit oh-my-zsh directory |

### Configuration Reload

| Alias | Command | Description |
|-------|---------|-------------|
| `r_zsh` | `source ~/.zshrc` | Reload ZSH configuration |
| `r_p10k` | `p10k reload` | Reload p10k theme (if using) |

### GitHub PR Workflow

| Alias | Command | Description |
|-------|---------|-------------|
| `prc` | `gh pr create -a '@me'` | Create PR assigned to self |
| `prcd` | `gh pr create -a '@me' --draft` | Create draft PR assigned to self |
| `prr` | `gh pr ready` | Mark PR as ready for review |
| `prv` | `gh pr view -w` | View PR in browser |
| `prm` | `gh pr merge` | Merge PR |
| `prma` | `gh pr merge --auto` | Enable auto-merge on PR |

### Utility Aliases

| Alias | Command | Description |
|-------|---------|-------------|
| `lah` | `ls -lah` | List all files with human-readable sizes |
| `neo` | `cd ${HOME}/code && tmux` | Navigate to code directory and start tmux |
| `kubectl` | `kubecolor` | Colorized kubectl output |

### Privacy Aliases

| Alias | Command | Description |
|-------|---------|-------------|
| `incognito` | `unset HISTFILE` | Disable shell history recording |
| `cognito` | `set HISTFILE=~/.zsh_history` | Re-enable shell history recording |

### Work-Specific Aliases (Examples)

These are examples of work-specific aliases that may need customization:

| Alias | Command | Description |
|-------|---------|-------------|
| `rt` | `ttt roll https://ttt.idex.huntress.io rampart luke` | Work-specific: TTT roll command |
| `rr` | `gh pr edit --add-reviewer huntresslabs/idex` | Work-specific: Add team as reviewer |

## Custom Shell Functions

Functions are located in `zfunc/` and autoloaded via `autoload -Uz <function_name>`.

### avs

AWS Vault execution wrapper for running commands with assumed roles.

```bash
avs <profile> <command>
```

**Example:**
```bash
avs production aws s3 ls
```

### liftoff

Spacelift authentication and jets launcher for infrastructure management.

```bash
liftoff <space_id>
```

Handles Spacelift token caching - use `unset SPACELIFT_TOKEN` to re-authenticate.

### update_rcfiles

Pull latest rcfiles from remote repository including submodules.

```bash
update_rcfiles
```

### commit_rcfiles

Stage and commit all changes in rcfiles repository.

```bash
commit_rcfiles
```

### g_branch_clean

Clean up merged git branches (excludes `main` and current branch).

```bash
g_branch_clean
```

## Custom Settings & Rationale

### Theme Choice: bira

```bash
ZSH_THEME="bira"
```

**Rationale**: Chosen over powerlevel10k for simplicity. While p10k is more feature-rich, bira provides a clean, fast-loading prompt without external font dependencies.

### Completion Waiting Dots

```bash
COMPLETION_WAITING_DOTS="true"
```

**Rationale**: Provides visual feedback during slow tab completions, especially useful with large directories or remote file systems.

### Command Correction

```bash
ENABLE_CORRECTION="true"
```

**Rationale**: Suggests corrections for mistyped commands, saving time on typos.

### History Format

```bash
HIST_STAMPS="yyyy-mm-dd"
```

**Rationale**: ISO 8601 date format for consistent, sortable history timestamps.

### Performance Optimizations

```bash
DISABLE_MAGIC_FUNCTIONS="true"
DISABLE_COMPFIX="true"
DISABLE_AUTO_UPDATE="true"
```

**Rationale**: These settings reduce shell startup time by disabling features that add latency:
- `DISABLE_MAGIC_FUNCTIONS`: Skips URL auto-escaping which can cause paste delays
- `DISABLE_COMPFIX`: Skips permission checks on completion directories
- `DISABLE_AUTO_UPDATE`: Manual updates preferred for controlled environments

### Pipenv Virtual Environment Location

```bash
export PIPENV_VENV_IN_PROJECT=1
```

**Rationale**: Creates `.venv/` inside project directories instead of `~/.local/share/virtualenvs/`. Benefits:
- Easier to locate project virtual environments
- Simplifies cleanup (delete project = delete venv)
- Works better with IDE detection

### AWS Vault Backend

```bash
export AWS_VAULT_BACKEND="keychain"
```

**Rationale**: Uses macOS Keychain for secure credential storage. On Linux, change to `"file"` or `"kwallet"`.

### SSH Agent Forwarding

```zsh
zstyle :omz:plugins:ssh-agent agent-forwarding on
```

**Rationale**: Enables SSH agent forwarding for seamless key usage across SSH sessions.

## Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `ZSH` | `$HOME/.oh-my-zsh` | oh-my-zsh installation path |
| `EDITOR` | `nvim` | Default editor |
| `PIPENV_VENV_IN_PROJECT` | `1` | Project-local virtual environments |
| `AWS_VAULT_BACKEND` | `keychain` | AWS Vault credential storage |
| `ZSH_TMUX_AUTOSTART` | `false` | Don't auto-start tmux |

### PATH Additions

The following directories are added to PATH:

```bash
${HOME}/.local/bin           # User-local binaries
/usr/local/go/bin            # Go installation
${HOME}/go/bin               # Go workspace binaries
${ASDF_DATA_DIR}/shims       # asdf-managed tools
/opt/homebrew/Caskroom       # Homebrew Casks (macOS)
$HOME/.rvm/bin               # Ruby Version Manager
$HOME/.poetry/bin            # Python Poetry
```

## oh-my-zsh Plugins

| Plugin | Description |
|--------|-------------|
| alias-finder | Suggests aliases for typed commands |
| archlinux | Arch Linux package management shortcuts |
| asdf | asdf version manager integration |
| aws | AWS CLI completions and helpers |
| docker | Docker command completions |
| git | Git aliases and completions |
| github | GitHub CLI integration |
| gpg-agent | GPG agent management |
| kubectl | Kubernetes CLI completions |
| kubectx | Kubernetes context/namespace switching |
| ssh-agent | SSH agent auto-start and key management |
| terraform | Terraform command completions |
| tmux | tmux integration and helpers |
| zsh-interactive-cd | Interactive cd with file preview |
| zsh-navigation-tools | Enhanced history and file navigation |

## Host-Specific Configuration

Machine-specific configurations are placed in `hostspecific/zsh/*.sh` and sourced automatically. These files are:

- **Ephemeral**: Not tracked in git
- **Machine-specific**: Environment variables, paths, or aliases unique to a machine
- **Auto-sourced**: All `.sh` files in the directory are loaded

**Example use cases:**
- Work-specific environment variables
- Machine-specific PATH additions
- Local aliases that don't belong in the shared config

## Completion Optimization

```bash
autoload -Uz compinit
if [ "$(date +'%j')" != "$(stat -f '%Sm' -t '%j' ~/.zcompdump 2>/dev/null)" ]; then
    compinit
else
    compinit -C
fi
```

**Rationale**: Only regenerates the completion cache once per day, significantly reducing startup time on subsequent shell launches.

## Custom Prompt Modification

```bash
export RPROMPT="%F{green}$AWS_VAULT%f$RPROMPT"
```

**Rationale**: Displays the current AWS Vault session in the right prompt, providing visibility into which AWS profile is active without cluttering the main prompt.
