"""Clear 'not supported' messages instead of confusing crashes."""
import sys
from typing import Optional, Tuple

MIN_PYTHON = (3, 10)


def unsupported_reason(platform: str = sys.platform,
                       version: Tuple[int, int] = sys.version_info[:2]) -> Optional[str]:
    """None if Clawd can run here, else a plain-English reason."""
    if not platform.startswith("win"):
        return ("Clawd Pacer only runs on Windows for now (it needs the Windows "
                "see-through window and sound APIs). Sorry!")
    if version < MIN_PYTHON:
        need = ".".join(map(str, MIN_PYTHON))
        have = ".".join(map(str, version))
        return f"Clawd Pacer needs Python {need} or newer (you have {have})."
    return None


def tkinter_missing() -> Optional[str]:
    """None if tkinter imports, else a hint on how to get it."""
    try:
        import tkinter  # noqa: F401
    except ImportError:
        return ("tkinter is missing. Reinstall Python from python.org and keep "
                "'tcl/tk and IDLE' ticked.")
    return None
