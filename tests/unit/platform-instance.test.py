"""
Purpose: check the 'not supported' messages and the one-Clawd-at-a-time lock.
Expected: Windows + Python 3.10+ is OK; Mac/Linux/old Python get a clear reason;
          a second lock with the same name reports already_running.
Related: plan v0.3.0 (docs/tasks/todo.md). No bug/lesson ID.
Preconditions: lock test runs on Windows only (uses a unique mutex name).
"""
import sys

import pytest

from clawd_pacer.platform_check import unsupported_reason


def test_windows_with_new_python_is_ok():
    assert unsupported_reason("win32", (3, 11)) is None


@pytest.mark.parametrize("platform", ["darwin", "linux"])
def test_mac_and_linux_get_clear_message(platform):
    assert "only runs on Windows" in unsupported_reason(platform, (3, 12))


def test_old_python_message():
    assert unsupported_reason("win32", (3, 8)) == \
        "Clawd Pacer needs Python 3.10 or newer (you have 3.8)."


@pytest.mark.skipif(not sys.platform.startswith("win"), reason="Windows mutex")
def test_second_instance_is_detected():
    from clawd_pacer.single_instance import InstanceLock
    name = "Local\\ClawdPacerTest-platform-instance"
    first = InstanceLock(name)
    second = InstanceLock(name)
    try:
        assert not first.already_running
        assert second.already_running
    finally:
        second.release()
        first.release()
    third = InstanceLock(name)
    assert not third.already_running      # freed after release
    third.release()
