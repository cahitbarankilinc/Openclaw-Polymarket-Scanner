# MEMORY.md

## Preferences

- User wants cron-related requests handled reliably and fast in new sessions.
- Preferred scheduler: **OpenClaw cron** (not `at`; host has `atrun` disabled).
- For exact Telegram message output, avoid announce summaries:
  - Schedule with `session=isolated` + `--no-deliver`.
  - Have the scheduled agent call `message` tool directly with exact text and then return `NO_REPLY`.
- For one-shot tests, use `--delete-after-run` and verify via `openclaw cron runs --id <id>` when asked.
