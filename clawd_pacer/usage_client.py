"""Fetch weekly usage from the (unofficial) Claude usage endpoint."""
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from clawd_pacer.config import OAUTH_BETA, USAGE_URL


class UsageError(Exception):
    """Server unreachable, login rejected, or response shape changed."""


@dataclass(frozen=True)
class Usage:
    weekly_pct: float
    resets_at: datetime
    session_pct: Optional[float] = None


def parse_usage(data: dict) -> Usage:
    """Turn the raw JSON into a Usage. Raises UsageError if fields are missing."""
    if isinstance(data, dict) and "seven_day" in data and data["seven_day"] is None:
        raise UsageError("No weekly limit found - needs a Pro/Max plan")
    try:
        week = data["seven_day"]
        resets_at = datetime.fromisoformat(week["resets_at"])
        weekly = float(week["utilization"])
    except (KeyError, TypeError, ValueError) as e:
        raise UsageError("Usage data format changed") from e
    session = (data.get("five_hour") or {}).get("utilization")
    return Usage(weekly, resets_at, None if session is None else float(session))


def fetch_usage(token: str, url: str = USAGE_URL, timeout: float = 10) -> Usage:
    """One HTTP GET. Network/auth problems become UsageError."""
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "anthropic-beta": OAUTH_BETA,
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return parse_usage(json.load(resp))
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            raise UsageError("Login expired - open Claude Code to wake me") from e
        raise UsageError(f"Server said HTTP {e.code}") from e
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        raise UsageError("Can't reach Claude right now") from e
