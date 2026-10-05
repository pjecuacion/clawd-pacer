# Changelog (technical)

## [0.3.0] - 2026-10-05
- Files added: clawd_pacer/{install,platform_check,single_instance}.py, scripts/install.bat, .gitattributes,
  tests/unit/{install-helpers,platform-instance}.test.py
- Files changed: __main__.py (platform/tkinter guard, MessageBox under pythonw, InstanceLock), config.py
  (CREDENTIALS_PATH -> CLAUDE_DIR_DEFAULT + CREDENTIALS_FILE), credentials.py (credentials_path(env) honours
  CLAUDE_CONFIG_DIR; load_token(path=None)), usage_client.py (`seven_day: null` -> Pro/Max message),
  scripts/start-clawd.bat (relative to %~dp0, uses .venv), docs/README.md.
- Installer: venv.create(with_pip=False); Startup .lnk via PowerShell WScript.Shell (single-quote escaped);
  launch with DETACHED_PROCESS. Single instance: CreateMutexW("Local\ClawdPacerSingleInstance").
- Migration: run scripts\install.bat once; remove any manually copied start-clawd.bat from shell:startup.

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
