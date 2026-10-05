"""
Purpose: check the text and mood Clawd shows, and that every mood has a face.
Expected: lines show week %, goal %, day and room left/over; errors -> sleepy.
Related: plan v0.1.0 (docs/tasks/todo.md). No bug/lesson ID.
Preconditions: none. Fixed datetimes; no tkinter window is opened.
"""
from datetime import datetime, timedelta, timezone

from clawd_pacer.sprite import BODY, COLS, ROWS, face_pixels
from clawd_pacer.status import build_status, error_status
from clawd_pacer.usage_client import Usage

RESET = datetime(2026, 10, 11, 3, 0, tzinfo=timezone.utc)
START = RESET - timedelta(days=7)


def test_status_on_pace_day2():
    s = build_status(Usage(20.0, RESET), START + timedelta(days=1, hours=3))
    assert s.mood == "ok"
    assert s.line1 == "Week 20% · goal 16%"
    assert s.line2 == "Day 2: 8% left today"


def test_status_over_today():
    s = build_status(Usage(40.0, RESET), START + timedelta(days=1))
    assert s.mood == "worried"
    assert s.line2 == "Day 2: 12% over today"


def test_error_status_is_sleepy():
    s = error_status("Login expired - open Claude Code")
    assert s.mood == "sleepy"
    assert s.line2 == "Login expired - open Claude Code"


def test_every_mood_face_fits_on_grid():
    assert all(len(row) == COLS for row in BODY) and len(BODY) == ROWS
    for m in ("happy", "ok", "worried", "sleepy"):
        for r, c, _ in face_pixels(m):
            assert 0 <= r < ROWS and 0 <= c < COLS


def test_unknown_mood_falls_back_to_ok():
    assert face_pixels("???") == face_pixels("ok")
