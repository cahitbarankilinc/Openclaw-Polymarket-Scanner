# MEMORY.md

## Preferences

- User wants cron-related requests handled reliably and fast in new sessions.
- Preferred scheduler: **OpenClaw cron** (not `at`; host has `atrun` disabled).
- For exact Telegram message output, avoid announce summaries:
  - Schedule with `session=isolated` + `--no-deliver`.
  - Have the scheduled agent call `message` tool directly with exact text and then return `NO_REPLY`.
- For one-shot tests, use `--delete-after-run` and verify via `openclaw cron runs --id <id>` when asked.
- Polymarket market microstructure note: for a YES outcome, `best_bid` is the best price you can currently SELL YES into, and `best_ask` is the best price you can currently BUY YES from. Keep this interpretation consistent in websocket / dashboard work.
- Weather market venue/source note: city labels can map to airport/station resolution pages (often Wunderground); prefer checking each event's `resolutionSource` instead of assuming the plain city name.
