"""Clawd's brain: decides what to say, which sound, which move. Pure (no UI).

All times passed in are LOCAL wall-clock times (for quiet hours / greetings).
"""
import random
from dataclasses import dataclass, replace
from datetime import date, datetime, timedelta
from typing import List, Optional

from clawd_pacer.config import CHATTER_MINUTES, QUIET_HOURS
from clawd_pacer.events import detect_events
from clawd_pacer.quips import QuipPicker
from clawd_pacer.sounds import CHATTER_SOUNDS
from clawd_pacer.status import Status

EVENT_SOUNDS = {"greeting": "chirp", "over_pace": "uhoh", "back_on_pace": "chirp",
                "reset": "jingle", "day_win": "celebrate"}
EVENT_POSES = {"greeting": "wave", "over_pace": "idle", "back_on_pace": "wave",
               "reset": "hop", "day_win": "hop"}


@dataclass(frozen=True)
class Action:
    text: str
    sound: Optional[str] = None
    pose: str = "idle"          # idle | wave | hop


def is_quiet(now: datetime, hours=QUIET_HOURS) -> bool:
    """True inside quiet hours; handles ranges that cross midnight (22 -> 8)."""
    start, end = hours
    h = now.hour
    return start <= h < end if start < end else h >= start or h < end


class Personality:
    def __init__(self, rng: random.Random):
        self.rng = rng
        self.quips = QuipPicker(rng)
        self.status: Optional[Status] = None
        self.last_good: Optional[Status] = None
        self.greeted_on: Optional[date] = None
        self.next_chatter: Optional[datetime] = None

    def on_status(self, status: Status, now: datetime) -> List[Action]:
        """React to a fresh status: events, plus a greeting once per day."""
        self.status = status
        if status.mood == "sleepy":
            return []
        names = detect_events(self.last_good, status) if self.last_good else []
        self.last_good = status
        if self.greeted_on != now.date():
            self.greeted_on = now.date()
            names.insert(0, "greeting")
        return [self._quiet(self._event(n), now) for n in names]

    def tick(self, now: datetime) -> Optional[Action]:
        """Call often. Returns a random chatter Action roughly once an hour."""
        if self.next_chatter is None or now >= self.next_chatter:
            first = self.next_chatter is None
            low, high = CHATTER_MINUTES
            self.next_chatter = now + timedelta(minutes=self.rng.randint(low, high))
            if not first:
                return self._quiet(self._chatter(), now)
        return None

    def poke(self) -> Action:
        """You clicked Clawd. Always answers, even in quiet hours (you asked!)."""
        return Action(self._say("poke"), "boop", "hop")

    def _chatter(self) -> Action:
        mood = self.status.mood if self.status else "sleepy"
        sound = "yawn" if mood == "sleepy" else self.rng.choice(CHATTER_SOUNDS)
        return Action(self._say(mood), sound, "idle" if mood == "sleepy" else "wave")

    def _event(self, name: str) -> Action:
        return Action(self._say(name), EVENT_SOUNDS[name], EVENT_POSES[name])

    def _say(self, category: str) -> str:
        values = self.status.numbers() if self.status else Status("", "", "").numbers()
        return self.quips.pick(category, **values)

    @staticmethod
    def _quiet(action: Action, now: datetime) -> Action:
        return replace(action, sound=None) if is_quiet(now) else action
