#!/bin/bash

# Sync dependencies with uv
uv sync

# Run the test script
uv run python -m test "$@"
