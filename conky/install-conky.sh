#!/bin/bash

set -e  # Exit on any error

echo "========================================="
echo "Conky Power-Aware Installation Script"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Do not run this script as root. It will prompt for sudo when needed."
    exit 1
fi

# # Step 1: Install required packages
# echo ""
# print_status "Installing required packages..."
# sudo pacman -S --needed --noconfirm conky lm_sensors nvidia-utils
#
# # Step 2: Configure sensors
# echo ""
# print_status "Configuring lm_sensors..."
# print_warning "The sensors-detect script will ask questions. It's safe to answer YES to all."
# echo "Press Enter to continue..."
# read -r
# sudo sensors-detect --auto
#
# # Step 3: Detect AC adapter path
# echo ""
# print_status "Detecting AC adapter path..."
#
# AC_PATH=""
# POSSIBLE_PATHS=(
#     "/sys/class/power_supply/AC/online"
#     "/sys/class/power_supply/AC0/online"
#     "/sys/class/power_supply/ACAD/online"
#     "/sys/class/power_supply/ADP0/online"
#     "/sys/class/power_supply/ADP1/online"
# )
#
# for path in "${POSSIBLE_PATHS[@]}"; do
#     if [ -f "$path" ]; then
#         AC_PATH="$path"
#         print_status "Found AC adapter at: $AC_PATH"
#         break
#     fi
# done
#
# if [ -z "$AC_PATH" ]; then
#     print_error "Could not detect AC adapter path automatically."
#     print_warning "Please enter the path manually (or press Enter to use default):"
#     read -r user_path
#     if [ -n "$user_path" ]; then
#         AC_PATH="$user_path"
#     else
#         AC_PATH="/sys/class/power_supply/AC/online"
#         print_warning "Using default: $AC_PATH"
#     fi
# fi
#
# # Step 4: Detect battery path
# echo ""
# print_status "Detecting battery path..."
#
# BATTERY_PATH=""
# POSSIBLE_BAT_PATHS=(
#     "/sys/class/power_supply/BAT0"
#     "/sys/class/power_supply/BAT1"
#     "/sys/class/power_supply/battery"
# )
#
# for path in "${POSSIBLE_BAT_PATHS[@]}"; do
#     if [ -d "$path" ]; then
#         BATTERY_PATH="$path"
#         print_status "Found battery at: $BATTERY_PATH"
#         break
#     fi
# done
#
# if [ -z "$BATTERY_PATH" ]; then
#     print_warning "Could not detect battery path. Battery monitoring may not work."
#     BATTERY_PATH="/sys/class/power_supply/BAT0"
# fi
#
# # Step 5: Create config directory
# echo ""
# print_status "Creating configuration directory..."
# mkdir -p ~/.config/conky
#
# # Step 6: Create AC configuration
# echo ""
# print_status "Creating AC power configuration..."
#
# cat > ~/.config/conky/conky-ac.conf << 'EOF'
# conky.config = {
#     -- Window settings for Gnome Shell compatibility
#     own_window = true,
#     own_window_type = 'desktop',
#     own_window_transparent = true,
#     own_window_argb_visual = true,
#     own_window_argb_value = 0,
#     own_window_hints = 'undecorated,below,sticky,skip_taskbar,skip_pager',
#
#     -- Performance settings - AC POWER MODE (1 second updates)
#     update_interval = 1.0,
#     cpu_avg_samples = 3,
#     net_avg_samples = 2,
#
#     -- Memory optimization
#     no_buffers = true,
#
#     -- Position and size
#     alignment = 'top_right',
#     gap_x = 20,
#     gap_y = 60,
#     minimum_width = 300,
#     maximum_width = 300,
#
#     -- Drawing settings
#     double_buffer = true,
#     draw_shades = false,
#     draw_outline = false,
#     draw_borders = false,
#     draw_graph_borders = true,
#
#     -- Text settings
#     use_xft = true,
#     font = 'DejaVu Sans Mono:size=9',
#     xftalpha = 0.8,
#
#     -- Colors
#     default_color = 'white',
#     color1 = '88aadd',  -- Headers
#     color2 = 'dd8888',  -- Critical values
#     color3 = '88dd88',  -- Normal values
#     color4 = 'ffaa00',  -- AC power indicator
# }
#
# conky.text = [[
# ${color1}${font DejaVu Sans:size=11:bold}SYSTEM MONITOR${font}${color}
# ${color4}⚡ AC POWER MODE (1s updates)${color}
# ${hr 2}
#
# ${color1}CPU Usage${color}
# Average: ${cpu cpu0}% ${alignr}${cpubar cpu0 8,120}
# ${cpugraph cpu0 40,300 88dd88 dd8888 -t}
#
# ${color1}Individual Cores${color}
# ${goto 10}C1: ${cpu cpu1}% ${goto 85}C2: ${cpu cpu2}% ${goto 160}C3: ${cpu cpu3}% ${goto 235}C4: ${cpu cpu4}%
# ${goto 10}C5: ${cpu cpu5}% ${goto 85}C6: ${cpu cpu6}% ${goto 160}C7: ${cpu cpu7}% ${goto 235}C8: ${cpu cpu8}%
# ${goto 10}C9: ${cpu cpu9}% ${goto 85}C10: ${cpu cpu10}% ${goto 160}C11: ${cpu cpu11}% ${goto 235}C12: ${cpu cpu12}%
# ${goto 10}C13: ${cpu cpu13}% ${goto 85}C14: ${cpu cpu14}% ${goto 160}C15: ${cpu cpu15}% ${goto 235}C16: ${cpu cpu16}%
# ${goto 10}C17: ${cpu cpu17}% ${goto 85}C18: ${cpu cpu18}% ${goto 160}C19: ${cpu cpu19}% ${goto 235}C20: ${cpu cpu20}%
# ${goto 10}C21: ${cpu cpu21}% ${goto 85}C22: ${cpu cpu22}% ${goto 160}C23: ${cpu cpu23}% ${goto 235}C24: ${cpu cpu24}%
#
# ${color1}Memory Usage${color}
# RAM: ${mem} / ${memmax} ${alignr}${memperc}%
# ${membar 8}
# ${memgraph 40,300 88dd88 dd8888 -t}
#
# ${color1}VRAM Usage${color}
# NVIDIA: ${execi 5 nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | awk '{printf "%d / %d MB (%.1f%%)", $1, $3, ($1/$3)*100}'}
# ${execigraph 5 "nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | awk '{printf \"%.1f\", ($1/$3)*100}'" 40,300 88dd88 dd8888 -t}
#
# ${color1}Temperatures${color}
# ${execi 5 sensors | grep -E "^(Package|Core|edge|Tctl|CPU|temp1)" | head -8}
#
# ${color1}Top Processes (CPU)${color}
# ${top name 1}${alignr}${top cpu 1}%
# ${top name 2}${alignr}${top cpu 2}%
# ${top name 3}${alignr}${top cpu 3}%
# ]]
# EOF
#
# print_status "AC configuration created"
#
# # Step 7: Create Battery configuration
# echo ""
# print_status "Creating Battery configuration..."
#
# cat > ~/.config/conky/conky-battery.conf << EOF
# conky.config = {
#     -- Window settings for Gnome Shell compatibility
#     own_window = true,
#     own_window_type = 'desktop',
#     own_window_transparent = true,
#     own_window_argb_visual = true,
#     own_window_argb_value = 0,
#     own_window_hints = 'undecorated,below,sticky,skip_taskbar,skip_pager',
#
#     -- Performance settings - BATTERY MODE (3 second updates)
#     update_interval = 3.0,
#     cpu_avg_samples = 2,
#     net_avg_samples = 2,
#
#     -- Memory optimization
#     no_buffers = true,
#
#     -- Position and size
#     alignment = 'top_right',
#     gap_x = 20,
#     gap_y = 60,
#     minimum_width = 300,
#     maximum_width = 300,
#
#     -- Drawing settings
#     double_buffer = true,
#     draw_shades = false,
#     draw_outline = false,
#     draw_borders = false,
#     draw_graph_borders = true,
#
#     -- Text settings
#     use_xft = true,
#     font = 'DejaVu Sans Mono:size=9',
#     xftalpha = 0.8,
#
#     -- Colors
#     default_color = 'white',
#     color1 = '88aadd',  -- Headers
#     color2 = 'dd8888',  -- Critical values
#     color3 = '88dd88',  -- Normal values
#     color4 = 'ffaa00',  -- Battery indicator
# }
#
# conky.text = [[
# \${color1}\${font DejaVu Sans:size=11:bold}SYSTEM MONITOR\${font}\${color}
# \${color4}🔋 BATTERY MODE (3s updates)\${color}
# \${color1}Battery:\${color} \${battery_percent ${BATTERY_PATH##*/}}% \${alignr}\${battery_bar 8,120 ${BATTERY_PATH##*/}}
# \${battery_time ${BATTERY_PATH##*/}} remaining
# \${hr 2}
#
# \${color1}CPU Usage\${color}
# Average: \${cpu cpu0}% \${alignr}\${cpubar cpu0 8,120}
# \${cpugraph cpu0 40,300 88dd88 dd8888 -t}
#
# \${color1}Individual Cores\${color}
# \${goto 10}C1: \${cpu cpu1}% \${goto 85}C2: \${cpu cpu2}% \${goto 160}C3: \${cpu cpu3}% \${goto 235}C4: \${cpu cpu4}%
# \${goto 10}C5: \${cpu cpu5}% \${goto 85}C6: \${cpu cpu6}% \${goto 160}C7: \${cpu cpu7}% \${goto 235}C8: \${cpu cpu8}%
# \${goto 10}C9: \${cpu cpu9}% \${goto 85}C10: \${cpu cpu10}% \${goto 160}C11: \${cpu cpu11}% \${goto 235}C12: \${cpu cpu12}%
# \${goto 10}C13: \${cpu cpu13}% \${goto 85}C14: \${cpu cpu14}% \${goto 160}C15: \${cpu cpu15}% \${goto 235}C16: \${cpu cpu16}%
# \${goto 10}C17: \${cpu cpu17}% \${goto 85}C18: \${cpu cpu18}% \${goto 160}C19: \${cpu cpu19}% \${goto 235}C20: \${cpu cpu20}%
# \${goto 10}C21: \${cpu cpu21}% \${goto 85}C22: \${cpu cpu22}% \${goto 160}C23: \${cpu cpu23}% \${goto 235}C24: \${cpu cpu24}%
#
# \${color1}Memory Usage\${color}
# RAM: \${mem} / \${memmax} \${alignr}\${memperc}%
# \${membar 8}
# \${memgraph 40,300 88dd88 dd8888 -t}
#
# \${color1}VRAM Usage\${color}
# NVIDIA: \${execi 5 nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | awk '{printf "%d / %d MB (%.1f%%)", \$1, \$3, (\$1/\$3)*100}'}
# \${execigraph 5 "nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | awk '{printf \"%.1f\", (\$1/\$3)*100}'" 40,300 88dd88 dd8888 -t}
#
# \${color1}Temperatures\${color}
# \${execi 5 sensors | grep -E "^(Package|Core|edge|Tctl|CPU|temp1)" | head -8}
#
# \${color1}Top Processes (CPU)\${color}
# \${top name 1}\${alignr}\${top cpu 1}%
# \${top name 2}\${alignr}\${top cpu 2}%
# \${top name 3}\${alignr}\${top cpu 3}%
# ]]
# EOF
#
# print_status "Battery configuration created"
#
# print_status "Config Diff"
# diff ~/.config/conky/conky-ac.conf ~/.config/conky/conky-battery.conf

