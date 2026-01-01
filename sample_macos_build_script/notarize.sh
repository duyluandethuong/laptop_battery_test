#!/bin/bash
# Notarization script for Video Utils macOS app
# Requires: Apple Developer account, Xcode, and app already built

set -e

APP_NAME="VideoUtils"
APP_PATH="dist/${APP_NAME}.app"
BUNDLE_ID="com.lighton.videoutils"

# Load credentials from build_credentials file
CREDENTIALS_FILE="build_credentials"
if [ ! -f "$CREDENTIALS_FILE" ]; then
    echo "Error: $CREDENTIALS_FILE not found!"
    echo ""
    echo "Please create $CREDENTIALS_FILE with your credentials."
    echo "You can copy build_credentials.example and fill in your values:"
    echo "  cp build_credentials.example build_credentials"
    echo "  # Then edit build_credentials with your actual credentials"
    exit 1
fi

# Source the credentials file
source "$CREDENTIALS_FILE"

# Validate required variables
if [ -z "$TEAM_ID" ] || [ -z "$APPLE_ID" ] || [ -z "$APP_SPECIFIC_PASSWORD" ]; then
    echo "Error: Missing required credentials in $CREDENTIALS_FILE"
    echo "Required: TEAM_ID, APPLE_ID, APP_SPECIFIC_PASSWORD"
    exit 1
fi

# Find Developer ID certificate automatically (unless specified in credentials file)
if [ -z "$DEVELOPER_ID" ]; then
    # This will find a certificate like "Developer ID Application: Your Name (TEAM_ID)"
    DEVELOPER_ID=$(security find-identity -v -p codesigning | grep "Developer ID Application" | head -1 | sed 's/.*"\(.*\)".*/\1/')
    
    if [ -z "$DEVELOPER_ID" ]; then
        echo "Error: No Developer ID Application certificate found!"
        echo "Please install your Developer ID certificate in Keychain Access."
        echo "You can download it from: https://developer.apple.com/account/resources/certificates/list"
        echo ""
        echo "Alternatively, you can specify DEVELOPER_ID in $CREDENTIALS_FILE"
        exit 1
    fi
    
    echo "Found certificate: $DEVELOPER_ID"
else
    echo "Using certificate from credentials: $DEVELOPER_ID"
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Video Transcriber Notarization Script ===${NC}\n"

# Check if app exists
if [ ! -d "$APP_PATH" ]; then
    echo -e "${RED}Error: ${APP_PATH} not found!${NC}"
    echo "Please build the app first using: uv run pyinstaller VideoTranscriber.spec"
    exit 1
fi

# Check if entitlements file exists
if [ ! -f "entitlements.plist" ]; then
    echo -e "${RED}Error: entitlements.plist not found!${NC}"
    echo "Please ensure entitlements.plist exists in the project root."
    exit 1
fi

# Sign all nested binaries first (required for proper signing)
echo "Signing nested binaries and frameworks..."
find "$APP_PATH" -type f \( -name "*.dylib" -o -name "*.so" -o -name "*.framework" -o -perm +111 \) \
    -not -path "*/Contents/MacOS/*" \
    -exec codesign --force --sign "$DEVELOPER_ID" --options runtime --timestamp {} \; 2>/dev/null || true

# Check if app needs signing or force re-sign
FORCE_SIGN=false
if [ "$1" == "--force-sign" ]; then
    FORCE_SIGN=true
elif ! codesign --verify --verbose "$APP_PATH" 2>/dev/null; then
    FORCE_SIGN=true
fi

if [ "$FORCE_SIGN" = true ]; then
    echo -e "${YELLOW}Code signing ${APP_PATH}...${NC}"
    
    # Code sign the main executable with all required flags
    codesign --deep --force --sign "$DEVELOPER_ID" \
        --options runtime \
        --timestamp \
        --entitlements entitlements.plist \
        --verbose \
        "$APP_PATH"
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Code signing failed!${NC}"
        echo "Make sure you have a valid Developer ID Application certificate installed."
        exit 1
    fi
    
    echo -e "${GREEN}✓ Code signing successful${NC}\n"
else
    echo -e "${GREEN}✓ App is already code-signed${NC}\n"
fi

# Verify code signature with strict checking
echo "Verifying code signature..."
codesign --verify --deep --strict --verbose "$APP_PATH"
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Code signature verification failed!${NC}"
    exit 1
