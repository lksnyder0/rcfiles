#!/bin/bash

# Detect AC adapter path
AC_PATH=""

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
if is_on_ac; then
    CONFIG="$HOME/.config/conky/conky-ac.conf"
else
    CONFIG="$HOME/.config/conky/conky-battery.conf"
fi

# Start conky with appropriate config
exec /usr/bin/conky -c "$CONFIG"
