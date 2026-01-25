#!/bin/bash
#
# Docker Stats for Conky
# Provides Docker container information in Conky-compatible format
#
# Usage: docker-stats.sh [summary|containers|memory]
#

MODE="${1:-summary}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker not installed"
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "Docker daemon not running"
    exit 1
fi

# Get container count
get_container_count() {
    docker ps -q 2>/dev/null | wc -l
}

# Get total memory used by containers
get_total_memory() {
    docker stats --no-stream --format "{{.MemUsage}}" 2>/dev/null | \
        awk -F'/' '{gsub(/[^0-9.]/, "", $1); sum+=$1} END {printf "%.1f", sum}'
}

# Get container list with status
get_containers() {
    local limit="${2:-5}"
    docker ps --format "{{.Names}}: {{.Status}}" 2>/dev/null | head -n "$limit"
}

# Get container list (names only)
get_container_names() {
    local limit="${2:-5}"
    docker ps --format "{{.Names}}" 2>/dev/null | head -n "$limit"
}

# Main execution
case "$MODE" in
    summary)
        # Output: "X containers (Y MB)"
        local count=$(get_container_count)
        local memory=$(get_total_memory)
        if [ "$count" -eq 0 ]; then
            echo "No containers running"
        else
            echo "$count container(s) - ${memory} MB used"
        fi
        ;;
    
    containers)
        # Output: Container names, one per line
        get_container_names "$2"
        ;;
    
    memory)
        # Output: Just memory usage
        get_total_memory
        ;;
    
    count)
        # Output: Just container count
        get_container_count
        ;;
    
    *)
        echo "Usage: $0 [summary|containers|memory|count]"
        exit 1
        ;;
esac