# Step 8: Create wrapper script
echo ""
print_status "Creating power-aware wrapper script..."

cat > ~/.config/conky/conky-power-aware.sh << WRAPPER_EOF
#!/bin/bash

# Detect AC adapter path
AC_PATH="$AC_PATH"

# Function to check if on AC power
is_on_ac() {
    if [ -f "\$AC_PATH" ]; then
        [ "\$(cat "\$AC_PATH")" = "1" ]
    else
        # Default to AC if can't detect
        true
    fi
}

# Determine which config to use
if is_on_ac; then
    CONFIG="\$HOME/.config/conky/conky-ac.conf"
else
    CONFIG="\$HOME/.config/conky/conky-battery.conf"
fi

# Start conky with appropriate config
exec /usr/bin/conky -c "\$CONFIG"
WRAPPER_EOF

chmod +x ~/.config/conky/conky-power-aware.sh
print_status "Wrapper script created and made executable"

# Step 9: Create systemd service
echo ""
print_status "Creating systemd user service..."

mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/conky.service << 'SERVICE_EOF'
[Unit]
Description=Conky System Monitor (Power-Aware)
After=graphical-session.target

[Service]
Type=simple
ExecStart=%h/.config/conky/conky-power-aware.sh
Restart=on-failure
RestartSec=3

