#!/bin/bash
# Laptop Battery Test launcher (macOS) - double-clickable in Finder.
# Syncs deps, then runs the test. The test applies the one-click system
# setup (utils/system_setup.py) automatically before the test loop starts.
#
# No sudo needed: brightness (DisplayServices), volume (osascript) and
# display-sleep prevention (caffeinate) all run as the normal user.
#
# Usage:  double-click in Finder, or from a terminal:
#           ./run.command        (full test, YouTube enabled)
#           ./run.command 1      (skip the YouTube test)

# Run from the script's own directory (matters when double-clicked).
cd "$(dirname "$0")" || exit 1

# Check uv is available.
if ! command -v uv >/dev/null 2>&1; then
    echo "Error: uv is not installed!"
    echo "Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    read -r -p "Press Enter to close..."
    exit 1
fi

echo "[1/2] Syncing dependencies..."
uv sync || { echo "Error: failed to sync dependencies!"; read -r -p "Press Enter to close..."; exit 1; }

echo "[2/2] Starting test..."
uv run python -m test "$@"

read -r -p "Press Enter to close..."
