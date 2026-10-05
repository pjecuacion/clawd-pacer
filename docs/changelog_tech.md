# Changelog (technical)

## [0.2.0] - 2026-10-05
- Files added: clawd_pacer/{synth,sounds,player,quips,events,personality,animator,bubble}.py,
  tests/unit/{synth-wav,quips-pick,personality-events}.test.py
- Files changed: config.py (CHATTER_MINUTES, QUIET_HOURS, BUBBLE_SECONDS), status.py (Status gains
  used/target/room/day/resets_at + numbers()), sprite.py (body_pixels, pose_face, draw_clawd(pose=)),
  window.py (Callbacks dataclass replaces positional callbacks; bubble area; click-vs-drag poke; mute toggle),
  app.py (Personality + Player wiring, chatter loop every 30 s).
- Sounds: sine synth -> in-memory WAV -> winsound.PlaySound(SND_MEMORY) in a daemon thread. No sound files.
- Personality is pure (local datetimes + seeded Random passed in); events computed against last non-sleepy Status.
- Quips are ASCII-only (Tk 8.6 on Windows can't reliably render non-BMP emoji).

## [0.1.1] - 2026-10-05
- Files changed: scripts/start-clawd.cmd (removed), scripts/start-clawd.bat (added), clawd_pacer/__init__.py, docs/requirements.md
- Launcher used `%~dp0..` (breaks when copied elsewhere) and PATH `pythonw`; now absolute project path + `.venv\Scripts\pythonw.exe`.

## [0.1.0] - 2026-10-05
- Files changed: clawd_pacer/{__init__,__main__,config,pace,credentials,usage_client,status,sprite,window,app}.py,
  tests/unit/{pace-basic,usage-parse,status-build}.test.py, pytest.ini, scripts/start-clawd.cmd
- Data: GET https://api.anthropic.com/api/oauth/usage (header `anthropic-beta: oauth-2025-04-20`,
  Bearer token from ~/.claude/.credentials.json `claudeAiOauth.accessToken`). Uses `seven_day.utilization`
  and `seven_day.resets_at`; `five_hour.utilization` parsed but not yet shown.
- pace.target_pct(now, resets_at) = clamp(days since resets_at-7d, 0, 7) * 14.
- Fetch runs in a daemon thread; results passed to the Tk thread through queue.Queue (polled every 500 ms).
- No token refresh implemented on purpose (avoids racing Claude Code's own refresh).
