#!/bin/bash
# Full build and notarization script for Video Utils
# Handles cleaning, building, notarizing, and packaging (DMG)

set -e

APP_NAME="VideoUtils"

# Detect if we have term colors
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

echo -e "${BLUE}=== Video Transcriber Build & Release Script ===${NC}"

# 1. Prerequisites Check
echo -e "\n${BLUE}[1/5] Checking prerequisites...${NC}"
if [ ! -f "build_credentials" ]; then
    echo -e "${RED}Error: build_credentials file not found!${NC}"
    echo "Please create it from build_credentials.example before running this script."
    exit 1
fi

if [ ! -f "${APP_NAME}.spec" ]; then
    echo -e "${RED}Error: ${APP_NAME}.spec file not found!${NC}"
    exit 1
fi

if [ ! -f "notarize.sh" ]; then
    echo -e "${RED}Error: notarize.sh script not found!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites found${NC}"

# 2. Clean & Prepare
echo -e "\n${BLUE}[2/5] Cleaning previous builds...${NC}"
rm -rf build dist
echo -e "${GREEN}✓ Cleaned build and dist directories${NC}"

# 3. Build with PyInstaller
echo -e "\n${BLUE}[3/5] Building application with PyInstaller...${NC}"
echo "Syncing dependencies..."
uv sync --all-groups

echo "Running PyInstaller..."
# Using --clean to clear cache and --noconfirm to overwrite dist without asking
uv run pyinstaller ${APP_NAME}.spec --clean --noconfirm

if [ -d "dist/${APP_NAME}.app" ]; then
    echo -e "${GREEN}✓ Build successful: dist/${APP_NAME}.app${NC}"
else
    echo -e "${RED}Error: Build failed! dist/${APP_NAME}.app not found.${NC}"
    exit 1
fi

# 4. Notarize
echo -e "\n${BLUE}[4/5] Running Notarization...${NC}"
# Make sure notarize script is executable
chmod +x notarize.sh
./notarize.sh

# 5. Create DMG (Optional)
echo -e "\n${BLUE}[5/5] Creating DMG installer...${NC}"
if command -v create-dmg &> /dev/null; then
    APP_VERSION=$(grep -A 1 "CFBundleShortVersionString" dist/${APP_NAME}.app/Contents/Info.plist | tail -n 1 | sed 's/.*<string>\(.*\)<\/string>.*/\1/')
    DMG_NAME="${APP_NAME}-${APP_VERSION:-0.1.0}.dmg"
    
    echo "Creating $DMG_NAME..."
    
    # Remove existing DMG if it exists
    rm -f "$DMG_NAME"
    
    create-dmg \
      --volname "Video Transcriber" \
      --window-pos 200 120 \
      --window-size 800 400 \
      --icon-size 100 \
      --icon "${APP_NAME}.app" 200 190 \
      --hide-extension "${APP_NAME}.app" \
      --app-drop-link 600 185 \
      "$DMG_NAME" \
      "dist/"
      
    if [ -f "$DMG_NAME" ]; then
        echo -e "${GREEN}✓ DMG created successfully: $DMG_NAME${NC}"
    else
        echo -e "${RED}Error: DMG creation failed!${NC}"
    fi
else
    echo -e "${YELLOW}Warning: 'create-dmg' tool not found.${NC}"
    echo "To create a DMG, install it with: brew install create-dmg"
    echo "Skipping DMG creation."
fi

echo -e "\n${GREEN}=== Build & Release Process Complete ===${NC}"
