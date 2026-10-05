# Clawd Pacer

A tiny pixel Clawd that lives on your Windows desktop and helps you pace your weekly Claude usage.

- Target: **14% per day** (98% by the end of the week), growing smoothly by the hour.
- Reads your weekly usage % automatically using your local Claude Code login.
- Clawd's mood shows your pace: happy (under), okay (on pace), worried (over), sleepy (no data).
- Personality: blinks, waves, hops when poked, cheerful speech bubbles, little synth beeps and chirps.
- Quiet hours (22:00-08:00), mute toggle, drag anywhere, right-click for the menu.

## Run
Requires Windows + Python 3.10+ (stdlib only) and a logged-in Claude Code.

```
python -m venv .venv
.venv\Scripts\pythonw -m clawd_pacer          # start Clawd
.venv\Scripts\python  -m clawd_pacer --check  # one-line status in the console
```
Or edit the paths in `scripts/start-clawd.bat` and copy it into `shell:startup` to launch at login.

## Heads-up
Usage comes from an **unofficial** Claude endpoint (`/api/oauth/usage`). It may change without notice;
if it does, Clawd just goes to sleep instead of crashing. Your token is read locally and only sent to Anthropic.
Not affiliated with Anthropic.

## Tests
```
.venv\Scripts\pip install pytest
.venv\Scripts\python -m pytest
```
