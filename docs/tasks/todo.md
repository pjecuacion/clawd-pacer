# Clawd Pacer — Plan v0.1.0

Goal: a small desktop pet (pixel Clawd) that shows weekly Claude usage vs a 14%/day target.

## Scope
- Windows desktop, Python 3 + tkinter (no extra installs).
- Usage pulled automatically (unofficial endpoint, see Risks).
- Week = 7 days ending at the API's `seven_day.resets_at` (Sun 03:00 UTC = Sun 14:00 local).
- Target grows smoothly: 14% per 24h → 98% at the end of day 7.

## Non-goals (v0.1)
- No manual entry, no history charts, no installer/.exe (later).
- No token refresh of our own (would interfere with Claude Code's login).

## Steps
- [x] 0. User runs `scripts/probe_usage.py` → confirm endpoint + response shape
- [x] 1. Scaffold: git init, `clawd_pacer/__init__.py` (`__version__`), docs, tests, pytest config
- [x] 2. `pace.py` — pure math: target % at a given time, status (ahead / on pace / over)
- [x] 3. `credentials.py` — load token; detect missing/expired
- [x] 4. `usage_client.py` — fetch + parse `seven_day.utilization` / `resets_at`
- [x] 5. `sprite.py` — pixel Clawd, 4 moods: happy, ok, worried, sleepy (no data)
- [x] 6. `window.py` — transparent, always-on-top, draggable; right-click: Refresh / Quit
- [x] 7. `app.py` — wiring; poll every 5 min (gentle on the endpoint)
- [x] 8. Docs: requirements, changelogs (plain + tech) for 0.1.0
- [ ] 9. Run it live with real data (user)

## Status rules
- used < target − 5 → happy · within ±5 → ok · used > target + 5 → worried · no data → sleepy

## Test strategy
- What: pace math (day boundaries, week rollover, Sunday 14:00 anchor, clamp 0–98),
  status thresholds, API response parsing (good / missing fields / HTTP 401).
- How: pytest, fixed datetimes (no real clock), canned JSON (no network).
- Where: `tests/unit/pace-basic.test.py`, `tests/unit/usage-parse.test.py`, `tests/unit/status-build.test.py`.

## Risks
- Endpoint is unofficial; may change or vanish → Clawd goes "sleepy" with a message, never crashes.
- Token expires; Claude Code renews it when you use it. If expired → "open Claude Code" hint.

## Review
- Probe confirmed endpoint works (HTTP 200); reset time taken from API, so no reset setting needed.
- 21/21 unit tests pass (incl. HTTP 401/500 handling). All 4 moods rendered with fake data and checked by screenshot.
- Fixed during review: long messages widened the window and pushed Clawd off-center → text now wraps.
- Not verified by me: live run with real token (blocked from reading credentials; user runs it).
- Ideas for later: show 5-hour session %, start with Windows, .exe build.

---

# Plan v0.2.0 — Personality pack

Choices (user, 2026-10-05): rare chatter (~1/hour), synth sounds, quiet hours 22:00–08:00, cheerful coach.

## Scope
- Idle life: blink every few seconds, occasional claw wave, hop when poked.
- Speech bubble above Clawd (5 s), cheerful-coach quips per mood/event.
- Synth sounds generated in code (no files): beeps, chirps, crab clicks, boop, jingle, uh-oh, celebrate, yawn.
- Events: greeting (first check of a new day), over pace (mood → worried), back on pace,
  weekly reset (new `resets_at`), day win (day ended under checkpoint), poke (click).
- Random chatter: next one scheduled 45–75 min after the last.
- Quiet hours 22:00–08:00: no sounds except when you poke; bubbles still show.
- Right-click: "Mute sounds" toggle.

## Non-goals
- Real animal recordings, mute setting saved across restarts, voice/TTS.

## Steps
- [x] 1. `synth.py` — tone segments → WAV bytes (pure)
- [x] 2. `sounds.py` — named sound recipes (pure, rng passed in)
- [x] 3. `player.py` — play WAV bytes in a background thread (winsound), mute flag
- [x] 4. `quips.py` — lines per category, no immediate repeats
- [x] 5. `events.py` — detect events between old and new Status (pure)
- [x] 6. `personality.py` — decides Action(text, sound, pose) for events / chatter / poke; quiet hours
- [x] 7. Sprite poses (blink, wave), `bubble.py`, window: bubble area, click-vs-drag poke, mute menu
- [x] 8. App wiring, version 0.2.0, changelogs
- [x] 9. Visual check by screenshot
- [x] 10. Sound check by user (confirmed working 2026-10-05)

## Test strategy
- What: WAV validity/length/determinism; sound recipes all render; quip picking (seeded, no repeats);
  event detection (each event + none); quiet hours across midnight; chatter schedule; poke always speaks.
- How: pytest, seeded `random.Random`, fixed datetimes, no audio device, no window.
- Where: `tests/unit/synth-wav.test.py`, `tests/unit/personality-events.test.py`, `tests/unit/quips-pick.test.py`.

## Review
- 53/53 tests pass. Bubbles, wave and blink poses checked by screenshot with fake data.
- Changed during build: removed emoji from quips (Tk 8.6 risk); greetings made time-neutral (app may start at 3pm);
  "room" never shown negative in quips.
- Not verified by me: actual sound output (didn't want to beep at you unannounced) and live data.
- Known limit: mute resets when the app restarts.

---

# Plan v0.3.0 — Easy install for other Claude users

## Scope
- `scripts/install.bat` (tiny): finds Python (`py -3`, else `python`) and runs `clawd_pacer.install`.
- `clawd_pacer/install.py`: checks Python >= 3.10 + tkinter, makes `.venv` (no pip needed), adds a
  Startup shortcut pointing at *this* folder, starts Clawd. `--uninstall` removes the shortcut; `--no-start`.
- `scripts/start-clawd.bat`: back to folder-relative (no hard-coded path).
- Windows-only guard: clear message on Mac/Linux instead of a crash (`--check` still allowed).
- Single instance: Windows named mutex; a second launch exits quietly.
- Friendlier sleepy messages; honour `CLAUDE_CONFIG_DIR` for the login file; "needs Pro/Max" when no weekly limit.
- README rewrite: who it's for, download, install, uninstall, known limits.

## Non-goals
- Token refresh (could log users out of Claude Code), Mac/Linux support, .exe build.

## Steps
- [x] 1. credentials: `credentials_path(env)` + friendlier errors
- [x] 2. usage_client: `seven_day: null` -> "needs Pro/Max plan" message
- [x] 3. `platform_check.py` + `single_instance.py`, wired in `__main__`
- [x] 4. `install.py` + `install.bat`; relative `start-clawd.bat`
- [x] 5. README, requirements, changelogs, version 0.3.0
- [x] 6. Run installer here with `--no-start`, check the shortcut; commit + push
- [x] 7. Tag v0.3.0

## Test strategy
- What: credentials path (env set / unset), null weekly limit message, platform message,
  mutex blocks a 2nd instance (Windows only), shortcut PowerShell command (quoting, paths with spaces),
  startup folder path, Python version check.
- How: pytest, pure functions with injected env/platform; mutex uses a unique test name.
- Where: `tests/unit/install-helpers.test.py`, `tests/unit/platform-instance.test.py`, `tests/unit/usage-parse.test.py`.

## Review
- 63/63 tests pass (incl. real Windows mutex test).
- End-to-end: copied project to a temp folder with a space in its name, ran install.bat --no-start:
  venv created, Startup shortcut target/args/workdir correct, venv imports tkinter + app. --uninstall removed it.
  Then installed from E:\Git\clawd-pacer (shortcut now points there).
- Found during build: Git Bash rewrote `>nul` to `>/dev/null` in the .bat; fixed + .gitattributes forces CRLF for .bat.
- Not verified: Mac/Linux message on a real Mac (unit-tested only); fresh PC without Python.
