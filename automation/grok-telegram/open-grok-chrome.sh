#!/usr/bin/env bash
set -euo pipefail

PROFILE_DIR="$HOME/.openclaw/chrome-grok-profile"
URL="https://grok.com/"

mkdir -p "$PROFILE_DIR"
open -na "Google Chrome" --args --user-data-dir="$PROFILE_DIR" --new-window "$URL"

echo "Chrome opened with profile: $PROFILE_DIR"
