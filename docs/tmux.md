# tmux Configuration

Terminal multiplexer configuration with vim-style navigation and solarized-inspired colors.

## Quick Start

| Action | Keybinding |
|--------|------------|
| Prefix key | `C-a` (Ctrl+a) |
| Split horizontally | `C-a |` |
| Split vertically | `C-a -` |
| Navigate panes | `C-a h/j/k/l` |
| Reload config | `C-a r` |

## Keybindings

All keybindings use `C-a` as the prefix (changed from default `C-b` for vim compatibility).

### Session/Window Management

| Keybinding | Description |
|------------|-------------|
| `C-a C` | Create new named window (prompts for name) |
| `C-a c` | Create new window (inherits current path) |
| `C-a a` | Send prefix to nested tmux session |
| `C-a C-a` | Switch to last window |

### Pane Navigation (vim-style)

| Keybinding | Description |
|------------|-------------|
| `C-a h` | Select pane left |
| `C-a j` | Select pane down |
| `C-a k` | Select pane up |
| `C-a l` | Select pane right |

### Pane Splitting

| Keybinding | Description |
|------------|-------------|
| `C-a |` | Split horizontally (side by side) |
| `C-a -` | Split vertically (top and bottom) |
| `C-a "` | Split vertically (top and bottom) |
| `C-a %` | Split horizontally (side by side) |
| `C-a s` | Split vertically (top and bottom) |
| `C-a v` | Split horizontally (side by side) |

All split commands preserve the current pane's working directory.

### Configuration

| Keybinding | Description |
|------------|-------------|
| `C-a r` | Reload tmux configuration |

## Options & Settings

### General

| Option | Value | Rationale |
|--------|-------|-----------|
| `prefix` | `C-a` | More accessible than C-b, vim-friendly |
| `base-index` | 1 | Window numbering starts at 1, not 0 |
| `escape-time` | 0 | No delay for escape key (better vim experience) |
| `aggressive-resize` | on | Windows resize to smallest *client viewing that window* |

### Window Naming

| Option | Value | Rationale |
|--------|-------|-----------|
| `automatic-rename` | on | Windows auto-rename to current command |
| `automatic-rename-format` | `#{b:pane_current_path}` | Show directory name as window title |

### Activity Monitoring

| Option | Value | Rationale |
|--------|-------|-----------|
| `monitor-activity` | on | Highlight windows with activity |
| `visual-activity` | on | Show message when activity detected |

### Colors

| Option | Value |
|--------|-------|
| `default-terminal` | `screen-256color` |
| `status-bg` | colour235 (base02 - dark gray) |
| `status-fg` | colour136 (yellow) |
| `display-panes-active-colour` | colour33 (blue) |
| `display-panes-colour` | colour166 (orange) |
| `clock-mode-colour` | green |

## Status Bar

### Layout

```
Left: hostname | kernel-version
Right: uptime | time | date
```

### Left Status

Shows:
- Hostname (green)
- Kernel version (first 6 characters)

### Right Status

Shows:
- Uptime
- Time (12-hour format with seconds)
- Date (YYYY-MM-DD)

### Customization

The status bar is intentionally minimal with no external dependencies. If you want to add system metrics, you can modify `status-right` in `tmux.conf`.

## External Dependencies

This tmux configuration has **no external dependencies**. All features work with a standard tmux installation.

## Version Compatibility

The configuration includes version checks for tmux 1.8+ features:
- Path preservation in splits
- New window creation with current path

These features are conditionally enabled for backwards compatibility.

## Color Theme

Inspired by [tmux-colors-solarized](https://github.com/seebi/tmux-colors-solarized), using the 256-color palette for broad terminal compatibility.

## Tips

### Nested tmux Sessions

When running tmux inside tmux (e.g., SSH into a server running tmux):
- Use `C-a a <command>` to send commands to the inner session
- The inner session receives `C-a` as its prefix

### Creating Named Windows

Use `C-a C` (capital C) to create a window with a specific name. This prompts for the window name and is useful for organizing work contexts.

### Quick Config Reload

After editing `~/.tmux.conf`, press `C-a r` to reload the configuration without restarting tmux. A confirmation message will appear.
