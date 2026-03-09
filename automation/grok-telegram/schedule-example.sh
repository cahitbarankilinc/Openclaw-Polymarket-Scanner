#!/usr/bin/env bash
set -euo pipefail

# Kendi Telegram hedefini burada doldur.
# Örnekler:
#   TARGET="@kullaniciadi"
#   TARGET="123456789"
TARGET="REPLACE_TELEGRAM_TARGET"

PROMPT_FILE="/Users/baran/Desktop/grok/promt.md"
AGENT_PROMPT_FILE="/Users/baran/.openclaw/workspace/automation/grok-telegram/agent-prompt.md"

if [[ "$TARGET" == "REPLACE_TELEGRAM_TARGET" ]]; then
  echo "Önce TARGET değerini doldur." >&2
  exit 1
fi

cat > /tmp/grok-telegram-agent-message.txt <<EOF
$(cat "$AGENT_PROMPT_FILE")

Telegram hedefi: ${TARGET}
Prompt dosyası: ${PROMPT_FILE}
EOF

# Her gün 09:00 Europe/Istanbul örneği.
openclaw cron add \
  --session isolated \
  --name "grok-to-telegram-daily" \
  --cron "0 9 * * *" \
  --tz "Europe/Istanbul" \
  --message-file /tmp/grok-telegram-agent-message.txt

echo "Cron job eklendi."
