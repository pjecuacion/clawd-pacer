"""Turn usage numbers into what Clawd shows: a mood and two short lines."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from clawd_pacer.pace import day_number, mood, room_today, target_pct
from clawd_pacer.usage_client import Usage


@dataclass(frozen=True)
class Status:
    mood: str   # happy | ok | worried | sleepy
    line1: str
    line2: str
    used: float = 0.0
    target: float = 0.0
    room: float = 0.0
    day: int = 0
    resets_at: Optional[datetime] = None

    def numbers(self) -> dict:
        """Values for quip placeholders, rounded for display."""
        return {"used": round(self.used), "target": round(self.target),
                "room": max(0, round(self.room)), "day": self.day}


def build_status(usage: Usage, now: datetime) -> Status:
    target = target_pct(now, usage.resets_at)
    day = day_number(now, usage.resets_at)
    room = room_today(usage.weekly_pct, now, usage.resets_at)
    line1 = f"Week {usage.weekly_pct:.0f}% · goal {target:.0f}%"
    if room >= 0:
        line2 = f"Day {day}: {room:.0f}% left today"
    else:
        line2 = f"Day {day}: {-room:.0f}% over today"
    return Status(mood(usage.weekly_pct, target), line1, line2,
                  usage.weekly_pct, target, room, day, usage.resets_at)


def error_status(message: str) -> Status:
    return Status("sleepy", "zzz...", message)
