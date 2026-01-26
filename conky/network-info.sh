#!/bin/bash

# Script to detect and display network information for Conky
# Handles both wired (Ethernet) and wireless (WiFi) connections

# Function to get the active network interface
get_active_interface() {
    # Get the default route interface
    ip route | grep '^default' | awk '{print $5}' | head -1
}

# Function to check if interface is wireless
is_wireless() {
    local iface=$1
    [ -d "/sys/class/net/$iface/wireless" ]
}

# Function to get IP address
get_ip() {
    local iface=$1
    ip addr show "$iface" 2>/dev/null | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1
}

# Function to get netmask
get_netmask() {
    local iface=$1
    ip addr show "$iface" 2>/dev/null | grep 'inet ' | awk '{print $2}' | cut -d'/' -f2
}

# Function to get wireless signal quality
get_wifi_signal() {
    local iface=$1
    if is_wireless "$iface"; then
        # Try /proc/net/wireless first (older method)
        local quality=$(cat /proc/net/wireless 2>/dev/null | grep "$iface" | awk '{print $3}' | sed 's/\.//')
        
        # If that fails, try nmcli (NetworkManager)
        if [ -z "$quality" ] && command -v nmcli &>/dev/null; then
            quality=$(nmcli -f IN-USE,SIGNAL dev wifi 2>/dev/null | grep '^\*' | awk '{print $2}')
        fi
        
        # If still no quality, try iw command (returns signal in dBm, convert to %)
        if [ -z "$quality" ] && command -v iw &>/dev/null; then
            local signal_dbm=$(iw dev "$iface" link 2>/dev/null | grep 'signal' | awk '{print $2}')
            if [ -n "$signal_dbm" ]; then
                # Convert dBm to percentage (rough approximation: -30dBm=100%, -90dBm=0%)
                quality=$(awk "BEGIN {print int(100 + ($signal_dbm + 30) * 100 / 60)}")
                [ "$quality" -lt 0 ] && quality=0
                [ "$quality" -gt 100 ] && quality=100
            fi
        fi
        
        # Return quality or N/A
        if [ -n "$quality" ]; then
            echo "${quality}%"
        else
            echo "N/A"
        fi
    fi
}

# Function to get wireless SSID
get_wifi_ssid() {
    local iface=$1
    if is_wireless "$iface"; then
        # Try iwgetid first (older method)
        local ssid=$(iwgetid -r "$iface" 2>/dev/null)
        
        # If iwgetid fails, try nmcli (NetworkManager)
        if [ -z "$ssid" ] && command -v nmcli &>/dev/null; then
            ssid=$(nmcli -t -f active,ssid dev wifi 2>/dev/null | grep '^yes' | cut -d: -f2)
        fi
        
        # If still no SSID, try iw command
        if [ -z "$ssid" ] && command -v iw &>/dev/null; then
            ssid=$(iw dev "$iface" link 2>/dev/null | grep 'SSID' | awk '{print $2}')
        fi
        
        # Return SSID or N/A
        echo "${ssid:-N/A}"
    fi
}

# Main logic based on command argument
COMMAND=${1:-status}
IFACE=$(get_active_interface)

case "$COMMAND" in
    interface)
        echo "$IFACE"
        ;;
    type)
        if [ -z "$IFACE" ]; then
            echo "No Connection"
        elif is_wireless "$IFACE"; then
            echo "WiFi ($IFACE)"
        else
            echo "Wired ($IFACE)"
        fi
        ;;
    ip)
        if [ -z "$IFACE" ]; then
            echo "N/A"
        else
            get_ip "$IFACE"
        fi
        ;;
    netmask)
        if [ -z "$IFACE" ]; then
            echo "N/A"
        else
            get_netmask "$IFACE"
        fi
        ;;
    ssid)
        if [ -z "$IFACE" ]; then
            echo "N/A"
        elif is_wireless "$IFACE"; then
            get_wifi_ssid "$IFACE"
        else
            echo "N/A (Wired)"
        fi
        ;;
    signal)
        if [ -z "$IFACE" ]; then
            echo "N/A"
        elif is_wireless "$IFACE"; then
            get_wifi_signal "$IFACE"
        else
            echo "N/A (Wired)"
        fi
        ;;
    status)
        if [ -z "$IFACE" ]; then
            echo "No active network connection"
        else
            IP=$(get_ip "$IFACE")
            MASK=$(get_netmask "$IFACE")
            if is_wireless "$IFACE"; then
                SSID=$(get_wifi_ssid "$IFACE")
                SIGNAL=$(get_wifi_signal "$IFACE")
                echo "WiFi: $SSID ($SIGNAL)"
                echo "Interface: $IFACE"
            else
                echo "Wired Connection"
                echo "Interface: $IFACE"
            fi
            echo "IP: $IP/$MASK"
        fi
        ;;
    *)
        echo "Usage: $0 {interface|type|ip|netmask|ssid|signal|status}"
        exit 1
        ;;
esac
