# Requirements — Clawd Pacer

1. Show weekly Claude usage % vs a pacing target on the desktop, always on top.
2. Target: 14% per day, cumulative (98% by end of day 7), growing smoothly by the hour.
3. Week window = 7 days ending at the server's `seven_day.resets_at` (Sunday 14:00 local for this user).
4. Usage is fetched automatically from the Claude usage endpoint using the local Claude Code login.
   - Unofficial endpoint: failures must never crash the app; show a "sleepy" Clawd with a reason.
   - The token is never printed, logged, or sent anywhere except Anthropic's API.
5. Moods: happy (> 5 points under target), ok (within 5), worried (> 5 over), sleepy (no data).
6. Poll no more than once every 5 minutes; manual refresh via right-click.
7. No third-party runtime dependencies (stdlib + tkinter only).
8. Personality: idle animations (blink, wave), poke = hop + boop, cheerful-coach speech bubbles.
9. Sounds are synthesized in code (no files), short (< 1.5 s), mutable from the right-click menu.
10. Random chatter at most about once an hour (45-75 min apart); no sounds 22:00-08:00 except when poked.
11. Event reactions: daily greeting, over pace, back on pace, day won, weekly reset.
12. Installable by other Windows users with one double-click; no hard-coded paths; uninstall supported.
13. Only one instance runs at a time. Unsupported setups get a plain-English message, never a traceback.

## How to run
- Double-click `scripts/install.bat` once (sets up, adds to Startup, starts). Later: `scripts/start-clawd.bat`.
- Quick console check: `python -m clawd_pacer --check`
- Tests: `.venv\Scripts\python -m pytest`