[Install]
WantedBy=default.target
SERVICE_EOF

print_status "Systemd service created"

# Step 10: Create udev rule
echo ""
print_status "Creating udev rule for automatic power state switching..."

sudo tee /etc/udev/rules.d/99-conky-power.rules > /dev/null << UDEV_EOF
# Restart conky when AC power state changes
# This allows conky to switch between AC and battery configurations automatically
SUBSYSTEM=="power_supply", ATTR{online}=="0", RUN+="/usr/bin/systemctl --user --machine=\$env{USER}@.host restart conky.service"
SUBSYSTEM=="power_supply", ATTR{online}=="1", RUN+="/usr/bin/systemctl --user --machine=\$env{USER}@.host restart conky.service"
UDEV_EOF

sudo udevadm control --reload-rules
print_status "Udev rule created and reloaded"

# Step 11: Enable and start service
echo ""
print_status "Enabling and starting conky service..."

systemctl --user daemon-reload
systemctl --user enable conky.service
systemctl --user start conky.service

# Step 12: Verify installation
echo ""
print_status "Verifying installation..."

sleep 2

if systemctl --user is-active --quiet conky.service; then
    print_status "Conky is running successfully!"
else
    print_error "Conky service failed to start. Checking logs..."
    journalctl --user -u conky.service -n 20
