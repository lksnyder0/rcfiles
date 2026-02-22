# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this directory.

# Conky Power-Aware System Monitor

Power-aware system monitor for Arch Linux + Gnome Shell laptops. Automatically switches between AC (1s updates) and battery (3s updates) modes using systemd + udev.

## Files

| File | Purpose |
|------|---------|
| `conky-ac.conf` | AC power config — 1s update interval, full detail |
| `conky-battery.conf` | Battery config — 3s update interval, adds battery % section |
| `conky-power-aware.sh` | Wrapper: detects AC state and launches correct config |
| `network-info.sh` | Detects active interface, type, IP, WiFi SSID/signal |
| `docker-stats.sh` | Docker container count, memory, and container list |
| `gpu-mem-graph.sh` | NVIDIA GPU memory graph data |
| `debug.sh` | Debug helper for troubleshooting display issues |
| `install-conky.sh` | Installs systemd service, udev rule, and wrapper script |

**Important:** Changes to `conky-ac.conf` and `conky-battery.conf` usually need to be made in **both files** to stay in sync. The two configs are nearly identical except for update intervals and the battery percentage section.

## Deployed File Locations

After `install-conky.sh` runs:
```
~/.config/conky/          ← symlink target from ~/.rcfiles/conky/
~/.config/systemd/user/conky.service
/etc/udev/rules.d/99-conky-power.rules
```

The repo configs are symlinked (not copied), so edits here take effect after a service restart.

## Common Commands

```bash
# Restart after config changes
systemctl --user restart conky.service

# View live logs
journalctl --user -u conky.service -f

# Check running mode (ac or battery)
ps aux | grep conky | grep -oE 'conky-(ac|battery).conf'

# Test a config directly
conky -c ~/.config/conky/conky-ac.conf

# Test helper scripts
~/.config/conky/network-info.sh status
~/.config/conky/docker-stats.sh summary

# Monitor udev power events (for testing power switching)
udevadm monitor --property --subsystem-match=power_supply

# Run install script (first-time setup)
cd ~/.rcfiles/conky && ./install-conky.sh
```

## Architecture

Power switching uses **zero-overhead udev events** — no polling. When AC state changes, the udev rule triggers a `systemctl --user restart conky.service`, which re-runs `conky-power-aware.sh` to select the correct config.

```
udev (kernel event) → systemctl restart → conky-power-aware.sh → conky-{ac,battery}.conf
```

The `execi` intervals inside the configs control how often each section refreshes independently from the main `update_interval`:
- Docker stats: `execi 5` (AC), `execi 10` (battery)
- Network info: `execi 3` (AC), `execi 6` (battery)
- GPU/temps: `execi 5` both modes

## Key Config Settings

Both configs share this structure in `conky.config {}`:

```lua
update_interval = 1.0,         -- 1s (AC) or 3.0 (battery)
alignment = 'top_right',
gap_x = 20, gap_y = 60,
minimum_width = 300,
own_window_type = 'desktop',   -- try 'override' if invisible on Gnome
own_window_argb_value = 77,    -- 30% opacity (0=transparent, 255=opaque)
cpu_avg_samples = 3,           -- 2 in battery mode
```

## Hardware-Specific Sections

The configs target this specific hardware — adjust these when working on a different machine:

- **CPU**: 24 cores (12 physical + hyperthreading) — `cpu1`–`cpu24` in the per-core section
- **GPU**: NVIDIA (uses `nvidia-smi` via `execi`) — replace with `radeontop` for AMD
- **NVMe**: `nvme0n1` (Samsung) and `nvme1n1` (Micron) — update for different drives
- **AC path**: `/sys/class/power_supply/AC/online` — find yours with `find /sys/class/power_supply -name online`
- **Battery**: `BAT0` — check with `ls /sys/class/power_supply/`

## Troubleshooting Quick Reference

| Problem | Fix |
|---------|-----|
| Conky not visible | Change `own_window_type` to `'override'` in both configs |
| Power switching broken | Check AC path: `cat /sys/class/power_supply/AC/online` |
| Temperature missing | Run `sudo sensors-detect --auto` |
| Docker panel wrong | Test: `~/.config/conky/docker-stats.sh summary` |
| Network wrong interface | Test: `~/.config/conky/network-info.sh interface` |

See `docs/conky.md` in the repo root for full troubleshooting, customization details, and hardware compatibility notes.
