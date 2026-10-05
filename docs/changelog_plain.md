# Changelog (plain)

## [0.3.0] - 2026-10-05
### Added
- One-click installer (`scripts\install.bat`): sets everything up, makes Clawd start with Windows, and starts it.
  `install.bat --uninstall` removes it from startup.
- Only one Clawd at a time, even if you start it twice.
- Clear messages instead of crashes on Mac/Linux, old Python, or missing tkinter.
### Changed
- Sleepy messages now tell you what to do (log in with Pro/Max, open Claude Code, etc.).
- `start-clawd.bat` works from wherever the folder is (no more hard-coded path).
- README rewritten for new users: who it's for, install, uninstall, troubleshooting.

## [0.2.0] - 2026-10-05
### Added
- Clawd has a personality now! It blinks, waves its claws, and hops when you click it.
- Speech bubbles with cheerful pep talks that match how you're pacing.
- Little sounds made by the app: robot beeps, bird chirps, crab claw clicks, a boop when poked.
- Reacts to moments: hello once a day, "uh-oh" when you go over pace, a cheer when you get back on track,
  a celebration when a day ends under budget, and a jingle when the week resets.
- Random chatter about once an hour. No sounds from 10pm to 8am (unless you poke it).
- "Mute sounds" in the right-click menu.

## [0.1.1] - 2026-10-05
### Fixed
- The start file now works even when copied into the Windows Startup folder, so Clawd can launch when you log in.

## [0.1.0] - 2026-10-05
### Added
- A little pixel Clawd that sits on your desktop and shows your weekly Claude usage vs your 14%-a-day goal.
- Clawd smiles when you're under pace, sweats when you're over, and naps when it can't get your numbers.
- Shows how much room you have left before today's checkpoint.
- Drag it anywhere; right-click to refresh or quit.
