"""Spot interesting changes between two good (non-sleepy) statuses. Pure."""
from datetime import timedelta
from typing import List

from clawd_pacer.status import Status

RESET_SLACK = timedelta(hours=1)   # resets_at jitters by microseconds; ignore that


def detect_events(prev: Status, new: Status) -> List[str]:
    """Event names, most important first. A weekly reset hides the others."""
    if prev.resets_at and new.resets_at and new.resets_at > prev.resets_at + RESET_SLACK:
        return ["reset"]
    events = []
    if new.day == prev.day + 1 and prev.room >= 0:
        events.append("day_win")
    if new.mood == "worried" and prev.mood != "worried":
        events.append("over_pace")
    elif prev.mood == "worried" and new.mood != "worried":
        events.append("back_on_pace")
    return events
