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

## Scheduling Notes (macOS)

- On this host, `at`/`atrun` is disabled by default (`com.apple.atrun` disabled).
- Jobs can be queued with `at` but may never execute unless the daemon is explicitly enabled as root.
- Default to `cron`/OpenClaw cron for scheduled tasks (including one-off tasks via self-removing cron entries).

---

Add whatever helps you do your job. This is your cheat sheet.
