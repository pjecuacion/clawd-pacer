"""Read the Claude Code login token from disk. Never logs or prints it."""
import json
import time

from clawd_pacer.config import CREDENTIALS_PATH


class CredentialsError(Exception):
    """Token missing, unreadable, or expired."""


def is_expired(expires_at_ms, now_ms: float) -> bool:
    """True if the token has an expiry time that is already in the past."""
    return expires_at_ms is not None and expires_at_ms <= now_ms


def load_token(path: str = CREDENTIALS_PATH) -> str:
    """Return the access token, or raise CredentialsError with a friendly hint."""
    try:
        with open(path, encoding="utf-8") as f:
            oauth = json.load(f)["claudeAiOauth"]
        token = oauth["accessToken"]
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise CredentialsError("No Claude Code login found") from e
    if is_expired(oauth.get("expiresAt"), time.time() * 1000):
        raise CredentialsError("Login expired - open Claude Code")
    return token