fi

# Check for hardened runtime
echo "Checking hardened runtime..."
codesign -d --entitlements - "$APP_PATH" | grep -q "com.apple.security.cs.allow-unsigned-executable-memory"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Hardened runtime enabled${NC}\n"
else
    echo -e "${YELLOW}Warning: Hardened runtime may not be properly configured${NC}\n"
fi

# Display signature details
echo "Signature details:"
codesign -dvv "$APP_PATH" 2>&1 | grep -E "(Authority|Identifier|Format|Signed Time)"
echo ""

# Create a ZIP archive for notarization (required by Apple)
ZIP_PATH="dist/${APP_NAME}_for_notarization.zip"
echo "Creating ZIP archive for notarization..."
ditto -c -k --keepParent "$APP_PATH" "$ZIP_PATH"

if [ ! -f "$ZIP_PATH" ]; then
    echo -e "${RED}Error: Failed to create ZIP archive!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ ZIP archive created: ${ZIP_PATH}${NC}\n"

# Submit for notarization
echo "Submitting app for notarization to Apple..."
echo "This may take 5-15 minutes..."

NOTARIZATION_OUTPUT=$(xcrun notarytool submit "$ZIP_PATH" \
    --apple-id "$APPLE_ID" \
    --password "$APP_SPECIFIC_PASSWORD" \
    --team-id "$TEAM_ID" \
    --wait \
    --timeout 30m 2>&1)

# Extract submission ID from output (could be in different formats)
SUBMISSION_ID=$(echo "$NOTARIZATION_OUTPUT" | grep -iE "(id:|jobId)" | head -1 | grep -oE '[a-f0-9-]{36}' | head -1)

# If --wait was used, check if output contains JSON with status
if echo "$NOTARIZATION_OUTPUT" | grep -q '"status"'; then
    # Output already contains the final status JSON
    NOTARIZATION_STATUS_JSON="$NOTARIZATION_OUTPUT"
    echo -e "${GREEN}✓ Notarization completed${NC}"
else
    # Need to check status separately
    if [ -z "$SUBMISSION_ID" ]; then
        echo -e "${RED}Error: Failed to submit for notarization!${NC}"
        echo "$NOTARIZATION_OUTPUT"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Notarization submitted. ID: ${SUBMISSION_ID}${NC}"
    
    # Check notarization status
    echo "Checking notarization status..."
    NOTARIZATION_STATUS_JSON=$(xcrun notarytool log "$SUBMISSION_ID" \
        --apple-id "$APPLE_ID" \
        --password "$APP_SPECIFIC_PASSWORD" \
        --team-id "$TEAM_ID" 2>&1)
fi

# Parse JSON to check status field - handle both "status": "Accepted" and "status":"Accepted"
STATUS=$(echo "$NOTARIZATION_STATUS_JSON" | grep -oE '"status"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"status"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')

if [ "$STATUS" = "Accepted" ]; then
    echo -e "${GREEN}✓ Notarization successful!${NC}\n"
    
    # Staple the notarization ticket to the app
    echo "Stapling notarization ticket to app..."
    xcrun stapler staple "$APP_PATH"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Notarization ticket stapled successfully${NC}\n"
    else
        echo -e "${YELLOW}Warning: Failed to staple ticket, but notarization was successful${NC}\n"
    fi
    
    # Verify stapling
    echo "Verifying stapling..."
    xcrun stapler validate "$APP_PATH"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ App is notarized and ready for distribution!${NC}\n"
    fi
    
    # Clean up ZIP file
    echo "Cleaning up..."
    rm -f "$ZIP_PATH"
    echo -e "${GREEN}✓ Cleanup complete${NC}\n"
    
    echo -e "${GREEN}=== Notarization Complete ===${NC}"
    echo "Your app is now notarized and ready for distribution!"
    echo "App location: $APP_PATH"
    
else
    echo -e "${RED}Error: Notarization failed!${NC}"
    echo "Status: $STATUS"
    echo ""
    echo "Full status JSON:"
    echo "$NOTARIZATION_STATUS_JSON"
    echo ""
    if [ -n "$SUBMISSION_ID" ]; then
        echo "Check the notarization log for details:"
        echo "xcrun notarytool log $SUBMISSION_ID --apple-id $APPLE_ID --password $APP_SPECIFIC_PASSWORD --team-id $TEAM_ID"
    fi
    exit 1
fi
