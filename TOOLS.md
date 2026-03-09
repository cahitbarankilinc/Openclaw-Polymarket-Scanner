# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

## Grok Automation

- Fixed Chrome profile for Grok automation: `~/.openclaw/chrome-grok-profile`
- Primary Grok page: `https://grok.com/`
- Prompt source file: `/Users/baran/Desktop/grok/promt.md`
- Preferred extraction method: DOM-read final assistant response first; copy button only as fallback.

## Scheduling Notes (macOS)

- On this host, `at`/`atrun` is disabled by default (`com.apple.atrun` disabled).
- Jobs can be queued with `at` but may never execute unless the daemon is explicitly enabled as root.
- Default to **OpenClaw cron** for scheduled tasks (one-shot + recurring).
- Avoid OS `crontab` writes from agent runtime here (can hang due to environment/permissions edge cases).

### Cron Playbook (persistent preference)

- User preference: cron requests should be handled **without extra prompting** using OpenClaw cron by default.
- For exact output text (no LLM reformatting):
  - Use `openclaw cron add --session isolated --no-deliver`.
  - In job message, instruct agent to call `message` tool directly with exact text and then reply `NO_REPLY`.
- Do **not** use `--announce` when exact text is required (announce path can produce summary-style output).
- Use explicit timezone timestamps like `2026-03-07T13:10:00+03:00` when user gives local TR time.
- One-shot jobs should use `--delete-after-run`.
- After test jobs, verify with `openclaw cron runs --id <jobId>` on demand.

---

Add whatever helps you do your job. This is your cheat sheet.
