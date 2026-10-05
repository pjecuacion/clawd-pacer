"""One-click installer (run by scripts/install.bat).

    python -m clawd_pacer.install               set up + start-with-Windows + start now
    python -m clawd_pacer.install --no-start    set up, don't start now
    python -m clawd_pacer.install --uninstall   remove the start-with-Windows shortcut
"""
import os
import subprocess
import sys
import venv
from pathlib import Path
from typing import Mapping

from clawd_pacer.platform_check import tkinter_missing, unsupported_reason

PROJECT = Path(__file__).resolve().parent.parent
SHORTCUT_NAME = "Clawd Pacer.lnk"


def startup_dir(env: Mapping[str, str] = os.environ) -> Path:
    return Path(env["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"


def venv_pythonw(project: Path = PROJECT) -> Path:
    return project / ".venv" / "Scripts" / "pythonw.exe"


def _ps_quote(text: str) -> str:
    """Single-quote a string for PowerShell (a ' inside becomes '')."""
    return "'" + str(text).replace("'", "''") + "'"


def shortcut_script(lnk: Path, target: Path, workdir: Path) -> str:
    """PowerShell that creates a .lnk running `pythonw -m clawd_pacer`."""
    return "; ".join([
        "$s = (New-Object -ComObject WScript.Shell).CreateShortcut(" + _ps_quote(lnk) + ")",
        "$s.TargetPath = " + _ps_quote(target),
        "$s.Arguments = '-m clawd_pacer'",
        "$s.WorkingDirectory = " + _ps_quote(workdir),
        "$s.Description = 'Clawd Pacer - Claude usage pacing buddy'",
        "$s.Save()",
    ])


def make_venv(project: Path = PROJECT) -> Path:
    """Create .venv if missing (no pip needed: Clawd uses only the stdlib)."""
    if not venv_pythonw(project).exists():
        print("Creating a private Python environment...")
        venv.create(project / ".venv", with_pip=False)
    return venv_pythonw(project)


def add_startup_shortcut(pythonw: Path, project: Path = PROJECT) -> Path:
    lnk = startup_dir() / SHORTCUT_NAME
    subprocess.run(["powershell", "-NoProfile", "-Command",
                    shortcut_script(lnk, pythonw, project)], check=True)
    return lnk


def start_clawd(pythonw: Path, project: Path = PROJECT) -> None:
    subprocess.Popen([str(pythonw), "-m", "clawd_pacer"], cwd=str(project),
                     creationflags=subprocess.DETACHED_PROCESS)


def uninstall() -> None:
    lnk = startup_dir() / SHORTCUT_NAME
    if lnk.exists():
        lnk.unlink()
    print("Removed the start-with-Windows shortcut. To quit Clawd: right-click it > Quit.")


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    problem = unsupported_reason() or tkinter_missing()
    if problem:
        print(problem)
        return 1
    if "--uninstall" in argv:
        uninstall()
        return 0
    pythonw = make_venv()
    lnk = add_startup_shortcut(pythonw)
    print(f"Clawd will start with Windows (shortcut: {lnk}).")
    if "--no-start" not in argv:
        start_clawd(pythonw)
        print("Clawd is starting - look at the bottom-right of your screen!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
