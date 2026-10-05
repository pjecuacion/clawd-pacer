"""
Purpose: check the pacing math (target %, day number, room left, mood).
Expected: target grows 14%/day from window start (resets_at - 7d), clamped 0..98.
Related: plan v0.1.0 (docs/tasks/todo.md). No bug/lesson ID.
Preconditions: none. Fixed datetimes only; no clock, no network.
"""
from datetime import datetime, timedelta, timezone

from clawd_pacer.pace import day_number, mood, room_today, target_pct

RESET = datetime(2026, 10, 11, 3, 0, tzinfo=timezone.utc)  # Sun 14:00 Sydney
START = RESET - timedelta(days=7)


def at(days: float) -> datetime:
    return START + timedelta(days=days)


def test_target_matches_user_table_at_day_ends():
    for day in range(1, 8):
        assert target_pct(at(day), RESET) == 14 * day


def test_target_is_smooth_mid_day():
    assert target_pct(at(2.5), RESET) == 35.0


def test_target_clamped_before_start_and_after_reset():
    assert target_pct(at(-1), RESET) == 0.0
    assert target_pct(at(9), RESET) == 98.0


def test_day_number_boundaries():
    assert day_number(at(0), RESET) == 1
    assert day_number(at(0.99), RESET) == 1
    assert day_number(at(1), RESET) == 2
    assert day_number(at(7), RESET) == 7


def test_room_today_uses_end_of_day_checkpoint():
    # Day 2 checkpoint is 28%; used 20% -> 8% left.
    assert room_today(20, at(1.1), RESET) == 8.0
    assert room_today(30, at(1.1), RESET) == -2.0


def test_mood_thresholds():
    assert mood(10, 20) == "happy"
    assert mood(15, 20) == "ok"
    assert mood(25, 20) == "ok"
    assert mood(25.1, 20) == "worried"
