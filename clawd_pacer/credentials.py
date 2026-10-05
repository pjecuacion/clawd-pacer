"""Read the Claude Code login token from disk. Never logs or prints it."""
import json
import os
import time
from typing import Mapping, Optional

from clawd_pacer.config import CLAUDE_DIR_DEFAULT, CREDENTIALS_FILE


class CredentialsError(Exception):
    """Token missing, unreadable, or expired."""


def credentials_path(env: Mapping[str, str] = os.environ) -> str:
    """Where Claude Code keeps its login (respects CLAUDE_CONFIG_DIR)."""
    folder = env.get("CLAUDE_CONFIG_DIR") or CLAUDE_DIR_DEFAULT
    return os.path.join(os.path.expanduser(folder), CREDENTIALS_FILE)


def is_expired(expires_at_ms, now_ms: float) -> bool:
    """True if the token has an expiry time that is already in the past."""
    return expires_at_ms is not None and expires_at_ms <= now_ms


def load_token(path: Optional[str] = None) -> str:
    """Return the access token, or raise CredentialsError with a friendly hint."""
    try:
        with open(path or credentials_path(), encoding="utf-8") as f:
            oauth = json.load(f)["claudeAiOauth"]
        token = oauth["accessToken"]
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise CredentialsError("Log into Claude Code with your Pro/Max account") from e
    if is_expired(oauth.get("expiresAt"), time.time() * 1000):
        raise CredentialsError("Login expired - open Claude Code to wake me")
    return token
