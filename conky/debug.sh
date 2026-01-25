#!/bin/bash

# Detect AC adapter path
AC_PATH="/sys/class/power_supply/ACAD/online"

# Function to check if on AC power
is_on_ac() {
    if [ -f "$AC_PATH" ]; then
        [ "$(cat "$AC_PATH")" = "1" ]
    else
        # Default to AC if can't detect
        true
    fi
}

# Determine which config to use
AC=$(cat $AC_PATH)
if is_on_ac; then
    echo "Use AC Config. is_on_ac: $AC"
    CONFIG="$HOME/.config/conky/conky-ac.conf"
else
    echo "Use BAT Config. is_on_ac: $AC"
    CONFIG="$HOME/.config/conky/conky-battery.conf"
fi

# Start conky with appropriate config
# echo "nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits"
exec /usr/bin/conky -c "$CONFIG"
