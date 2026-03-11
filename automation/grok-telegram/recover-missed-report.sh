#!/bin/zsh
set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
cd /Users/baran/.openclaw/workspace
exec /opt/homebrew/bin/node /Users/baran/.openclaw/workspace/automation/grok-telegram/recover-missed-report.mjs >> /Users/baran/.openclaw/workspace/automation/grok-telegram/recovery.log 2>&1
