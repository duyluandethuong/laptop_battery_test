#!/bin/bash

# Configuration
REPO_URL="https://github.com/duyluandethuong/laptop_battery_test"
COMMIT_MSG="Update laptop battery test application"

echo "============================================"
echo "Pushing code to $REPO_URL"
echo "============================================"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed or not in the PATH."
    exit 1
fi

# Initialize git if it's not already a repo
if [ ! -d ".git" ]; then
    echo "Initializing new git repository..."
    git init
    git branch -M main
fi

# Check if remote already exists, if not add it
if ! git remote | grep -q "^origin$"; then
    echo "Adding remote origin..."
    git remote add origin "$REPO_URL"
else
    echo "Remote origin already exists, updating URL..."
    git remote set-url origin "$REPO_URL"
fi

# Add all files
echo "Adding files..."
git add .

# Commit
if git diff-index --quiet HEAD --; then
    echo "No changes to commit."
else
    echo "Committing changes..."
    git commit -m "$COMMIT_MSG"
fi

# Push
echo "Pushing to main..."
git push -u origin main

echo "============================================"
echo "Done!"
