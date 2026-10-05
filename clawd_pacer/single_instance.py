"""Make sure only one Clawd runs at a time (Windows named mutex)."""
import ctypes

ERROR_ALREADY_EXISTS = 183
DEFAULT_NAME = "Local\\ClawdPacerSingleInstance"


class InstanceLock:
    """Hold this object for the app's lifetime; Windows frees it on exit."""

    def __init__(self, name: str = DEFAULT_NAME):
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateMutexW.restype = ctypes.c_void_p
        self._kernel32 = kernel32
        self._handle = kernel32.CreateMutexW(None, False, name)
        self.already_running = ctypes.get_last_error() == ERROR_ALREADY_EXISTS

    def release(self) -> None:
        if self._handle:
            self._kernel32.CloseHandle(ctypes.c_void_p(self._handle))
            self._handle = None
