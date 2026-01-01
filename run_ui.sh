#!/bin/bash

# Sync dependencies with uv
uv sync

# Run the UI application
uv run python main.py
