#!/bin/bash
# Helper script to list available code signing certificates
# Use this to find your Developer ID for build_credentials

echo "=== Available Code Signing Certificates ==="
echo ""
echo "Looking for Developer ID Application certificates..."
echo ""

# List all Developer ID Application certificates
security find-identity -v -p codesigning | grep "Developer ID Application"

echo ""
echo "Copy the certificate name (in quotes) to your build_credentials file as DEVELOPER_ID"
echo "Or leave DEVELOPER_ID blank and the first one will be used automatically."
