"""
Purpose: check events, quiet hours, chatter timing, poke, and animation frames.
Expected: right event for each change; no sounds in quiet hours (except poke);
          chatter 45-75 min apart; blinks and hops happen.
Related: plan v0.2.0 (docs/tasks/todo.md). No bug/lesson ID.
Preconditions: none. Fixed local datetimes, seeded random.Random, no window.
"""
import random
from datetime import datetime, timedelta

from clawd_pacer.animator import Animator
from clawd_pacer.events import detect_events
from clawd_pacer.personality import Personality, is_quiet
from clawd_pacer.status import Status

RESET = datetime(2026, 10, 11, 3, 0)
NOON = datetime(2026, 10, 5, 12, 0)


def st(mood="ok", day=2, room=5.0, resets_at=RESET):
    return Status(mood, "l1", "l2", 20.0, 16.0, room, day, resets_at)


def test_detect_each_event():
    assert detect_events(st(), st()) == []
    assert detect_events(st(), st(resets_at=RESET + timedelta(days=7))) == ["reset"]
    assert detect_events(st(day=2, room=1), st(day=3)) == ["day_win"]
    assert detect_events(st(day=2, room=-1), st(day=3)) == []
    assert detect_events(st("ok"), st("worried")) == ["over_pace"]
    assert detect_events(st("worried"), st("happy")) == ["back_on_pace"]


def test_reset_ignores_microsecond_jitter():
    assert detect_events(st(), st(resets_at=RESET + timedelta(microseconds=50))) == []


def test_quiet_hours_cross_midnight():
    hours = [h for h in range(24) if is_quiet(NOON.replace(hour=h))]
    assert hours == [0, 1, 2, 3, 4, 5, 6, 7, 22, 23]


def test_greets_once_per_day_then_reacts_to_events():
    p = Personality(random.Random(1))
    first = p.on_status(st(), NOON)
    assert len(first) == 1 and first[0].sound == "chirp"      # greeting
    assert p.on_status(st(), NOON) == []
    over = p.on_status(st("worried"), NOON)
    assert [a.sound for a in over] == ["uhoh"]


def test_sleepy_status_triggers_nothing():
    assert Personality(random.Random(1)).on_status(st("sleepy"), NOON) == []


def test_quiet_hours_mute_events_but_keep_text():
    p = Personality(random.Random(1))
    (greet,) = p.on_status(st(), NOON.replace(hour=23))
    assert greet.sound is None and greet.text


def test_chatter_spacing_and_poke():
    p = Personality(random.Random(2))
    assert p.tick(NOON) is None                    # first call only schedules
    gap = p.next_chatter - NOON
    assert timedelta(minutes=45) <= gap <= timedelta(minutes=75)
    assert p.tick(NOON + gap - timedelta(seconds=1)) is None
    assert p.tick(NOON + gap).text
    poke = p.poke()
    assert poke.sound == "boop" and poke.pose == "hop"


def test_poke_still_sounds_in_quiet_hours():
    p = Personality(random.Random(2))
    p.on_status(st(), NOON.replace(hour=23))
    assert p.poke().sound == "boop"


def test_animator_blinks_and_hops():
    a = Animator(random.Random(5))
    poses = [a.tick()[0] for _ in range(60)]
    assert "blink" in poses
    a.start("hop")
    assert [a.tick()[1] for _ in range(4)][::2] == [-8, -8]
