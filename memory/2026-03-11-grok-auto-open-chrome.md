# Grok auto-open Chrome profile — 2026-03-11

- User noted Grok relay may have been available in principle, but the system never proactively opened the dedicated Chrome profile after reboot.
- Fix applied:
  - Added wrapper script: `automation/grok-telegram/open-grok-profile.sh`
  - Added launch agent: `/Users/baran/Library/LaunchAgents/ai.openclaw.grok-chrome-profile.plist`
- Behavior:
  - On user login / system load, macOS launchd will open Google Chrome with the dedicated Grok profile `~/.openclaw/chrome-grok-profile` and navigate to `https://grok.com/`.
- Purpose:
  - Reduce failures after reboot/power loss by making sure the correct Chrome profile is automatically opened.
- Note:
  - This opens the profile automatically, but Browser Relay still needs the extension/tab to be in a usable state.
