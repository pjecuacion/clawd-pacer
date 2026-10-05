"""
Purpose: check installer helpers that build paths and the shortcut PowerShell.
Expected: Startup folder from APPDATA; paths with spaces/quotes are quoted safely.
Related: plan v0.3.0 (docs/tasks/todo.md). No bug/lesson ID.
Preconditions: none. Pure functions only; no shortcut is created, nothing runs.
"""
from pathlib import Path

from clawd_pacer.install import (SHORTCUT_NAME, _ps_quote, shortcut_script,
                                 startup_dir, venv_pythonw)


def test_startup_dir_from_appdata():
    got = startup_dir({"APPDATA": "C:/Users/Ann/AppData/Roaming"})
    assert got == Path("C:/Users/Ann/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup")


def test_venv_pythonw_inside_project():
    assert venv_pythonw(Path("D:/My Apps/clawd")) == Path("D:/My Apps/clawd/.venv/Scripts/pythonw.exe")


def test_ps_quote_escapes_single_quotes():
    assert _ps_quote("C:/O'Brien/x") == "'C:/O''Brien/x'"


def test_shortcut_script_has_all_parts():
    script = shortcut_script(Path("C:/S/" + SHORTCUT_NAME),
                             Path("D:/My Apps/clawd/.venv/Scripts/pythonw.exe"),
                             Path("D:/My Apps/clawd"))
    assert "CreateShortcut('" in script and "Clawd Pacer.lnk'" in script
    assert "TargetPath = 'D:" in script and "My Apps" in script
    assert "$s.Arguments = '-m clawd_pacer'" in script
    assert script.endswith("$s.Save()")
