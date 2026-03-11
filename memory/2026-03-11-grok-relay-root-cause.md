# Grok relay root cause — 2026-03-11

- User reported repeated Grok failures and Telegram spam.
- Root cause confirmed with `browser status profile=chrome`:
  - `running: false`
  - `cdpReady: false`
- This means the Chrome relay / attached Chrome tab for Grok was not available, so the Grok cron could not actually control the target tab and kept timing out.
- Immediate mitigation applied:
  - Disabled main Grok cron job `5b030397-7df3-421b-82b4-b6f6cde88056`
  - Disabled its failure alerts to stop Telegram spam
- Likely required human action to restore service:
  - Open Chrome on grok.com with the correct logged-in profile
  - Click the OpenClaw Browser Relay toolbar icon on that tab until badge is ON/green
  - Then the job can be re-enabled and tested
