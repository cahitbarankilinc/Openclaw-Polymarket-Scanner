#!/bin/zsh
set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
PROFILE_DIR="$HOME/.openclaw/chrome-grok-profile"
URL="https://grok.com/"
mkdir -p "$PROFILE_DIR"
/usr/bin/open -na "Google Chrome" --args --user-data-dir="$PROFILE_DIR" "$URL"