fi

# Step 13: Display summary
echo ""
echo "========================================="
echo "Installation Complete!"
echo "========================================="
echo ""
print_status "Configuration Summary:"
echo "  - AC Mode: 1 second updates (high performance)"
echo "  - Battery Mode: 3 second updates (power saving)"
echo "  - AC Adapter Path: $AC_PATH"
echo "  - Battery Path: $BATTERY_PATH"
echo ""
print_status "Useful Commands:"
echo "  - Check status: systemctl --user status conky.service"
echo "  - View logs: journalctl --user -u conky.service -f"
echo "  - Restart: systemctl --user restart conky.service"
echo "  - Stop: systemctl --user stop conky.service"
echo "  - Disable autostart: systemctl --user disable conky.service"
echo ""
print_status "Test Power Switching:"
echo "  - Plug/unplug AC adapter and watch conky restart automatically"
echo "  - The mode indicator will show current power state"
echo ""
print_warning "If conky doesn't appear, try:"
echo "  1. Check if Gnome Shell extensions are interfering"
echo "  2. Try changing 'own_window_type' in configs to 'override' or 'normal'"
echo "  3. Restart Gnome Shell: Alt+F2, type 'r', press Enter"
echo ""

# Final verification
if pgrep -x conky > /dev/null; then
    print_status "Conky is currently running and monitoring your system!"
else
    print_warning "Conky process not found. Check service status."
fi
EOF
