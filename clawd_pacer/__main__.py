"""Entry point.

    pythonw -m clawd_pacer          start the desktop pet (no console)
    python  -m clawd_pacer --check  print one status line and exit (any OS)
"""
import sys

from clawd_pacer.platform_check import tkinter_missing, unsupported_reason


def _fail(message: str) -> None:
    """Print, and also pop a message box when there's no console (pythonw)."""
    print(message, file=sys.stderr)
    if sys.platform.startswith("win") and sys.stdout is None:   # pythonw
        import ctypes
        ctypes.windll.user32.MessageBoxW(None, message, "Clawd Pacer", 0x30)
    sys.exit(1)


def main() -> None:
    if "--check" in sys.argv:
        from clawd_pacer.app import get_status
        s = get_status()
        print(f"[{s.mood}] {s.line1} | {s.line2}")
        return
    problem = unsupported_reason() or tkinter_missing()
    if problem:
        _fail(problem)
    from clawd_pacer.single_instance import InstanceLock
    lock = InstanceLock()
    if lock.already_running:
        return                      # another Clawd is already on screen
    from clawd_pacer.app import App
    App().run()
    lock.release()


if __name__ == "__main__":
    main()
