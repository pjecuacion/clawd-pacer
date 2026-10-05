"""Pure pacing math. No clock, no network: callers pass `now` in."""
from datetime import datetime, timedelta

from clawd_pacer.config import DAILY_TARGET_PCT, MOOD_BAND_PCT, WEEK_DAYS

WEEK = timedelta(days=WEEK_DAYS)


def days_elapsed(now: datetime, resets_at: datetime) -> float:
    """Days since the weekly window started, clamped to 0..7."""
    started = resets_at - WEEK
    days = (now - started).total_seconds() / 86400
    return min(max(days, 0.0), float(WEEK_DAYS))


def target_pct(now: datetime, resets_at: datetime,
               daily: float = DAILY_TARGET_PCT) -> float:
    """Smooth target: grows `daily` % per 24h since the window started."""
    return round(days_elapsed(now, resets_at) * daily, 1)


def day_number(now: datetime, resets_at: datetime) -> int:
    """Which day of the week window we're on: 1..7."""
    return min(int(days_elapsed(now, resets_at)) + 1, WEEK_DAYS)


def room_today(used: float, now: datetime, resets_at: datetime,
               daily: float = DAILY_TARGET_PCT) -> float:
    """How much % is left before hitting today's end-of-day checkpoint."""
    checkpoint = day_number(now, resets_at) * daily
    return round(checkpoint - used, 1)


def mood(used: float, target: float, band: float = MOOD_BAND_PCT) -> str:
    """happy = well under target, worried = well over, ok = in between."""
    if used > target + band:
        return "worried"
    if used < target - band:
        return "happy"
    return "ok"
